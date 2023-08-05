# (c) Copyright 2022 Aaron Kimball
#
# Parse DIEs in .debug_info.
# Generates information about datatypes in the program as well as location-to-method(subprogram)
# and location-to-variable mappings.

import elftools.dwarf.constants as dwarf_constants
import elftools.dwarf.dwarf_expr as dwarf_expr
import elftools.dwarf.locationlists as locationlists
from sortedcontainers import SortedDict, SortedList

import arduino_dbg.binutils as binutils
import arduino_dbg.debugger as dbg
import arduino_dbg.eval_location as el
import arduino_dbg.term as term

_INT_ENCODING = dwarf_constants.DW_ATE_signed

PUBLIC = dwarf_constants.DW_ACCESS_public
PROTECTED = dwarf_constants.DW_ACCESS_protected
PRIVATE = dwarf_constants.DW_ACCESS_private

# Response enums from ParsedDebugInfo.getNamedDebugInfoEntry()
KIND_TYPE = 1
KIND_METHOD = 2
KIND_VARIABLE = 3


class PCRange(object):
    """
    An interval of $PC values associated with a method implementation.
    """
    def __init__(self, pc_lo, pc_hi, cuns, variable_scope=None, method_name=None):
        self.pc_lo = pc_lo
        self.pc_hi = pc_hi
        self.cuns = cuns  # associated CompilationUnitNamespace
        self.method_name = method_name  # Method represented by this PCRange, if any.
        self.variable_scope = variable_scope  # A MethodInfo or LexicalScope that holds Variables.

    def includes_pc(self, pc):
        return self.pc_lo <= pc and self.pc_hi >= pc

    def __repr__(self):
        s = f'[{self.pc_lo:x}..{self.pc_hi:x}]'
        if self.method_name:
            s += f': {self.method_name}'
        return s

    def __lt__(self, other):
        return self.pc_lo < other.pc_lo or (self.pc_lo == other.pc_lo and self.pc_hi < other.pc_hi)

    def __eq__(self, other):
        return self.pc_lo == other.pc_lo and self.pc_hi == other.pc_hi

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return other.__lt__(self)

    def __lte__(self, other):
        return self < other or self == other

    def __gte__(self, other):
        return self > other or self == other


class CompilationUnitNamespace(object):
    """
        Compilation Unit-specific namespacing for types, methods, $PC ranges.
    """

    def __init__(self, die_offset, cu, range_lists, debugger):
        self._named_entries = SortedDict()  # name -> entry
        self._addr_entries = {}  # DIE offset -> entry
        self._pc_ranges = SortedList()   # Range intervals held by methods, etc. within this CU.
        self._range_lists = range_lists  # Complete .debug_range data from DWARFInfo object.

        self._die_offset = die_offset
        self._cu = cu
        self._variables = {}
        self._methods = {}

        top_die = cu.get_top_DIE()
        try:
            self._cu_ranges = None  # PCRange objects defining the CU itself, if any.
            self._low_pc = top_die.attributes['DW_AT_low_pc'].value
            self._high_pc = top_die.attributes['DW_AT_high_pc'].value
            if top_die.attributes['DW_AT_high_pc'].form != 'DW_FORM_addr':
                self._high_pc += self._low_pc  # Not absolute addr; it's offset from low pc.
        except KeyError:
            # Ordinarily location ranges are relative to the compilation unit base address,
            # but if the compilation unit is itself defined as a set of ranges, they are absolute.
            # Either way, we need _low_pc to be an integer.
            self._low_pc = 0
            self._high_pc = None

            # Compilation unit covers noncontiguous range or otherwise unknown extent.
            # CU may have multiple intervals in DW_AT_ranges.

            # print(top_die)
            range_data_offset = None
            range_attr = top_die.attributes.get('DW_AT_ranges')
            if range_attr:
                range_data_offset = range_attr.value
            if range_data_offset and range_lists:
                rangelist = range_lists.get_range_list_at_offset(range_data_offset)
                self._cu_ranges = SortedList()
                for r in rangelist:
                    # debugger.verboseprint(f'Extracted range for CU: {r.begin_offset:04x}' +
                    #     f' -- {r.end_offset:04x}')
                    self._cu_ranges.add(PCRange(r.begin_offset, r.end_offset, self))

        self.expr_parser = dwarf_expr.DWARFExprParser(cu.structs)
        self._debugger = debugger

    def getCU(self):
        return self._cu

    def getOffset(self):
        return self._die_offset

    def getLocationExprBytes(self, location_expr_data, regs):
        """
        Extract the location expr bytes (opcode stream) from DW_AT_location-like attrs.
        """
        location_expr_bytes = None
        if isinstance(location_expr_data, locationlists.LocationExpr):
            # It's a single list<int> representing the universal location expression for this var.
            location_expr_bytes = location_expr_data.loc_expr
        else:
            # It's a list of pc-dependent location entries.
            pc = regs["PC"]
            base_addr = self._low_pc
            for loc_list_entry in location_expr_data:
                if isinstance(loc_list_entry, locationlists.BaseAddressEntry):
                    # I *think* this means the list in .debug_loc is not relative to CU start,
                    # but is now relative to this value. Is this *also* relative to CU start,
                    # or is it supposed to be absolute? Don't have example data to work with.
                    base_addr = loc_list_entry.base_address
                else:
                    interval_low = base_addr + loc_list_entry.begin_offset
                    interval_high = base_addr + loc_list_entry.end_offset
                    if pc >= interval_low and pc < interval_high:
                        # We found it.
                        location_expr_bytes = loc_list_entry.loc_expr
                        break

        return location_expr_bytes


    def getExprMachine(self, location_expr_data, regs):
        """
        Return an expression evaluation machine ready to process the specified location info.
        @param location_expr_data the result of a LocationParser (either a LocationExpr or
        a list of LocationEntry/BaseAddressEntry objects).

        @return the ready-to-go expr eval machine loaded with the right location expression opcodes
        for the current PC location, or None if there is no location data valid at the current PC.
        """

        location_expr_bytes = self.getLocationExprBytes(location_expr_data, regs)
        if location_expr_bytes is None:
            # No location entry info mapped to current $PC.
            return None

        parser = self.expr_parser
        return el.DWARFExprMachine(
            parser.parse_expr(location_expr_bytes),
            regs, self._debugger)


    def getDebugger(self):
        return self._debugger

    def define_pc_range(self, pc_lo, pc_hi, scope, method_name):
        self._pc_ranges.add(PCRange(pc_lo, pc_hi, self, scope, method_name))

    def cu_contains_pc(self, pc):
        """
        Return True if the PC is in-range for this CU, or if the CU contains no PC info whatsoever.
        """
        if self._low_pc is not None and self._high_pc is not None:
            return pc >= self._low_pc and pc < self._high_pc
        elif self._cu_ranges is not None:
            for r in self._cu_ranges:
                if r.includes_pc(pc):
                    return True
            return False
        else:
            # No PC range info whatsoever associated w/ this compilation unit. Assume True.
            return True

    def is_cu_range_defined(self):
        """
        Return True if this CU declares bookend PC range information.
        """
        return (self._low_pc is not None and self._high_pc is not None) or \
            self._cu_ranges is not None

    def get_ranges_for_pc(self, pc):
        """
        Return all PCRanges for methods, lexical scopes, etc. in this CU that include $PC.
        Returned in sorted order.
        """
        out = SortedList()

        if not self.cu_contains_pc(pc):
            # Out of bounds.
            return out

        # TODO(aaron): Consider using self._pc_ranges.bisect_left() on a PCRange(pc,pc)
        # to pinpoint in O(log(N)) time instead of O(n)
        # http://www.grantjenks.com/docs/sortedcontainers/sortedlist.html#sortedcontainers.SortedList.bisect_right
        for pcr in self._pc_ranges:
            if pcr.includes_pc(pc):
                out.add(pcr)
            elif pcr.pc_lo > pc:
                # We've walked past anything relevant.
                break
        return out

    def add_entry(self, typ, name, addr):
        if name and not self._named_entries.get(name):
            self._named_entries[name] = typ

        if not addr:
            return
        elif addr in self._addr_entries:
            # If we found an entry, we're trying to multiply-define it.
            # This can happen if a convoluted-enough series of forward-references causes us to
            # seek to places which define the dependents of this entry, and then 'forward ref'
            # to this address again. Use what we've already installed at this location; ignore
            # this rework.
            assert repr(typ) == repr(self._addr_entries[addr])
            self._debugger.verboseprint(f'Already defined entry at addr {addr:x}')
        else:
            # Typical case: haven't yet bound this addr to an entry. Do so here.
            self._addr_entries[addr] = typ

    def entry_by_name(self, name):
        return self._named_entries.get(name) or None

    def entry_by_addr(self, addr):
        return self._addr_entries.get(addr) or None

    def has_addr_entry(self, addr):
        return self.entry_by_addr(addr) is not None

    def addVariable(self, var):
        self._variables[var.name] = var
        self._debugger.bind_sym_type(var.name, var)

    def getVariable(self, varname):
        return self._variables.get(varname)

    def getVariables(self):
        return self._variables.items()

    def addMethod(self, methodInfo):
        self._methods[methodInfo.method_name] = methodInfo
        self._debugger.bind_sym_type(methodInfo.method_name, methodInfo)

    def getMethod(self, methodName):
        return self._methods.get(methodName)

    def __repr__(self):
        return f'Compilation unit (@offset {self._die_offset:x})'


class DieBase(object):
    """
    Basic root object for anything we pull out of a DIE.
    """
    def __init__(self):
        self.die = None

    def get_die(self):
        """
        Retrieve debug info entry for this object.
        """
        return self.die

    def set_die(self, new_die):
        self.die = new_die

    def get_type(self):
        """
        Return underlying type for this object, if any (or None).
        """
        return None

    @staticmethod
    def __die_to_str_inner(die, recursive=False, origin_die=None, typ=None):
        lines = []
        lines.append(term.fmt(f'DIE offset=0x{die.offset:04x} tag={die.tag}', term.COLOR_CYAN))
        s = str(die)
        lines.extend(s.split('\n'))

        if recursive:
            for child in die.iter_children():
                lines.extend(DieBase.__die_to_str_inner(child, recursive))

        if typ and typ.get_die():
            typ_die = typ.get_die()
            lines.append('')
            lines.append(term.fmt(
                f'Type for 0x{die.offset:04x} at 0x{typ_die.offset:04x}:',
                term.COLOR_CYAN))
            lines.append(term.fmt(f'{typ}', term.COLOR_GRAY))
            lines.extend(DieBase.__die_to_str_inner(typ_die, recursive, None, typ.get_type()))


        if origin_die:
            lines.append('')
            lines.append(term.fmt(
                f'Origin for 0x{die.offset:04x} at 0x{origin_die.offset:04x}:',
                term.COLOR_CYAN))
            lines.extend(DieBase.__die_to_str_inner(origin_die, recursive))

        # Handle identation.
        # nb, combined with the recursion, this is O(n^2). Should be fine for reasonable
        # DIE trees, but reimplement this as O(n) if it gets out of hand.
        return list(map(lambda ln: '  ' + ln, lines))

    def die_to_str(self, recursive=False, show_origin=False, show_type=False):
        """
        Return a stringified version of the DIE.

        @param recursive - if True, also format the tree of child DIEs.
        @param show_origin - if True, also format the DIE for the origin, if any.
        """
        if self.die is None:
            return ''
        else:
            typ = None
            if show_type:
                typ = self.get_type()

            origin_die = None
            if show_origin:
                if '_origin' in self.__dict__:
                    origin_elem = self.__dict__['_origin']
                    if origin_elem and origin_elem != self and origin_elem.die is not None:
                        origin_die = origin_elem.die

            return '\n'.join(DieBase.__die_to_str_inner(self.die, recursive, origin_die, typ))


class GlobalScope(DieBase):
    """
        Container for the globally-accessible names (types, vars, methods, etc.)
        Each of these elements formally sits within some CompilationUnit but is
        also accessible here.
    """

    def __init__(self, debugger):
        self._variables = {}
        self._methods = {}
        self._debugger = debugger

    def addVariable(self, var):
        self._variables[var.name] = var
        self._debugger.bind_sym_type(var.name, var)

    def getVariable(self, varname):
        return self._variables.get(varname)

    def getVariables(self):
        return self._variables.items()

    def addMethod(self, methodInfo):
        self._methods[methodInfo.method_name] = methodInfo
        self._debugger.bind_sym_type(methodInfo.method_name, methodInfo)

    def getMethod(self, methodName):
        return self._methods.get(methodName)

    def getOrigin(self):
        return self

    def getContainingScope(self):
        return None

    def __repr__(self):
        return 'GlobalScope'


class PrgmType(DieBase):
    """
    Basic root object for a datatype or other DIE within the debugged program.
    """

    def __init__(self, name, size, parent_type=None):
        super().__init__()
        self.name = name
        self.size = size
        if size is not None and not isinstance(size, int):
            raise TypeError(f'PrgmType.size must be int or None; got type {size.__class__}')
        self._parent_type = parent_type


    def parent_type(self):
        """
        Return the type underlying this one, if any, or None otherwise.
        """
        return self._parent_type

    def is_type(self):
        """
        Return True if this is actually a true type definition; not a var/method decl
        """
        return True

    def get_type(self):
        # Implement DieBase method.
        return self._parent_type

    def pointer_depth(self):
        """
        If this is not a pointer type, return 0. Otherwise return 'n' for the number
        of layers of indirection involved.

        char x;   // depth=0
        char *x;  // depth=1
        char **x; // depth=2, etc...
        """
        return 0

    def get_dereferenced_type(self):
        """
        If this is a pointer type, return the pointed-to type.
        """
        depth = self.pointer_depth()
        if depth == 0:
            return None
        else:
            base = self
            base_depth = depth
            # Use a loop because 'const foo *' is ConstT(PtrT(foo)) and requires two descents
            # into parent_type() to return the 'foo' type.
            while base_depth == depth:
                base = base.parent_type()
                base_depth = base.pointer_depth()
            return base

    def is_array(self):
        """
        Return True if this is an array type.
        """
        return False

    def is_string(self):
        """
        Return True if this represents string-printable data.
        """
        return False

    def is_char(self):
        """
        Return True if this represents a character. (signed char)
        """
        return False

    def is_union(self):
        """
        Return True if this represents a union type.
        """
        return False

    def get_array_len(self):
        """
        If is_array() is true, return the element count.
        """
        return None

    def get_array_elem_size(self):
        """
        If is_array() is true, return the element size in bytes.
        """
        return None

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        return pad + repr(self)

    def type_tree(self, indent=0):
        """
        Print structural type information about this object.
        indent specifies the number of indentation levels (2 spaces/level) to add to each line.
        Subclasses should implement type_tree_details(indent) to add more lines of detail.
        """
        if indent >= 16:
            # Prevent runaway recurison (e.g., via printing mutually-recursive types)
            return ''

        pad = indent * '  '
        s = f'{pad}{self.__class__} (name={self.name}, size={self.size})'
        details = self.type_tree_details(indent)
        if details is not None and len(details):
            s += '\n' + details + '\n'

        parent = self.parent_type()
        if parent is not None and parent != self:
            s += f'\n{parent.type_tree(indent + 1)}'

        return s

    def __repr__(self):
        return f'{self.name}'


class PrimitiveType(PrgmType):
    """
    A fundamental type in the programming language (int, long, float, etc).
    """

    def __init__(self, name, size, signed=False):
        PrgmType.__init__(self, name, size)
        self.signed = signed

    def is_char(self):
        """
        Return True if this represents a character. (signed char)
        """
        return self.signed and self.size == 1

    def __repr__(self):
        return self.name


class ConstType(PrgmType):
    """
    A const form of another type
    """
    def __init__(self, base_type):
        if base_type.name.endswith("*"):
            # e.g. 'char* const' -- the pointer itself is const/unchangeable. The data
            # it points to may or may not be mutable.
            name = f'{base_type.name} const'
        elif base_type.name.endswith("[]"):
            # If we have a line like `char foo[] = "bar";`, foo has type `char[]` but foo
            # itself cannot be assigned to another array, so we see ConstT(ArrayT(char)).
            # Nevertheless, we do not render this 'const '.
            #
            # If we have a line like 'const char foo[] = "bar";` then foo has type `const char[]`.
            # This is represented as ConstT(ArrayT(ConstT(char))); only the inner ConstType
            # renders the string "const " in the output name.
            name = base_type.name
        else:
            # e.g. 'const char'; immutable data. (which may be pointed-to by a PointerType
            # that wraps this ConstType('char'))
            name = f'const {base_type.name}'
        PrgmType.__init__(self, name, base_type.size, base_type)
        self.name = name

    def pointer_depth(self):
        return self.parent_type().pointer_depth()

    def is_array(self):
        return self.parent_type().is_array()

    def get_array_len(self):
        return self.parent_type().get_array_len()

    def get_array_elem_size(self):
        return self.parent_type().get_array_elem_size()

    def is_string(self):
        return self.parent_type().is_string()

    def is_char(self):
        return self.parent_type().is_char()

    def is_union(self):
        return self.parent_type().is_union()

    def __repr__(self):
        return self.name


VARIABLE_LEN_ARRAY = -1  # returned in NullTermString.get_array_len()


class NullTermString(PrgmType):
    """
    A special type to represent '[const] char *' after being dereferenced in 'access()';
    tells access() to read a variable amount of data until a null terminator is encountered.
    """
    def __init__(self):
        PrgmType.__init__(self, '*(const char*)', 1, None)

    def pointer_depth(self):
        # Returns 0 because this is already the dereferenced memory region.
        return 0

    def is_char(self):
        return False

    def is_array(self):
        return True

    def is_string(self):
        return True

    def get_array_elem_size(self):
        return 1  # char size.

    def get_array_len(self):
        return VARIABLE_LEN_ARRAY

    def __repr__(self):
        return 'const char*'


class PointerType(PrgmType):
    """
    A pointer to an item of type T.
    """
    def __init__(self, base_type, addr_size):
        name = f'{base_type.name}*'
        PrgmType.__init__(self, name, addr_size, base_type)

    def pointer_depth(self):
        return self.parent_type().pointer_depth() + 1

    # currently using default of 'is_array()' looking at parent_type, which will
    # then be true only if we have an array of pointers. pointer to array will
    # return pointer=True, array=False.

    def __repr__(self):
        return f'{self.name}'


class ReferenceType(PrgmType):
    """
    A reference to an item of type T.
    """
    def __init__(self, base_type, addr_size):
        name = f'{base_type.name}&'
        PrgmType.__init__(self, name, addr_size, base_type)

    def pointer_depth(self):
        return self.parent_type().pointer_depth() + 1

    # currently using default of 'is_array()' looking at parent_type, which will
    # then be true only if we have an array of pointers. pointer to array will
    # return pointer=True, array=False.

    def __repr__(self):
        return f'{self.name}'


class EnumType(PrgmType):
    """
    An enumeration of constant->value mappings.
    """

    def __init__(self, enum_name, base_type, mappings={}):
        if enum_name is None:
            full_name = '<enum>'
        else:
            full_name = 'enum ' + enum_name
        PrgmType.__init__(self, full_name, base_type.size, base_type)
        self.enum_name = enum_name
        self.enums = {}
        for (token, val) in mappings.items():
            self.enums[token] = val

    def addEnum(self, token, val):
        self.enums[token] = val

    def enum(self, token):
        """
        Return the value for the given enum label.
        """
        return self.enums[token]

    def nameOf(self, val):
        """
        Return the enum label for the given value.
        """
        for (token, mapval) in self.enums.items():
            if val == mapval:
                return token
        return None

    def __repr__(self):
        s = f'{self.name} [size={self.size}] {{\n  '
        mappings = []
        for (token, val) in self.enums.items():
            mappings.append(f"{token} = {val}")
        s += ",\n  ".join(mappings)
        s += f'\n}}'
        return s


class ArrayType(PrgmType):
    """
    An array of items.
    """

    def __init__(self, base_type, length=0):
        PrgmType.__init__(self, f'{base_type.name}[]', base_type.size, base_type)
        self.length = length

    def setLength(self, _len):
        self.length = _len
        if self.length is not None:
            self.size = self.get_type().size * self.length
        else:
            self.size = None
        # TODO(aaron): if DW_AT_byte_size specified, that overrides the above calculation.

    def is_array(self):
        return True

    def get_array_len(self):
        """
        If is_array() is true, return the element count.
        """
        return self.length

    def get_array_elem_size(self):
        """
        If is_array() is true, return the element size in bytes.
        """
        return self.get_type().size

    def is_string(self):
        return self.parent_type().is_char()

    def is_char(self):
        return False  # Definitionally it's not a single character, it's an array.

    def __repr__(self):
        if self.length is not None:
            return f'{self.parent_type()}[{self.length}]'
        else:
            return f'{self.parent_type()}[]'


class AliasType(PrgmType):
    """
    A typedef or other alias.
    """
    def __init__(self, alias, base_type):
        PrgmType.__init__(self, alias, base_type.size, base_type)

    def pointer_depth(self):
        return self.parent_type().pointer_depth()

    def get_dereferenced_type(self):
        return self.parent_type().get_dereferenced_type()

    def is_array(self):
        return self.parent_type().is_array()

    def is_string(self):
        return self.parent_type().is_string()

    def is_char(self):
        return self.parent_type().is_char()

    def is_union(self):
        return self.parent_type().is_union()

    def get_array_len(self):
        return self.parent_type().get_array_len()

    def get_array_elem_size(self):
        return self.parent_type.get_array_elem_size()

    def __repr__(self):
        return f'typedef {self.parent_type().name} {self.name}'


class LexicalScope(DieBase):
    """
        A lexical scope (bound to a PCRange) - container for Variable definitions in a method.
    """

    def __init__(self, origin=None, containingScope=None):
        """
            * origin is the resolved abstract_origin object for this scope.
            * containingScope is a LexicalScope or Method that encloses this one, if any.
        """
        super().__init__()
        self._origin = origin
        self._containingScope = containingScope
        self._variables = {}
        self.name = '<LexicalScope>'

    def addVariable(self, var):
        self._variables[var.name] = var

    def getVariable(self, varname):
        return self._variables.get(varname)

    def getVariables(self):
        return self._variables.items()

    def getOrigin(self):
        return self._origin or self

    def getContainingScope(self):
        return self._containingScope

    def evalFrameBase(self, regs):
        scope = self.getContainingScope()
        if not scope:
            return None
        return scope.evalFrameBase(regs)

    def addFormal(self, arg):
        # Pass formal argument on to containing Method.
        if self._containingScope:
            self._containingScope.addFormal(arg)

    def getFormals(self):
        return []

    def __repr__(self):
        return 'LexicalScope'


class MethodPtrType(PrgmType):
    """
    Pointer-to-method type. Not an actual method decl/def'n.
    """
    def __init__(self, name, addr_size, return_type=None, member_of=None):
        PrgmType.__init__(self, name, addr_size, None)
        self.return_type = return_type or _VOID
        self.member_of = member_of
        self.formal_args = []

    def addFormal(self, arg):
        if arg is None:
            arg = FormalArg('', _VOID, None)
        self.formal_args.append(arg)

    def pointer_depth(self):
        return 1

    def __repr__(self):
        formals = FormalArg.filter_signature_args(self.formal_args)
        formals = ', '.join(map(lambda arg: f'{arg}', formals))
        if self.member_of:
            member = self.member_of.class_name + '::'
        else:
            member = ''

        name = self.name  # ptr-to-method doesn't need to have a name assigned.
        if name is None:
            name = ''

        return f'{self.return_type.name}({member}*{name})({formals})'


class MethodInfo(PrgmType):
    def __init__(self, method_name, return_type, cuns, member_of=None, virtual=0,
                 accessibility=1, is_decl=False, is_def=False, origin=None, die=None):

        if method_name is None:
            name = None
        else:
            name = f'{return_type.name} '
            if member_of:
                name += f'{member_of.class_name}::'
            name += f'{method_name}()'

        PrgmType.__init__(self, name, 0, None)

        self.method_name = method_name
        self.return_type = return_type
        self.member_of = member_of
        self.virtual = virtual
        self.accessibility = accessibility

        self._cuns = cuns
        self.die = die

        # Methods may appear multiple times throughout the .debug_info.
        # A forward-declared prototype signature will have is_decl=True.
        # The method proper, with its body will have is_def=True.
        # An inline-defined method in a class { ... } can be is_decl and is_def=True.
        # An inline instance of a method will have both set to False.
        # _origin should point back to the canonical declaration instance of the method.
        self.is_decl = is_decl  # Is this the _declaration_ of the method?
        self.is_def = is_def    # Is this the _definition_ of the method?

        self._variables = {}
        self._origin = origin
        self.formal_args = []
        self.frame_base = None

    def addFormal(self, arg):
        if arg is None:
            arg = FormalArg('', _VOID, None)
        arg.setScope(self)
        if arg.name is not None and len(arg.name):
            # If there is already a formal arg with this name in the method args list,
            # this is a redundant arg definition and should be flagged as such.
            # (See comments in FormalArg.__init__() for definition of 'redundant')
            existing = list(filter(lambda nm: nm == arg.name, map(lambda f: f.name, self.formal_args)))
            arg.redundant = (len(existing) > 0)  # set redundant flag if we found arg w/ same name.

        self.formal_args.append(arg)

    def getFormals(self):
        return self.formal_args

    def addVariable(self, var):
        self._variables[var.name] = var

    def getVariable(self, varname):
        return self._variables.get(varname)

    def getVariables(self):
        return self._variables.items()

    def setOrigin(self, origin):
        self._origin = origin

    def getOrigin(self):
        return self._origin or self

    def setFrameBase(self, frame_base):
        """ Set the LocationExpr / LocationList for the frame pointer """
        self._frame_base = frame_base

    def evalFrameBase(self, regs):
        """
        Evaluate the location info in frame_base to get the canonical frame addr (CFA)
        for the current method. Used in the FBREG operation for a framebase-relative
        variable storage location.
        """
        loc = self._location  # TODO(aaron): or self.getOrigin()._location??
        if loc is None:
            return None

        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return None
        return expr_machine.access(size=self.cuns.getDebugger().get_arch_conf('ret_addr_size'))

    def is_type(self):
        return False

    def get_type(self):
        # Implement DieBase method.
        return self._return_type

    def make_signature(self, include_class=False, include_die_offset=False, override_name=None):
        s = ''
        if self.accessibility == PUBLIC:
            s += 'public '
        elif self.accessibility == PROTECTED:
            s += 'protected '
        elif self.accessibility == PRIVATE:
            s += 'private '

        if self.virtual:
            s += 'virtual '

        if include_class and self.member_of:
            class_part = f'{self.member_of.class_name}::'
        else:
            class_part = ''

        use_name = self.method_name
        if override_name is not None:
            use_name = override_name

        s += f'{self.return_type.name} {class_part}{use_name}('
        s += ', '.join(map(lambda arg: f'{arg}', FormalArg.filter_signature_args(self.formal_args)))
        s += ')'
        if self.virtual == dwarf_constants.DW_VIRTUALITY_pure_virtual:
            # pure virtual.
            s += ' = 0'

        if include_die_offset and self.die:
            s += f' @ {self.die.offset:x}'
        return s

    def __repr__(self):
        return self.make_signature(include_class=False, include_die_offset=False)

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        details = pad + self.make_signature(include_class=True)
        details += '\n' + pad + 'Return Type:'
        details += '\n' + self.return_type.type_tree(indent + 1)
        details += '\n' + pad + 'Formal Args:'
        arg_lines = []
        for arg in self.formal_args:
            arg_lines.append(arg.type_tree(indent + 1))
        details += '\n'.join(arg_lines)
        return details


class FormalArg(DieBase):

    @staticmethod
    def filter_signature_args(args_list):
        """
        Return only the arguments that should appear in the method signature. We discard
        any args flagged as 'artificial' or 'redundant'.
        """
        return list(filter(lambda f: not f.artificial and not f.redundant, args_list))


    def __init__(self, name, arg_type, cuns, origin=None, location=None, const_val=None, scope=None,
                 artificial=False, redundant=False):
        super().__init__()
        self.name = name
        if arg_type is None:
            arg_type = _VOID
        self.arg_type = arg_type
        self._cuns = cuns
        self._origin = origin
        self._location = location
        self._const_val = const_val
        self._scope = scope

        self.artificial = artificial  # arg is declared 'artificial' in debug info; created by the
                                      # compiler, not the programmer. e.g. 'this' ptr in C++ member
                                      # methods. Do not show in method signature.

        self.redundant = redundant   # this is a redundant DIE for an argument of the same name.
                                     # in foo(int bar) {... } there may be multiple DIEs for 'bar',
                                     # each with different $PC-location-specific instructions for
                                     # finding the arg's value. Do not format in formals list.


    def __repr__(self):
        if self.name is None:
            return f'{self.arg_type.name}'
        else:
            return f'{self.arg_type.name} {self.name}'

    def setOrigin(self, origin):
        self._origin = origin

    def getOrigin(self):
        return self._origin or self

    def setScope(self, scope):
        self._scope = scope

    def getAddress(self, regs, frame):
        """
        Evaluate the location info to get the memory address of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the memory and register location info for the variable (in the format
              returned by the DWARFExprMachine), or None if no such info is available.
            - some LookupFlags OR'd together indicating info about the address.
        """
        loc = self._location or self.getOrigin()._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.eval()

    def getValue(self, regs, frame):
        """
        Evaluate the location info to get the current value of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the value of the variable, or None if no such info is available
            - some LookupFlags OR'd together indicating info about the value.
        """
        if self._const_val is not None:
            # It got hardcoded in the end.
            return (self._const_val, el.LookupFlags.OK | el.LookupFlags.COMPILE_TIME_CONST)

        loc = self._location or self.getOrigin()._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        self._cuns.getDebugger().verboseprint("Getting value for formal arg: ", self.name)
        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.access(self.arg_type)

    def get_type(self):
        # Implement DieBase method.
        return self.arg_type

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        details = pad + 'Formal arg: ' + repr(self)
        details += '\n' + pad + 'Arg type:'
        details += '\n' + self.arg_type.type_tree(indent + 1)
        return details

    def type_tree(self, indent=0):
        """
        Print structural type information about this object.
        indent specifies the number of indentation levels (2 spaces/level) to add to each line.
        Subclasses should implement type_tree_details(indent) to add more lines of detail.
        """
        pad = indent * '  '
        s = f'{pad}{self.__class__} (name={self.name})'
        details = self.type_tree_details(indent)
        if details is not None and len(details):
            s += '\n' + details + '\n'

        return s


class FieldType(PrgmType):
    def __init__(self, field_name, member_of, field_type, offset, accessibility):
        PrgmType.__init__(self, f'{member_of.name}::{field_name} {field_type}', field_type.size, field_type)
        self.field_name = field_name
        self.member_of = member_of
        self.offset = offset
        self.accessibility = accessibility

    def is_type(self):
        return False

    def __repr__(self):
        if self.accessibility == PUBLIC:
            acc = 'public'
        elif self.accessibility == PROTECTED:
            acc = 'protected'
        elif self.accessibility == PRIVATE:
            acc = 'private'
        else:
            acc = 'public'  # Assume public by default.

        if self.offset is None:
            offset_str = ''
        else:
            offset_str = f', offset={self.offset:#x}'

        return f'{acc} {self.parent_type().name} {self.field_name} ' + \
            f'[size={self.parent_type().size}{offset_str}]'


class ClassType(PrgmType):
    """
    A class or struct.
    """
    def __init__(self, class_name, size, base_type):
        # TODO(aaron): how does 'base_type' interact with multiple inheritance? diamond inheritance?
        if class_name is None:
            full_name = '<class>'
        else:
            full_name = 'class ' + class_name
        PrgmType.__init__(self, full_name, size, base_type)

        self.class_name = class_name
        self.methods = []
        self.fields = []


    def addMethod(self, method_type):
        self.methods.append(method_type)

    def getMethod(self, methodName):
        for m in self.methods:
            if m.method_name == methodName:
                return m
        return None

    def addField(self, field_type):
        self.fields.append(field_type)

    def getField(self, fieldName):
        for f in self.fields:
            if f.field_name == fieldName:
                return f
        return None

    def __repr__(self):
        s = f'{self.name}'
        if self.parent_type():
            s += f' <subtype of {self.parent_type().name}>'
        s += ' {\n'
        decl_methods = list(filter(lambda m: m.is_decl, self.methods))
        if len(decl_methods) + len(self.fields) > 0:
            s += '  '
        s += ';\n  '.join(map(lambda m: f'{m}', decl_methods + self.fields))
        if len(decl_methods) + len(self.fields) > 0:
            s += ';\n'
        s += '}'
        return s

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        details = pad + f'class {self.class_name}'
        details += '\n' + pad + 'Methods:\n' + pad
        method_lines = []
        for method in self.methods:
            method_lines.append(method.make_signature(True))
        details += f'\n{pad}'.join(method_lines)
        details += '\n' + pad + 'Fields:\n'
        field_lines = []
        for field in self.fields:
            field_lines.append(field.type_tree(indent + 1))
        details += '\n'.join(field_lines)
        return details


class UnionType(PrgmType):
    """
    A union (OR-type)
    """
    def __init__(self, union_name, size, base_type):
        # TODO(aaron): Do these actually have a base type?
        if union_name is None:
            full_name = '<union>'
        else:
            full_name = 'union ' + union_name
        PrgmType.__init__(self, full_name, size, base_type)

        self.union_name = union_name
        self.fields = []


    def addField(self, field_type):
        self.fields.append(field_type)

    def getField(self, fieldName):
        for f in self.fields:
            if f.field_name == fieldName:
                return f
        return None

    def is_union(self):
        return True

    def __repr__(self):
        s = f'{self.name}'
        if self.parent_type():
            s += f' <subtype of {self.parent_type().name}>'
        s += f' [size={self.size}] {{\n'
        if len(self.fields) > 0:
            s += '  '
        s += ';\n  '.join(map(lambda m: f'{m}', self.fields))
        if len(self.fields) > 0:
            s += ';\n'
        s += '}'
        return s

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        details = pad + f'union {self.union_name}'
        details += '\n' + pad + 'Fields:\n' + pad
        field_lines = []
        for field in self.fields:
            field_lines.append(field.type_tree(indent + 1))
        details += '\n'.join(field_lines)
        return details


class PtrToMember(PrgmType):
    """
    Pointer to member field or method of a class/struct.
    """

    def __init__(self, ptr_name, addr_size, member_type, class_type):
        PrgmType.__init__(self, ptr_name, addr_size, member_type)
        self.member_type = member_type
        self.class_type = class_type

    def pointer_depth(self):
        return self.parent_type().pointer_depth() + 1

    def __repr__(self):
        if self.name is None:
            namestr = ''
        else:
            namestr = self.name

        if isinstance(self.member_type, MethodInfo):
            # Pointer-to-method syntax; embed the name of this pointer-type (if any) in place
            # of the actual member method name in its own signature.
            namestr = '*' + namestr
            return self.member_type.make_signature(include_class=True, override_name=namestr)
        else:
            # Pointer to field
            return f'{self.member_type} {self.class_type}::{namestr}*'




class DwarfProcedure(DieBase):
    """
    A DWARF Procedure is a `location` attribute containing a dwarf expr that can be invoked
    during evaluation of other location expressions.
    """

    def __init__(self, cuns, location=None, const_val=None, scope=None):
        self._cuns = cuns
        self._location = location
        self._const_val = const_val
        self._scope = scope

    def getAddress(self, regs, frame):
        """
        Evaluate the location info to get the memory address of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the memory and register location info for the variable (in the format
              returned by the DWARFExprMachine), or None if no such info is available.
            - some LookupFlags OR'd together indicating info about the address.
        """
        loc = self._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.eval()

    def getValue(self, regs, frame):
        """
        Evaluate the location info to get the current value of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the value of the variable, or None if no such info is available
            - some LookupFlags OR'd together indicating info about the value.
        """
        if self._const_val is not None:
            # It got hardcoded in the end.
            return (self._const_val, el.LookupFlags.OK | el.LookupFlags.COMPILE_TIME_CONST)

        loc = self._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        self._cuns.getDebugger().verboseprint("Evaluating DWARF Procedure")
        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.access(size=el.DWARFExprMachine.ALL)

    def setConstValue(self, val):
        """
        This expression has been const-reduced.
        """
        self._const_val = val


class VariableInfo(PrgmType):
    """
    Info record for a variable (not struct field) defined globally/statically in a file or
    locally within a method.

    A single variable may have multiple VariableInfo records associated with it to distinguish
    forward declaration vs the resolved definition. Local variables within a method that is
    inlined to multiple locations may also have multiple definitions.
    """
    def __init__(self, var_name, var_type, cuns, location=None, is_decl=False, is_def=False,
                 origin=None, scope=None):

        PrgmType.__init__(self, var_name, var_type.size)
        self.var_name = var_name
        self.var_type = var_type
        self._cuns = cuns           # CompilationUnitNS owner of this DIE (needed to eval locations)
        self._location = location   # Expression (or pc range -> expr list) defining how to find
                                    # the value in the prgm memory / regs
        self._const_val = None

        self.is_decl = is_decl      # See MethodInfo for definitions of these two flags.
        self.is_def = is_def

        self._origin = origin       # Resolved DW_AT_abstract_origin, if any, poiting decl->def
        self._scope = scope

    def __repr__(self):
        return f'{self.var_type.name} {self.var_name}'

    def setOrigin(self, origin):
        self._origin = origin

    def getOrigin(self):
        # TODO(aaron): Should this be recursive?
        return self._origin or self

    def getAddress(self, regs, frame):
        """
        Evaluate the location info to get the memory address of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the memory and register location info for the variable (in the format
              returned by the DWARFExprMachine), or None if no such info is available.
            - some LookupFlags OR'd together indicating info about the address.
        """
        loc = self._location or self.getOrigin()._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.eval()

    def getValue(self, regs, frame):
        """
        Evaluate the location info to get the current value of this variable.

        @param regs the current register state for the frame.
        @param frame the backtrace frame for this variable's scope.
        @return a tuple containing:
            - the value of the variable, or None if no such info is available
            - some LookupFlags OR'd together indicating info about the value.
        """
        if self._const_val is not None:
            # It got hardcoded in the end.
            return (self._const_val, el.LookupFlags.OK | el.LookupFlags.COMPILE_TIME_CONST)

        loc = self._location or self.getOrigin()._location
        if loc is None:
            return (None, el.LookupFlags.ERR_NO_LOCATION)

        self._cuns.getDebugger().verboseprint("Getting value for local var: ", self.name)
        expr_machine = self._cuns.getExprMachine(loc, regs)
        if expr_machine is None:
            return (None, el.LookupFlags.ERR_PC_OUT_OF_BOUNDS)
        expr_machine.setScope(self._scope)
        expr_machine.setFrame(frame)
        return expr_machine.access(self.var_type)

    def setConstValue(self, val):
        """
        This variable has been const-reduced.
        """
        self._const_val = val

    def is_type(self):
        return False

    def get_type(self):
        # Implement DieBase method.
        return self.var_type

    def type_tree_details(self, indent):
        """
        Return additional details about this object for the Type Tree.
        Each line of text output should be indented by 2*indent spaces.
        """
        pad = indent * '  '
        details = pad + 'Variable: ' + repr(self)
        details += '\n' + pad + 'Var type:'
        details += '\n' + self.var_type.type_tree(indent + 1)
        return details




class ParsedDebugInfo(object):
    """
    Parsed .debug_info data state.
    """

    # List of 'context' keys for .debug_info DIE parsing that should always be in the `context`
    # map. Keep this in sync with the fields populated in context in parseTypeInfo()
    _default_context_keys = [
        'debugger', 'int_size', 'range_lists', 'loc_lists', 'dwarf_ver',
        'nesting', 'print_full_die']

    def __init__(self, debugger):
        self._debugger = debugger

        self._encodings = {}  # Global encodings table (encodingId -> PrgmTypE)
        self._cu_namespaces = []  # Set of CompilationUnitNamespace objects.
        self._global_syms = GlobalScope(debugger)  # vars/methods tagged DW_AT_external visible from any CU.

        self.int_size = debugger.get_arch_conf("int_size")
        self.addr_size = debugger.get_arch_conf("ret_addr_size")
        self._populateEncodings()  # Get base types in the encodings map.

    def types(self, prefix=None):
        """
        Iterator over all typedefs.

        If prefix is specified, returns all type names that begin with 'prefix'.
        """
        if prefix is None or len(prefix) == 0:
            nextfix = None  # Empty str prefix means return all types.
            prefix = None
        else:
            # Increment the last char of the string to get the first possible type
            # after the matching set.
            last_char = prefix[-1]
            next_char = chr(ord(last_char) + 1)
            nextfix = prefix[0:-1] + next_char

        for cuns in self._cu_namespaces:
            # Do a prefix search.
            #
            # Note that this will efficiently search for appropriate keys across all
            # compilation units, but it will yield items in sorted order only per-CU; a
            # globally sorted list requires yielding all items and then sorting the results.
            for name in cuns._named_entries.irange(prefix, nextfix, inclusive=(True, False)):
                typ = cuns._named_entries[name]
                if typ.is_type():
                    yield (name, typ)

    def getDebugInfoEntryByOffset(self, offset):
        """
        Return the DIE at the specified offset into the .debug_info section, or None
        if there is not one available.
        """
        for cuns in self._cu_namespaces:
            if cuns.has_addr_entry(offset):
                return cuns.entry_by_addr(offset)
        return None


    def getNamedDebugInfoEntry(self, name, pc):
        """
        Return the debug info object for a given name in the compilation unit associated with $PC.
        This can be a named type, a method, or a variable.
        This method returns a pair of (KIND, entry).
        """
        pc_ranges = SortedList()
        search_cuns = None
        for cuns in self._cu_namespaces:
            if cuns.cu_contains_pc(pc) and cuns.is_cu_range_defined():
                # The above update is the exclusive namespace search we need.
                # Don't keep searching.
                search_cuns = cuns
                break
            elif cuns.cu_contains_pc(pc):
                # Try to search method-by-method to see if this cuns covers it.
                pc_ranges.update(cuns.get_ranges_for_pc(pc))
                if len(pc_ranges) > 0:
                    # Yes, we found it.
                    search_cuns = cuns
                    break

        if search_cuns is None:
            return None  # We fell off the edge into outer space?

        # search_cuns is the CompilationUnitNamespace that encloses the $PC.

        # Use the various lookup tables available to us:
        # we are either looking up a literal type, a signature for a method name, or a type for a var.
        typ = search_cuns.getMethod(name)
        if typ:
            return (KIND_METHOD, typ)

        typ = search_cuns.getVariable(name)
        if typ:
            return (KIND_VARIABLE, typ)

        typ = search_cuns.entry_by_name(name)
        if typ:
            return (KIND_TYPE, typ)

        # Also search globals if not found locally.
        global_entry = self._global_syms.getVariable(name)
        if global_entry:
            return (KIND_VARIABLE, global_entry)

        global_entry = self._global_syms.getMethod(name)
        if global_entry:
            return (KIND_METHOD, global_entry)

        return (None, None)


    def getMethodsForPC(self, pc):
        """
        Return a list identifying method(s) that contain the specified $PC.
        If the PC is in a "normal" method, this will be a singleton list.
        However, if the method (as identified on the stack frame) body contains other inlined methods
        (which may happen recursively), this provides a list from narrowest to widest of the
        method(s) where the PC currently is.

        e.g. if we have:
        inline void inner2() { ...; /* $PC */; ... }
        inline void inner1() { ...; inner2(); ... }
        void outermost() {
            inner1();
        }

        then getMethodsForPC($PC) will return ['inner2', 'inner1', 'outermost']
        """
        pc_ranges = SortedList()
        for cuns in self._cu_namespaces:
            pc_ranges.update(cuns.get_ranges_for_pc(pc))

        out = []
        for pcr in pc_ranges:
            if pcr.method_name:
                out.append(pcr.method_name)

        # print(f"inline chains: {pc:x} -> {out}")
        out.reverse()
        return out

    def getScopesForPC(self, pc, include_global=False):
        """
        Return a list of methods, inlined methods, and lexical scopes that enclose the specified PC.

        @param pc the current program counter value for the frame.
        @param include_global if true includes a GlobalScope object showing what globals can be
            accessed from the $PC.

        @return the enclosing scopes, sorted from widest to tightest.
        """
        out = []
        used_set = set()

        pc_ranges = SortedList()

        for cuns in self._cu_namespaces:
            pc_ranges.update(cuns.get_ranges_for_pc(pc))

            if cuns.cu_contains_pc(pc) and cuns.is_cu_range_defined():
                # The above update is the exclusive namespace search we need.

                # If include_globals is true, then include the CUNS itself as a containing scope..
                if include_global:
                    out.append(cuns)

                # Don't keep searching.
                break


        for pcr in pc_ranges:
            if pcr.variable_scope and pcr.variable_scope not in used_set:
                # We have not yet seen this variable scope. Add to output.
                out.append(pcr.variable_scope)

                # Save variable scopes as dict keys to get the unique set,
                # as a lexical scope's variable_scope may just point to the enclosing method.
                used_set.add(pcr.variable_scope)

        if include_global:
            # if include_globals, include the GlobalScope object too.
            out.insert(0, self._global_syms)

        return out

    def _populateEncodings(self):
        """
        Set up initial primitive types that also map to the 'encoding' attr of some DIE types.
        """
        def _add(n, typ):
            if n is not None:
                self._encodings[n] = typ

        global _VOID
        _VOID = PrimitiveType('void', 0)
        _add(0, _VOID)
        _add(1, PrimitiveType('<ptr>', self.addr_size))
        _add(2, PrimitiveType('bool', 1))
        # 3 is 'complex float'
        _add(4, PrimitiveType('float', 4))
        _add(5, PrimitiveType('int', self.int_size, signed=True))
        _add(6, PrimitiveType('char', 1, signed=True))
        _add(7, PrimitiveType('unsigned int', self.int_size, signed=False))
        _add(8, PrimitiveType('unsigned char', 1, signed=False))
        _add(0x10, PrimitiveType('<UTF8_string>', 1))
        _add(0x12, PrimitiveType('<ASCII_string>', 1))

    def parseTypesFromDIE(self, die, cuns, context={}):
        """
            Parse a DIE within a specific CompilationUnitNamespace

            @param die the DIE to process.
            @param cuns the current CompilationUnitNamespace
            @param context additional context for nested DIE processing.
        """
        cu = cuns.getCU()
        cu_offset = cu.cu_offset
        debugger = context['debugger']
        nesting = context['nesting']

        if context['print_full_die'] is not None and context['print_full_die'] >= nesting:
            # If full DIE dumping was enabled, and we're at the same (or further-out) nesting
            # level as when we enabled dumping, turn it off. We've stopped recursing into subtrees
            # of the chosen DIE, and we're now at its next sibling (or parent).
            context['print_full_die'] = None

        # Hack for debugging the debugger: if the die.offset is in this list, then verboseprint()
        # the entire DIE data structure, as well as that of any child DIEs, recursively.
        # e.g.: PRINT_DIE_TREE_OFFSETS = [ 0x11b6, 0x47dc, 0x4843 ]
        PRINT_DIE_TREE_OFFSETS = []
        # You can also field-configure a specific DIE offset to dump it + its subtree.
        PRINT_DIE_TREE_OFFSETS.append(debugger.get_conf('dbg.print_die.offset'))
        try:
            PRINT_DIE_TREE_OFFSETS.index(die.offset)
            context['print_full_die'] = nesting  # Enable super-verbose DIE debugging.
        except Exception:
            pass  # We don't need to print the entire DIE tree below here.

        # Early-return conditions that terminate recursion.
        if not die.tag:
            return  # null DIE to terminate nested set.
        elif cuns.has_addr_entry(die.offset):
            return  # Our seek-driven parsing has already parsed this entry, don't double-process.

        # Declare various helper methods needed internally within DIE-parsing process.
        def _fresh_context():
            """
            Return a context that is 'clean' of any nested DIE state, for use in non-local
            parsing requirements.
            """
            ctxt = {}
            for key in ParsedDebugInfo._default_context_keys:
                ctxt[key] = context[key]

            ctxt['nesting'] = 0             # wipe/reset nesting level back to 0 for a jump to DIE.
            ctxt['print_full_die'] = None   # Don't recursively print entire DIE for seek'd DIEs.

            return ctxt

        def _lookup_type(param='type'):
            """
            Look up the 'DW_AT_type' attribute and resolve it to a PrgmType within the current
            CU Namespace..
            """
            # This attr value is offset relative to the compile unit, but it refers
            # to elements of our address-oriented lookup table which is global across
            # all addresses/offsets within the .dwarf_info.
            if ('DW_AT_' + param) not in die.attributes:
                return None  # No 'type' field for this DIE.

            addr = die.attributes['DW_AT_' + param].value + cu_offset

            if addr == die.offset:
                # Struct/class can refer to their own addr as containing_type. Do nothing.
                return None
            elif not cuns.has_addr_entry(addr):
                # We haven't processed this address yet; it's e.g. a forward reference.
                # We need to process that entry before returning a type to the caller of this method.
                sub_die = cu.get_DIE_from_refaddr(addr)
                debugger.verboseprint(f'** Seeking forward to process DIE at addr {sub_die.offset:04x}')
                self.parseTypesFromDIE(sub_die, cuns, _fresh_context())
                debugger.verboseprint('** End forward-seek process.')

            return cuns.entry_by_addr(addr)

        def _resolve_abstract_origin(attr='abstract_origin'):
            """
            Trace the abstract_origin property of this DIE back up to the root of the abstract_origin
            trail.
            """
            typ = _lookup_type(attr)
            return typ.getOrigin()

        def _add_entry(typ, name, addr):
            """
            Add entry to the compilation unit namespace.
            Only add by name if it's a top-level
            """
            typ.set_die(die)
            if nesting == 0:
                set_name = name
            else:
                set_name = None
            cuns.add_entry(typ, set_name, addr)

        def dieattr(name, default_value=None):
            """
                Look up an attribute within the current DIE; if not found, use default_value.
            """
            try:
                val = die.attributes['DW_AT_' + name].value
                if isinstance(val, bytes):
                    val = val.decode("utf-8")
                return val
            except KeyError:
                return default_value

        def hasattr(name):
            """
                Return true if DIE has attribute 'name'.
            """
            return ('DW_AT_' + name) in die.attributes


        def _get_locations(attr_name='location'):
            """
            Return location expression or a list of LocationEntry elements.
            """
            try:
                attr = die.attributes['DW_AT_' + attr_name]
                return locationlists.LocationParser(context['loc_lists']).parse_from_attribute(
                    attr, context['dwarf_ver'])
            except KeyError:
                return None


        ### In verbose mode, print the DIE tree as we parse it.
        if debugger.get_conf('dbg.verbose'):
            abs_origin = None
            if hasattr('abstract_origin'):
                abs_origin = _resolve_abstract_origin()
            if not abs_origin and hasattr('specification'):
                abs_origin = _resolve_abstract_origin('specification')
            debugger.verboseprint(
                dbg.VHEX4, die.offset, ':  ', nesting, '  ', nesting * '  ',
                die.tag, ': ', dieattr('name', None) or (abs_origin and abs_origin.name))

            if context['print_full_die'] is not None:
                # Dump the _entire_ DIE to stdout.
                debugger.verboseprint('')
                debugger.verboseprint(die)

        name = dieattr('name')

        if nesting == 0 and name and cuns.entry_by_name(name):
            # We're redefining a top-level type name or symbol that already exists.
            # Just copy the existing definition into this address.
            debugger.verboseprint('(Redefining existing ', name, '); copying existing')
            _add_entry(cuns.entry_by_name(name), None, die.offset)
            return


        ### Main switch-case for DW_TAG-specific parsing and interpretation.
        if die.tag == 'DW_TAG_base_type':
            # name, byte_size, encoding
            # This could be a true base/primitive type, or a typedef of a primitive type.
            # These may be repeated over multiple compilation units.
            #
            # If it has the same name as the pre-installed PrimitiveType for its encoding,
            # it's just the primitive type all over again.
            # If it has a different name and size, it's a fundamental C type we didn't already add.
            # If it has a different name and same size it's a typedef.
            size = dieattr('byte_size')
            prim = self._encodings[dieattr('encoding')]

            if name == prim.name and size == prim.size:
                # benign redundant definition.
                # register the common type object at this addr too.
                _add_entry(prim, None, die.offset)
            elif size == prim.size:
                _add_entry(AliasType(name, prim), name, die.offset)
            else:
                _add_entry(PrimitiveType(name, size), name, die.offset)

        elif die.tag == 'DW_TAG_const_type':
            base = _lookup_type() or _VOID
            const = ConstType(base)
            _add_entry(const, const.name, die.offset)
        elif die.tag == 'DW_TAG_volatile_type':
            # define 'volatile foo' as an alias to type foo.
            base = _lookup_type()
            _add_entry(base, 'volatile ' + base.name, die.offset)
        elif die.tag == 'DW_TAG_pointer_type':
            base = _lookup_type() or _VOID
            ptr = PointerType(base, self.addr_size)
            _add_entry(ptr, ptr.name, die.offset)
        elif die.tag == 'DW_TAG_reference_type':
            base = _lookup_type() or _VOID
            ref = ReferenceType(base, self.addr_size)
            _add_entry(ref, ref.name, die.offset)
        elif die.tag == 'DW_TAG_typedef':
            # name, type
            base = _lookup_type()
            _add_entry(AliasType(name, base), name, die.offset)
        elif die.tag == 'DW_TAG_array_type':
            # type
            base = _lookup_type()
            arr = ArrayType(base)
            _add_entry(arr, arr.name, die.offset)
            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['array'] = arr
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_subrange_type':  # Size of array
            # [lower_bound=0], upper_bound
            lower = dieattr("lower_bound", 0)
            upper = dieattr("upper_bound")
            if upper is None:
                # We may declare the presence of a const array of unknown size in a .h file
                # (`const some_t foo[];`) without giving its contents until definition in
                # some .cpp file. Length unknown for now.
                length = None
            else:
                length = upper - lower + 1
            context['array'].setLength(length)
        elif die.tag == 'DW_TAG_enumeration_type':
            # name, type, byte_size
            if name is None:
                name = dieattr('linkage_name', None)
            base = _lookup_type()
            enum = EnumType(name, base)
            _add_entry(enum, enum.name, die.offset)
            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['enum'] = enum
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_enumerator':  # Member of enumeration
            # name, const_value
            val = dieattr('const_value')
            context['enum'].addEnum(name, val)
        elif die.tag == 'DW_TAG_structure_type' or die.tag == 'DW_TAG_class_type':  # class or struct
            # name, byte_size, containing_type
            # TODO(aaron): can have 1+ DW_TAG_inheritance that duplicate or augment containing_type
            if name is None:
                name = dieattr('linkage_name', None)
            size = dieattr('byte_size')

            parent_type_offset = dieattr("containing_type", None)
            if parent_type_offset is None:
                parent_type = None
            else:
                parent_type = _lookup_type("containing_type")

            class_type = ClassType(name, size, parent_type)
            _add_entry(class_type, name, die.offset)
            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['class'] = class_type
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_union_type':
            if name is None:
                name = dieattr('linkage_name', None)
            size = dieattr('byte_size')
            parent_type_offset = dieattr("containing_type", None)
            if parent_type_offset is None:
                parent_type = None
            else:
                parent_type = _lookup_type("containing_type")

            union_type = UnionType(name, size, parent_type)
            _add_entry(union_type, name, die.offset)
            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['class'] = union_type
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_member':
            # name, type, data_member_location
            # accessibility (1=public, 2=protected, 3=private)
            # data_member_location is a multibyte sequence:
            # [23h, Xh] means 'at offset Xh' (DW_OP_plus_uconst)
            base = _lookup_type()
            if context['class'].is_union():
                # This is a member field of a union; no offset info.
                offset = None
                location_bytes = None
            else:
                data_member_location = dieattr('data_member_location')
                # Class member offsets may be integer constants representing offset from the
                # beginning of the class/struct.
                location_bytes = cuns.getLocationExprBytes(
                    locationlists.LocationExpr(data_member_location), {})

            if location_bytes is None:
                # No location available
                offset = None
            elif isinstance(location_bytes, int):
                # Just a plain integer offset.
                offset = location_bytes
            else:
                # ... But they may also be stack machine exprs that require full evaluation.
                # g++ for AVR seems to encode them all as DW_OP_plus_uconst [offset], but we've
                # got the ability to calculate more complicated patterns, so long as they don't
                # require access to current memory or registers here (which they shouldn't, as
                # part of a static type definition). The expr assumes the address of the object
                # is already on the expr stack to provide a true member address; we push '0'
                # here as a starting stack to get a member offset rather than a member address.
                #
                # nb evaluating for offset here means doing so without a $PC, so we're assuming
                # it's a single location expr and not a location_list. The latter _seems_
                # impossible for a field offset location to be PC-dependent, but maybe not?
                expr_machine = cuns.getExprMachine(
                    locationlists.LocationExpr(data_member_location), {})
                expr_machine.push(0)
                offset_list, flags = expr_machine.eval()
                if el.LookupFlags.successful(flags):
                    (offset, _) = offset_list[0]
                else:
                    cuns.getDebugger.verboseprint(
                        "Error decoding data member location for field ",
                        context.get("class").class_name, "::", name, " - ",
                        el.LookupFlags.get_message(flags))
                    offset = None

            accessibility = dieattr('accessibility', 1)
            field = FieldType(name, context.get("class"), base, offset, accessibility)
            context['class'].addField(field)
            _add_entry(field, None, die.offset)
        elif die.tag == 'DW_TAG_subprogram':
            # (Can be a function on its own, or a member method of a class)
            # name, [accessibility=1], [virtuality=0]
            # object_pointer <-- points to implicit 'this' formal arg.
            #
            # In addition to using subprogram to define a method type/signature, we use subprogram and
            # inlined_subroutine to resolve a $PC to the right compilation unit to understand the type
            # definitions relevant to the current stack frame/method.
            #
            # * A subprogram can have a low_pc -- high_pc range
            # * It can also have a `specification` that points to another subprogram.
            # * An inlined_subroutine can have a low_pc--high_pc range.
            #   It has an abstract_origin that points to a subprogram canonically defining it within a
            #   CU. You may need to recursively follow 'specification' from there to get the real CU.

            # 'name' itself is going to be a mangled name, which isn't super useful to the user.
            # Get this in demangled form.
            demangled = binutils.demangle(name, hide_params=True)
            if demangled:
                # 'demangled' may now be in the form '/[ClassName::]+methodName/'.
                # Trim that down to just 'methodName'.
                try:
                    last_namespace = demangled.rindex(':')
                    demangled = demangled[last_namespace + 1:]
                except ValueError:
                    # No ':' in string; nothing to do.
                    pass

                name = demangled  # Use demangled format for name.

            virtual = dieattr('virtuality', dwarf_constants.DW_VIRTUALITY_none)
            accessibility = dieattr('accessibility', dwarf_constants.DW_ACCESS_public)

            enclosing_class = context.get("class") or None
            if enclosing_class is None and hasattr('containing_type'):
                # A method body may be defined outside an enclosing DW_TAG_class_type,
                # which already has a declaration for this method. Confusingly, it may
                # lack an origin that points to that method declaration. Nonetheless, we
                # can still set the member_of field for the MethodInfo correctly, via
                # DW_AT_containing_type.
                enclosing_class = _lookup_type('containing_type')

            origin = None
            if hasattr('abstract_origin'):
                origin = _resolve_abstract_origin()
            elif hasattr('specification'):
                # This incomplete entry has the DW_AT_specification field, which is an offset from
                # cu_offset. The specification points to another incomplete declaration from
                # which we can populate data we need. (DWARFv5 2.13.2)
                origin = _resolve_abstract_origin('specification')

            return_type = _lookup_type() or _VOID

            if hasattr('declaration'):
                # If the DW_AT_declaration flag is provided, DWARFv5 says this is a declaration
                # and *not* the definition; don't bother with heuristics to set flags. (DWARFv5 2.13.1)
                is_decl = True
                is_def = False
            elif dieattr('low_pc') is None:
                # abstract instance of the method. Just the method signature, or else the abstract
                # instance of an inline method.
                is_decl = False
                is_def = False
            else:
                is_decl = origin is None  # If it has no abstract origin, it's also the declaration.
                is_def = True  # It has a PC range... concrete method definition.

            if hasattr('inline') and dieattr('inline') != dwarf_constants.DW_INL_inlined:
                # DWARFv5 3.3.8.1: This is an inline function but not actually an inline instance.
                # This is an 'abstract instance root' for the method.

                # This overrides the null low_pc => !is_def rule from earlier, since actual
                # DW_TAG_inlined_subroutines cannot be definitions.
                is_def = True

            if origin is not None:
                # The origin can populate fields we lack.
                if name is None:
                    name = origin.method_name
                if return_type is None or return_type == _VOID:
                    return_type = origin.return_type
                if enclosing_class is None:
                    enclosing_class = origin.member_of

            method = MethodInfo(
                name, return_type, cuns, enclosing_class, virtual, accessibility,
                is_decl, is_def, origin, die)

            if enclosing_class:
                enclosing_class.addMethod(method)
            else:
                # it's a standalone method in the CU
                cuns.addMethod(method)

            if dieattr('external') and not enclosing_class:
                # Also publish this method to the globals list in addition to the CUNS.
                self._global_syms.addMethod(method)

            _add_entry(method, None, die.offset)

            if dieattr('low_pc'):
                # has a PC range associated with it.
                low_pc = dieattr('low_pc')
                if 'DW_AT_high_pc' in die.attributes:
                    hi_pc_attr = die.attributes['DW_AT_high_pc']
                    if hi_pc_attr.form == 'DW_FORM_addr':
                        # It's an absolute address
                        hi_pc = hi_pc_attr.value
                    else:
                        # It's an offset from low_pc
                        hi_pc = low_pc + hi_pc_attr.value
                else:
                    hi_pc = None
                cuns.define_pc_range(low_pc, hi_pc, method, name)

            frame_base_loc = _get_locations('frame_base')
            if frame_base_loc is not None:
                method.setFrameBase(frame_base_loc)

            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['method'] = method
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)

        elif die.tag == 'DW_TAG_inlined_subroutine':
            # Defines a PC range associated with a subroutine inlined within another one.
            definition = _resolve_abstract_origin()
            if hasattr('specification') and definition is None:
                # This incomplete entry has the DW_AT_specification field, which is an offset from
                # cu_offset. The specification points to another incomplete declaration from
                # which we can populate data we need. (DWARFv5 2.13.2)
                definition = _resolve_abstract_origin('specification')

            name = definition.method_name or dieattr('name')  # try demangled name from def'n first
            return_type = definition.return_type or _lookup_type() or _VOID

            # inline instance of a method is neither declaration nor definition.
            is_decl = False
            is_def = False

            method = MethodInfo(
                name, return_type, cuns, definition.member_of, definition.virtual,
                definition.accessibility, is_decl, is_def, definition, die)


            if dieattr('low_pc') and dieattr('high_pc'):
                # has a PC range associated with it.
                low_pc = dieattr('low_pc')
                hi_pc_attr = die.attributes['DW_AT_high_pc']
                if hi_pc_attr.form == 'DW_FORM_addr':
                    # It's an absolute address
                    hi_pc = hi_pc_attr.value
                else:
                    # It's an offset from low_pc
                    hi_pc = low_pc + hi_pc_attr.value
                cuns.define_pc_range(low_pc, hi_pc, method, definition.name)
            elif dieattr('ranges'):
                # Some inlined methods have a DW_AT_entry_pc and a 'DW_AT_ranges' field.
                # Use multiple PCRanges to record this.
                range_lists = context['range_lists']
                if range_lists:
                    rangelist = range_lists.get_range_list_at_offset(dieattr('ranges'))
                    for r in rangelist:
                        cuns.define_pc_range(r.begin_offset, r.end_offset, method, definition.name)

            frame_base_loc = _get_locations('frame_base')
            if frame_base_loc is not None:
                method.setFrameBase(frame_base_loc)

            _add_entry(method, None, die.offset)

            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['method'] = method
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)

        elif die.tag == 'DW_TAG_lexical_block':
            # Lexical block defines a PCRange that can contain variables.
            origin = None
            if dieattr('abstract_origin'):
                origin = _resolve_abstract_origin()
            lexical_scope = LexicalScope(origin, context['method'])
            _add_entry(lexical_scope, None, die.offset)
            if dieattr('low_pc') and dieattr('high_pc'):
                low_pc = dieattr('low_pc')
                hi_pc_attr = die.attributes['DW_AT_high_pc']
                if hi_pc_attr.form == 'DW_FORM_addr':
                    # It's an absolute address
                    hi_pc = hi_pc_attr.value
                else:
                    # It's an offset from low_pc
                    hi_pc = low_pc + hi_pc_attr.value
                cuns.define_pc_range(low_pc, hi_pc, lexical_scope, None)

            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['method'] = lexical_scope
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_subroutine_type':
            # Used only for 'pointers to methods'. Establishes a type for a pointer to
            # a method with a specified return type & formal arg types.
            # This is used as a target for a TAG_pointer_type to a vtable entry.
            enclosing_class = context.get("class") or None
            return_type = _lookup_type() or _VOID
            method_type = MethodPtrType(name, self.addr_size, return_type, enclosing_class)
            _add_entry(method_type, name, die.offset)
            ctxt = context.copy()
            ctxt['nesting'] += 1
            ctxt['method'] = method_type
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, ctxt)
        elif die.tag == 'DW_TAG_ptr_to_member_type':
            # Used for pointers to member methods or fields of a class/struct.
            # Establishes a type for the pointer. This type may be named or anonymous.
            member_type = _lookup_type()
            class_type = _lookup_type('containing_type')
            member_ptr_type = PtrToMember(name, self.addr_size, member_type, class_type)
            _add_entry(member_ptr_type, name, die.offset)
        elif die.tag == 'DW_TAG_formal_parameter':
            # type signature for a formal arg to a method.
            # artificial=1 if added by compiler (e.g., implicit 'this')
            origin = None
            if dieattr('abstract_origin'):
                origin = _resolve_abstract_origin()

            base = _lookup_type()
            artificial = bool(dieattr('artificial', False))

            if origin is not None:
                if name is None:
                    name = origin.name
                if base is None:
                    base = origin.arg_type
                if not artificial:
                    artificial = origin.artificial

            location = _get_locations()
            const_val = dieattr('const_value')

            formal = FormalArg(name, base, cuns, origin, location, const_val, None, artificial)
            context['method'].addFormal(formal)
            _add_entry(formal, None, die.offset)
        elif die.tag == 'DW_TAG_variable':
            origin = None
            if dieattr('abstract_origin'):
                origin = _resolve_abstract_origin()
            elif dieattr('specification'):
                origin = _resolve_abstract_origin('specification')

            if name is None and origin is not None:
                name = origin.var_name
            base = _lookup_type()
            if base is None and origin is not None:
                base = origin.var_type
            location = _get_locations()
            is_decl = dieattr('declaration') and True
            is_def = not is_decl  # Variables are one or the other of decl and def.

            if context.get('method'):
                enclosing_scope = context['method']
            else:
                enclosing_scope = None

            # TODO(aaron): Check for DW_AT_data_location. And implement DW_OP_push_object_address.

            if name is None:
                # Nothing to actually define here... degenerate variable entry.
                # TODO(aaron): *why* do we see nameless variables? What attrs might give a clue?
                return

            var = VariableInfo(name, base, cuns, location, is_decl, is_def, origin, enclosing_scope)

            const_val = dieattr('const_value')
            if const_val is not None:
                # Hard-coded 'variable' value within this scope.
                var.setConstValue(const_val)

            if context.get('method'):
                # method or lexical block wrapped around this.
                context['method'].addVariable(var)
            else:
                # It's global in scope within the CU Namespace.
                cuns.addVariable(var)

            _add_entry(var, None, die.offset)

            if dieattr('external'):
                self._global_syms.addVariable(var)
        elif die.tag == "DW_TAG_dwarf_procedure":
            location = _get_locations()
            const_val = dieattr('const_value')

            if context.get('method'):
                enclosing_scope = context['method']
            else:
                enclosing_scope = None

            proc = DwarfProcedure(cuns, location, const_val, enclosing_scope)
            _add_entry(proc, None, die.offset)
        else:
            # TODO(aaron): Consider parsing DW_TAG_GNU_call_site
            for child in die.iter_children():
                self.parseTypesFromDIE(child, cuns, context)


    def parseTypeInfo(self, dwarf_info):
        range_lists = dwarf_info.range_lists()

        context = {}
        context['debugger'] = self._debugger
        context['int_size'] = self.int_size
        context['range_lists'] = range_lists
        context['loc_lists'] = dwarf_info.location_lists()
        context['nesting'] = 0
        context['print_full_die'] = None
        # TODO(aaron): If you add entries to context here, add to _default_context_keys.

        for compile_unit in dwarf_info.iter_CUs():
            context['dwarf_ver'] = compile_unit.header['version']
            self._debugger.verboseprint(f'Parsing compile unit (0x{compile_unit.cu_offset:04x})')

            cuns = CompilationUnitNamespace(
                compile_unit.cu_offset, compile_unit, range_lists,
                self._debugger)
            self._cu_namespaces.append(cuns)
            self.parseTypesFromDIE(compile_unit.get_top_DIE(), cuns, context)


# TODO(aaron): UnionType?
