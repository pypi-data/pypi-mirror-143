from .h_error import HascalError, HascalWarning
from .h_lexer import Lexer
from .h_parser import Parser
from .h_import import use, cuse
import sys
from os.path import isfile
from pathlib import Path
import copy

HLIB_BASE_DIR = str(Path(__file__).parents[1])


class Generator(object):
      LDFLAGS = []
      def __init__(self,BASE_DIR):
            self.BASE_DIR = BASE_DIR
            self.src_includes = ""
            self.src_pre_main = ""
            #init standard types
            self.types = {
                  'int' : Type('int',True,category='number'),
                  'int8' : Type('int8',True,category='number'),
                  'int16' : Type('int16',True,category='number'),
                  'int32' : Type('int32',True,category='number'),
                  'int64' : Type('int64',True,category='number'),
                  'uint' : Type('uint',True,category='number'),
                  'uint8' : Type('uint8',True,category='number'),
                  'uint16' : Type('uint16',True,category='number'),
                  'uint32' : Type('uint32',True,category='number'),
                  'uint64' : Type('uint64',True,category='number'),


                  'float' : Type('float',True,category='number'),
                  'double' : Type('double',True,category='number'),

                  'bool' : Type('bool',True,category='number'),
                  'char' : Type('char',True,category='number'),
                  'string' : Type('string',True),
                  'void' : Type('void',True),
            }

            self.vars = { } # global vars
            self.consts = {
                  'NULL' : Const('NULL',Type('NULL',True,category='all-nullable'))
            } # global consts

            # functions
            self.funcs = {
                  'print' : Function('print',{'...':'...'},'void'),
                  'ReadStr' : Function('ReadStr',{},self.types['string']),
                  'ReadInt' : Function('ReadInt',{},self.types['int']),
                  'ReadFloat' : Function('ReadFloat',{},self.types['float']),
                  'ReadChar' : Function('ReadChar',{},self.types['char']),
                  'ReadBool' : Function('ReadBool',{},self.types['bool']),

                  'format' : Function('format',{'...':'...'},self.types['string']),
                  'split' : Function('split',{'str':'string','sep':'string'},self.types['string']),
                  'exit' : Function('exit',{'exit_code':'int'},self.types['void']),
                  'panic' : Function('panic',{'err_msg':'string'},self.types['string']),
                  'error' : Function('error',{'errmsg':'string'},self.types['void']),

                  'len' : Function('len',{'s':'string'},self.types['int']),
                  'len' : Function('len',{'vec':'T'},self.types['int']),
                  'append' : Function('append',{'vec':'T','val':'T'},self.types['int']),

                  'sizeof' : Function('sizeof',{'T':'T'},self.types['int']),
                  'typeof' : Function('typeof',{'T':'T'},self.types['string']),
            }

            # list of imported libraries
            self.imported = []

            # list of decorators
            self.decorators = {
                  'extern' : 'extern "C"',
                  'static' : 'static'
            }

            self.scope = False
      def generate(self, tree,use=False):
            _expr = self.walk(tree)
            result = ""
            for e in _expr :
                  result += e['expr']
            if use :
                  return f"\n{self.src_includes}\n{self.src_pre_main}\n{result}"
            else :
                  runtime = open(self.BASE_DIR+"/hlib/libcpp/std.cc").read()
                  runtime_h = open(self.BASE_DIR+"/hlib/libcpp/std.hpp").read()
                  return f"{runtime_h}\n{runtime}\n{self.src_includes}\n{self.src_pre_main}\n{result}\n"
      def get_flags(self):
            return self.LDFLAGS
      def exists(self,name):
            if name in self.funcs:
                  return True
            elif name in self.types :
                  return True
            elif name in self.vars :
                  return True
            if name in self.consts:
                  return True
            return False

      def add_to_output(self,cpp_code,hpp_code):
            self.src_includes += '\n' + hpp_code + '\n'
            self.src_pre_main += '\n' + cpp_code + '\n'

      def walk(self, node):
            # {
            #     <statements>
            # }
            if node[0] == 'block':
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  return result
            if node[0] == 'in_block':
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  return result
            if node[0] == 'block_struct':
                  current_vars = self.vars
                  self.vars = { }
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  self.vars = current_vars
                  return result
            #-------------------------------------            
            # var <name> = <expr>
            if node[0] == 'declare' and node[1] == "no_type":
                  _name = node[2]
                  _expr = self.walk(node[3])
                  _type = copy.deepcopy(_expr['type'])
                  _line = node[4]

                  if (_name in self.vars or _name in self.consts) and self.scope == False: 
                        HascalError(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type, cannot redefine it as a variable:{_line}")
                  elif _expr['type'].category == 'all-nullable' :
                        HascalError(f"Assign 'NULL' to non-typed variable '{_name}':{_line}")
                  else:
                        members = {}

                        if isinstance(_type,Struct) :
                              members = _type.members
                        self.vars[_name] = Var(_name,_type,members=members)
                        res = "auto %s = %s;\n" % (_name,_expr['expr'])
                        expr = {
                              'expr' : res,
                              'type' : _type,
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type>
            if node[0] == 'declare' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]

                  if (_name in self.vars or _name in self.consts) and self.scope == False :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_nullable(_type['type']) == False :
                        HascalError(f"The non-nullable variable '{_name}' must be initialized.\nTry adding an initializer expression:{_line}")
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct) : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)
                        res =  "%s %s ;\n" % (_type['expr'],_name)

                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type> = <expr>
            if node[0] == 'declare' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if (_name in self.vars or _name in self.consts) and self.scope == False  :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_nullable_compatible_type(_expr['type'],_type['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  elif is_compatible_type(_expr['type'],_type['type']) == False :
                        HascalError(f"Mismatched type {_type['type'].get_name_for_error()} and {_expr['type'].get_name_for_error()}:{_line}")
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct) : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)

                        expr = {
                              'expr' : "%s %s = %s;\n" % (_type['expr'],_name,_expr['expr']),
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr
                        
            # var <name> : [<return_type>]
            if node[0] == 'declare_array' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]

                  if (_name in self.vars or _name in self.consts) and self.scope == False :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")   
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")   
                  else:
                        self.vars[_name] = Var(_name,Array(_type['type']),is_array=True)
                        expr = {
                              'expr' : "std::vector<%s> %s;\n" % (_type['expr'],_name),
                              'type' : Array(_type['type']),
                              'name' : _name,
                        }
                        return expr

            # var <name> : [<return_type>] = <expr>
            if node[0] == 'declare_array' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if (_name in self.vars or _name in self.consts) and self.scope == False :
                        HascalError(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type, cannot redefine it as a variable:{_line}")
                  elif is_nullable_compatible_type(_expr['type'],_type['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  elif is_compatible_type(_expr['type'],Array(_type['type'])) == False :
                        HascalError(f"Mismatched type {Array(_type['type']).get_name_for_error()} and {_expr['type'].get_name_for_error()}:{_line}")    
                  else:
                        self.vars[_name] = Var(_name,Array(_type['type']),is_array=True)

                        expr = {
                              'expr' : "std::vector<%s> %s = %s ;\n" % (_type['expr'],_name,_expr['expr']),
                              'type' : Array(_type['type']),
                              'name' : _name,
                        }
                        return expr
            # const <name> : <return_type>
            if node[0] == 'declare' and node[1] == "const_no_expr":
                  _name = node[3]
                  _line = node[5]

                  HascalError(f"Uninitialized const '{_name}'")

            # const <name> : <return_type> = <expr>
            if node[0] == 'declare' and node[1] == "const":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if (_name in self.vars or _name in self.consts) and self.scope == False :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a constant:{_line}")
                  elif is_nullable_compatible_type(_expr['type'],_type['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable const '{_name}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  elif is_compatible_type(_expr['type'],_type['type']) == False :
                        HascalError(f"Mismatched type {_type['type'].get_name_for_error()} and {_expr['type'].get_name_for_error()}:{_line}") 
                  else:
                        self.consts[_name] = Const(_name,_type['type'])
                        expr = {
                              'expr' : "const %s %s = %s ;\n" % (_type,_name,_expr['expr']),
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type>*
            if node[0] == 'declare_ptr' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]
                  if (_name in self.vars or _name in self.consts) and self.scope == False :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_nullable(_type['type']) == False :
                        HascalError(f"The non-nullable variable '{_name}' must be initialized.\nTry adding an initializer expression:{_line}")
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct)  : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)
                        res =  "%s %s ;\n" % (_type['expr'],_name)

                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type>* = <expr>
            if node[0] == 'declare_ptr' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]
            
                  if (_name in self.vars or _name in self.consts) and self.scope == False  :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_nullable_compatible_type(_expr['type'],_type['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type']}' from NULL")
                  elif is_compatible_type(_expr['type'],_type['type']) == False :
                        HascalError(f"Mismatched type {_type['type'].get_name_for_error()} and {_expr['type'].get_name_for_error()}:{_line}") 
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct)  : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)

                        expr = {
                              'expr' : "%s %s = %s;\n" % (_type['type'],_name,_expr['expr']),
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr
            
            # var <name> = <expr>
            if node[0] == 'declare' and node[1] == "no_type":
                  _name = node[2]
                  _expr = self.walk(node[3])
                  _type = copy.deepcopy(_expr['type'])
                  _line = node[4]

                  if (_name in self.vars or _name in self.consts) and self.scope == False: 
                        HascalError(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type, cannot redefine it as a constant:{_line}")
                  elif _expr['type'].category == 'all-nullable' :
                        HascalError(f"Assign 'NULL' to non-typed variable '{_name}':{_line}")
                  else:
                        members = {}

                        if isinstance(_type,Struct) :
                              members = _type.members
                        self.vars[_name] = Const(_name,_type,members=members)
                        res = "auto %s = %s;\n" % (_name,_expr['expr'])
                        expr = {
                              'expr' : res,
                              'type' : _type,
                              'name' : _name,
                        }
                        return expr
            #-------------------------------------
            if node[0] == 'cuse':
                  _c_code = node[1]
                  return {
                        'expr' : _c_code+"\n",
                        'type' : '',
                        'cuse' : True,
                  }

            # cuse <lib_name>
            if node[0] == 'cinclude':
                  name = '.'.join(name for name in node[1])
                  if name not in self.imported :
                        result = cuse(Generator,node[1],self.BASE_DIR)

                        self.imported.append(name)
                        self.add_to_output(result['cpp_code'],result['header_code'])
                        self.LDFLAGS += result["LDFLAGS"]

                  return {'expr':'','type':''}
            #-------------------------------------
            # <name> = <expr>   
            if node[0] == 'assign':
                  _name = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if is_nullable_compatible_type(_name['type'],_expr['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name['expr']}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_name['type']}' from NULL")
                  elif is_compatible_type(_name['type'],_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type'].get_name_for_error()}' and '{_expr['type'].get_name_for_error()}':{_line}") 
                  elif _expr['type'].category == 'all-nullable':
                        HascalWarning(f"Assign 'NULL' to nullable variable '{_name['expr']}':{_line}")
                  expr = {
                        'expr' : '%s = %s;' % (_name['expr'],_expr['expr']),
                        'type' : _name['type']
                  }
                  return expr

            # <name>[<expr>] = <expr>;
            if node[0] == 'assign_var_index':
                  _name = self.walk(node[1])
                  _index = self.walk(node[2])
                  _expr = self.walk(node[3])
                  _line = node[4]

                  if not isinstance(_name['type'],Array) :
                        HascalError(f"'{_name['expr']}' is not subscriptable:{_line}")

                  if is_nullable_compatible_type(_name['type'].type_obj,_expr['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name['expr']}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False:
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  elif is_compatible_type(_name['type'].type_obj,_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type'].type_obj.get_name_for_error()}' and '{_expr['type'].get_name_for_error()}':{_line}") 
                  elif _expr['type'].category == 'all-nullable':
                        HascalWarning(f"Assign 'NULL' to nullable variable '{_name['expr']}':{_line}")
                  
                  expr = {
                        'expr' : '%s[%s] = %s;' % (_name['expr'],_index['expr'],_expr['expr']),
                        'type' : _name['type'].type_obj
                  }
                  return expr
            
            # <name>[<expr>].<name> = <expr>;
            if node[0] == 'assign_var_index_struct':
                  _name = self.walk(node[1])
                  _index = self.walk(node[2])
                  _field = node[3]
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if not isinstance(_name['type'],Array) :
                        HascalError(f"'{_name['expr']}' is not subscriptable:{_line}")
                  if not isinstance(_name['type'].type_obj,Struct) :
                        HascalError(f"'{_name['expr']}[{_index['expr']}]' is not a struct:{_line}")
                  if not _field in _name['type'].type_obj.members :
                        HascalError(f"'{_name['expr']}[{_index['expr']}]' has no field '{_field}':{_line}")
                  
                  if is_nullable_compatible_type(_name['type'].type_obj.members[_field],_expr['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name['expr']}[{_index['expr']}].{_field}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  elif is_compatible_type(_name['type'].type_obj.members[_field],_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type'].type_obj.members[_field].get_name_for_error()}' and '{_expr['type'].get_name_for_error()}':{_line}")
                  elif _expr['type'].category == 'all-nullable':
                        HascalWarning(f"Assign 'NULL' to nullable variable '{_name['expr']}':{_line}")
                  
                  expr = {
                        'expr' : '%s[%s].%s = %s;' % (_name['expr'],_index['expr'],_field,_expr['expr']),
                        'type' : _name['type'].type_obj.members[_field]
                  }
                  return expr
            
            # *<name> = <expr>
            if node[0] == 'assign_ptr' :
                  _name = self.walk(node[1])
                  _type = _name['type']
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if not _type.is_ptr :
                        HascalError(f"Invalid type argument of unary '^' (have '{_type['type'].get_name_for_error()}'):{_line}")
                  _type.is_ptr = False
                  _type.ptr_str = ''

                  if is_nullable_compatible_type(_type,_expr['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable '{_name['expr']}':{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type.get_name_for_error()}' from NULL")
                  elif is_compatible_type(_type,_expr['type']) == False :
                        HascalError(f"Mismatched type '{_type.get_name_for_error()}' and '{_expr['type'].get_name_for_error()}':{_line}")
                  elif _expr['type'].category == 'all-nullable':
                        HascalWarning(f"Assign 'NULL' to nullable variable '{_name['expr']}':{_line}")
                  
                  expr = {
                        'expr' : "*%s = %s;\n" % (_name['expr'],self.walk(node[2])['expr']),
                        'type' : _type,
                  }
                  return expr
            #-----------------------------------------
            # return <expr>
            if node[0] == 'return':
                  _expr = self.walk(node[1])
                  _line = node[2]

                  if _expr['expr'] in self.types :
                        HascalError(f"Cannot return a type '{_expr['expr']}':{_line}")
                  
                  expr = {
                        'expr' : "return %s;\n" %  _expr['expr'],
                        'type' : _expr['type'],
                        'return' : True
                  }
                  return expr 
            #-----------------------------------------
            # break
            if node[0] == 'break':
                  expr = {
                        'expr' : 'break;\n',
                        'type' : '',
                  }
                  return expr
            
            # continue
            if node[0] == 'continue':
                  expr = {
                        'expr' : 'continue;\n',
                        'type' : '',
                  }
                  return expr
            #-----------------------------------------
            # use <name>
            if node[0] == 'use':
                  name = '.'.join(name for name in node[1])
                  if name not in self.imported :
                        result = use(Generator,node[1],self.BASE_DIR)

                        self.imported.append(name)
                        self.imported += result['generator'].imported
                        self.add_to_output(result['output_cpp'],result['generator'].src_includes)
                        self.funcs.update(result['generator'].funcs)
                        self.types.update(result['generator'].types)
                        self.vars.update(result['generator'].vars)
                  return {'expr':'','type':''}
            
            # use <name>, <name>,...
            if node[0] == 'uses':
                  names = str(node[1])
                  names = names.replace("[","")
                  names = names.replace("]","")
                  names = names.replace("'","")
                  names = names.split(",")
                  for name in names :
                        if name in self.imported :
                              ...
                        else :
                              result = use(Generator,name,self.BASE_DIR)

                              self.imported.append(name)
                              self.imported += result['generator'].imported
                              self.add_to_output(result['output_cpp'],result['generator'].src_includes)
                              self.funcs.update(result['generator'].funcs)
                              self.types.update(result['generator'].types)
                              self.vars.update(result['generator'].vars)
                  return {'expr':'','type':''}
            #-----------------------------------------
            # function <name> {
            #     <block>
            # }
            # or :
            # function <name> : <return_type> {
            #     <block>
            # }

            # function <name>() {
            #     <block>
            # }
            # or :
            # function <name>() : <return_type> {
            #     <block>
            # }

            # function <name>(<args>) {
            #     <block>
            # }
            # or :
            # function <name>(<args>) : <return_type> {
            #     <block>
            # }
            if node[0] == 'function':
                  current_vars = self.vars.copy()
                  current_types = self.types.copy()
                  self.scope = True

                  _name = node[2]
                  _type = self.walk(node[1])
                  _return_type = _type['expr']
                  _line = node[5]
                  _decorator = self.walk(node[6])['expr']
                  _params = { }

                  params = self.walk(node[3])
                  params_type = params['type']
                  params_name = params['name']

                  if len(params) != 1:
                        for i in range(len(params_name)):
                              _params[params_name[i]] = params_type[i]
                              self.vars[params_name[i]] = Var(params_name[i],params_type[i])

                  if params['expr'].endswith(','):
                        params['expr'] = params['expr'][:-1]


                  if self.funcs.get(_name) != None:
                        if type(self.funcs[_name]) == Function:
                              self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_type['type'])]
                        else:
                              self.funcs[_name].append(Function(_name,_params,_type['type']))
                  else :
                        self.funcs[_name] = Function(_name,_params,_type['type'])

                  _name = node[2]
                  _expr = self.walk(node[4])
                  _res = ""

                  if _return_type != 'void' and len(_expr) < 1 :
                        HascalError(f"Function '{_name}' must return a value at end of function block:{_line}")
                  if _return_type != 'void' and len(_expr) != 0 and _expr[-1].get('return') != True :
                        HascalError(f"Function '{_name}' should return a value at end of function block:{_line}")
                  if _return_type != 'int' and _name == 'main':
                        HascalError(f"Function 'main' must return 'int'")
                  
                  for e in _expr :
                        _res += e['expr']
                  res = "%s %s %s(%s) {\n%s\n}\n" % (_decorator,_return_type,_name,params['expr'],_res) 

                  self.vars = current_vars
                  self.types = current_types
                  self.scope = False
                  
                  # program arguments 
                  _params_keys = list(_params.keys())
                  if len(params['name']) == 1 and (_name == "main" and isinstance(_params[_params_keys[0]],Array) and isinstance(_params[_params_keys[0]],Type) and _params[_params_keys[0]].type_obj.type_name == 'string'):
                        res = "%s %s %s(int argc,char** args) {\nstd::vector<std::string> %s;for(int i=0;i<argc;i++){%s.push_back(args[i]);}\n%s\n}\n" % (_decorator,_return_type,_name,_params_keys[0],_params_keys[0],_res) 
                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                        }
                        return expr
                  
                  if len(params['name']) > 1 and _name == "main" :
                        HascalError(f"Function 'main' takes only zero or one arguments(with string array type):{_line}")
                  if len(params['name']) == 1 and ((isinstance(_params[_params_keys[0]],Array) and isinstance(_params[_params_keys[0]].type_obj,Struct)) or isinstance(_params[_params_keys[0]],Struct)) and _name == "main" :
                        HascalError(f"Function 'main' takes only zero or one arguments(with struct type):{_line}")
                  if len(params['name']) == 1 and _name == "main" and isinstance(_params[_params_keys[0]],Array) and _params[_params_keys[0]].type_obj.type_name != 'string' :
                        HascalError(f"Function 'main' takes only zero or one arguments(with string array type):{_line}")
                  
                  expr = {
                        'expr' : res,
                        'type' : _type['type'],
                  }
                  return expr
            #-------------------------------------
            if node[0] == "inline_function" :
                  _name = node[2]
                  _type = self.walk(node[1])
                  _params = { }

                  params = self.walk(node[3])
                  params_type = params['type']
                  params_expr = params['expr']
                  params_name = params['name']
                        
                  if len(params) != 1:
                        for i in params_name :
                              for j in params_type :
                                    _params[i] = j   
                  
                  if self.funcs.get(_name) != None:
                        if type(self.funcs[_name]) == Function:
                              self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_type['type'])]
                        else:
                              self.funcs[_name].append(Function(_name,_params,_type['type']))
                  else :
                        self.funcs[_name] = Function(_name,_params,_type['type'])

                  return {'expr':'','type':'type'}
            #-------------------------------------
            # struct <name> {
            #     <block_struct>
            # }
            if node[0] == 'struct':
                  _name = node[1]
                  _members = { }
                  self.types[_name] = Struct(_name,_members)
                  _body = self.walk(node[2])
                  _line = node[3]
                  # generate output code and members
                  res = ""
                  for e in _body :
                        if str(e['type']) == _name :
                              HascalError(f"Incomplete type definition '{_name}':{_line}")
                        
                        if e.get('cuse') == None :
                              _members[e['name']] = e['type']

                        res += e['expr']
                  
                  # update nested structs
                  for member in _members :
                        if isinstance(_members[member],Struct) and _members[member].name == _name :
                              _members[member].members = self.types[_members[member].name].members
                  self.types[_name] = Struct(_name,_members)
                  
                  res = 'struct %s{\n%s\n};\n' % (_name,res)
                  # overload std::cout operator for current struct
                  res += 'std::ostream& operator<<(std::ostream& out,const %s& obj){\n' % _name
                  res += f'out << "{_name}(";\n'
                  
                  keys = list(_members.keys())
                  for i in range(len(_members)) :
                        res += 'out << "' + keys[i] + '" << ":" << obj.' + keys[i]
                        # check if last member
                        if i == len(keys)-1 :
                              res += ';\n'
                        else :
                              res += ' << ",";\n'
                  res += 'out << ")";\nreturn out;\n}\n'
                  expr = {
                        'expr' : res,
                        'type' : _name,
                  } 
                  return expr
            
            # struct <name> : <name> {
            #     <block_struct>
            # }
            if node[0] == 'struct_inheritance':
                  _name = node[1]
                  _i_name = node[2]
                  _line = node[4]
                  _members = { }
                  self.types[_name] = Struct(_name,_members)
                  _body = self.walk(node[3])

                  # get members from parent struct
                  if self.types.get(_i_name) != None:
                        _members = copy.deepcopy(self.types[_i_name].members)
                  else :
                        HascalError(f"Cannot found struct '{_i_name}'")

                  # generate output code and member
                  res = ""
                  for e in _body :
                        if str(e['type']) == _name :
                              HascalError(f"Incomplete type definition '{_name}':{_line}")
                        
                        if e.get('cuse') == None :
                              _members[e['name']] = e['type']

                        res += e['expr']
                        
                  self.types[_name] = Struct(_name,_members)
                  expr = {
                        'expr' : 'struct %s : %s{\n%s\n};\n' % (_name,_i_name,res),
                        'type' : _name,
                  } 
                  return expr
            #-------------------------------------
            # enum <name> {
            #     <enum_names>
            # }
            if node[0] == 'enum':
                  _name = node[1]
                  _members = node[2].split(',')

                  if _name in self.types:
                        HascalError(f"Redefinition of type '{_name}'")
                  if _name in self.vars:
                        HascalError(f"Redefinition of variable '{_name}'")
                  if _name in self.funcs:
                        HascalError(f"Redefinition of function '{_name}'")

                  members = {}
                  for i in range(len(_members)-1):
                        members[str(_members[i])] = copy.deepcopy(self.types['int'])
                  
                  self.types[_name] = Enum(_name,members)
                  expr = {
                        'expr' : 'enum %s{\n%s\n};\n' % (_name,node[2]),
                        'type' : copy.deepcopy(self.types[_name]),
                  } 
                  return expr
            #-------------------------------------
            # if <condition> {
            #     <block>
            # }   

            # or : 

            # if <condition> {
            #     <block>
            # }else {
            #     <block>
            # }

            # or :

            # if <condition> {
            #     <block>
            # }else if <condition> {
            #     <block>
            # }
            if node[0] == 'if':
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])

                  res = ""
                  for e in body :
                        res += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}\n' % (cond['expr'],res),
                        'type' : '',
                  }
                  return expr
            if node[0] == 'if_else':
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  body2 = self.walk(node[3])

                  res = ""
                  for e in body :
                        res += e['expr']
                  res2 = ""
                  for e in body2 :
                        res2 += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}else {\n%s\n}\n' % (cond['expr'],res,res2),
                        'type' : '',
                  }
                  return expr
            if node[0] == 'if_else2':
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  body2 = self.walk(node[3])
                  res = ""
                  for e in body :
                        res += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}else %s\n' % (cond['expr'],res,body2['expr']),
                        'type' : '',
                  }
                  return expr
            #------------------------------------
            # for <name> in <name> {
            #     <block>
            # }
            if node[0] == 'for':      
                  _name = node[1]
                  _name2 = node[2][0]
                  _line = node[4]
                  res = ""
                  current_vars = self.vars.copy()

                  if not (_name2 in self.vars or _name2 in self.consts) :
                        HascalError(f"'{_name2}' not defined:{_line}")

                  if not isinstance(self.vars[_name2].type,Array) :
                        HascalError(f"'{_name2}' is not iterable:{_line}") 

                  self.vars[_name] = Var(_name,self.vars[_name2].type.type_obj)
                  body = self.walk(node[3])
                  for e in body :
                        res += e['expr']
                  self.vars = current_vars
                  expr = {
                        'expr' : 'for(auto %s : %s){\n%s\n}\n' % (_name,_name2,res),
                        'type' : '',
                  }
                  return expr
            #--------------------------------------
            # while <condition> {
            #     <block>
            # }
            if node[0] == 'while':      
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  res = ""
                  for e in body :
                        res += e['expr']
                  expr = {
                        'expr' : 'while(%s){\n%s\n}\n' % (cond['expr'],res),
                        'type' : '',
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'new' :
                  _type = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if is_nullable_compatible_type(_type['type'],_expr['type']) == False:
                        HascalError(f"Assign 'NULL' to non-nullable variable:{_line}")
                  elif _expr['type'].category == 'all-nullable' and _name['type'].is_ptr == False :
                        HascalError(f"Converting to non-pointer type '{_type['type'].get_name_for_error()}' from NULL")
                  if is_compatible_type(_type['type'],_expr['type']) == False:
                        HascalError(f"Mismatched type '{_type['type'].get_name_for_error()}' and '{_expr['type'].get_name_for_error()}' in 'new' expression:{_line}")
                  
                  _type['type'].is_ptr = True
                  _type['type'].ptr_str += '*'

                  expr = {
                        'expr' : 'new %s(%s)' % (_type['expr'],_expr['expr']),
                        'type' : _type['type'],
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'delete' :
                  _name = node[1]
                  _line = node[2]

                  if not _name in self.vars :
                        HascalError(f"'{_name}' not defined:{_line}")
                  
                  if self.vars[_name].type.is_ptr == False :
                        HascalError(f"'{_name}' is not a pointer:{_line}")
                  
                  expr = {
                        'expr' : 'delete %s;\n' % (_name),
                        'type' : copy.deepcopy(self.vars[_name].type),
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'cast' :
                  _return_type = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  expr = {
                        'expr' : 'static_cast<%s>(%s)' % (_return_type['type'],_expr['expr']),
                        'type' : _return_type['type'],
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'pass_by_ptr' :
                  _name = self.walk(node[1])
                  _type = copy.deepcopy(_name['type'])
                  _line = node[2]
                  
                  if not _type.is_ptr :
                        HascalError(f"Invalid type argument of unary '^' (have '{_type}'):{_line}")
                  
                  
                  _type.is_ptr = False
                  _type.ptr_str = ''

                  expr = {
                        'expr' : '*%s' % (_name['expr']),
                        'type' : _type,
                  }
                  return expr
            
            if node[0] == 'pass_by_ref' :
                  _name = self.walk(node[1])
                  _type = _name['type']
                  _line = node[2]

                  type_ = None
                  if isinstance(_type,Struct) :
                        type_ = Struct(_type.name,_type.members,is_ptr=True,ptr_str='&',category=_type.category)
                  else :
                        type_ = Type(_type.type_name,_type.stdtype,is_ptr=True,ptr_str='*',category=_type.category)
                  
                  expr = {
                        'expr' : '&%s' % (_name['expr']),
                        'type' : type_,
                  }
                  return expr
            #---------------------------------------
            # <expr>                   
            if node[0] == 'expr':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : "%s;\n" % (_expr['expr']),
                        'type' : _expr['type'],
                  }
                  return expr
            #---------------------------------------
            # <expr>(<params>)
            if node[0] == 'call':
                  _name = node[1]
                  _line = node[3]
                  _args = [self.walk(_arg) for _arg in node[2]]
                  if self.exists(_name):
                        if _name == "print":
                              expr = {
                                    'expr' : 'std::cout << %s << std::endl' % ('<< '.join(self.walk(arg)['expr'] for arg in node[2])),
                                    'type' : self.funcs['print'].return_type,
                              }
                              return expr
                        else :
                              if isinstance(self.funcs.get(_name),list):
                                    _f_params = {}
                                    for f in self.funcs[_name]:
                                          _f_params[f.name] = f.params
                                    
                                    counter = 0
                                    while counter < len(self.funcs[_name]):
                                          f = self.funcs[_name][counter]

                                          if len(f.params) != len(node[2]):
                                                # check if there is at end of list
                                                if counter == len(self.funcs[_name]) - 1:
                                                      if len(f.params) > len(node[2]):
                                                            HascalError(f"{_name} has more parameters than given:{_line}")
                                                      else :
                                                            HascalError(f"{_name} has less parameters than given:{_line}")
                                                else :
                                                      counter += 1
                                                      continue
                                          else :
                                                _return_type = f.return_type

                                                # check if return type is pointer
                                                if isinstance(_return_type,Type) and _return_type.is_ptr:
                                                      _return_type = Type(_return_type.type_name,_return_type.stdtype,is_ptr=True,ptr_str=_return_type.ptr_str,category=_return_type.category)
                                                
                                                expr = {
                                                      'expr' : '%s(%s)' % (f.name,','.join(self.walk(arg)['expr'] for arg in node[2])),
                                                      'type' : _return_type,
                                                }
                                                return expr
                                          counter += 1
                              if _name in self.types:
                                    if not isinstance(self.types[_name],Struct):
                                          HascalError(f"Cannot call type {_name}:{_line}")
                                    
                                    expr = {
                                          'expr' : "%s{%s}" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : copy.deepcopy(self.types[_name],)
                                    }
                                    return expr
                              else :
                                    _return_type = self.funcs[_name].return_type

                                    # check if return type is pointer
                                    if isinstance(_return_type,Type) and _return_type.is_ptr:
                                          _return_type = Type(_return_type.type_name,_return_type.stdtype,is_ptr=True,ptr_str=_return_type.ptr_str,category=_return_type.category)
                                                
                                    expr = {
                                          'expr' : "%s(%s)" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : _return_type,
                                    }
                                    return expr
                  else :
                        HascalError(f"Function '{_name}' not defined:{_line}")
            if node[0] == 'call_stmt' :
                  _expr = self.walk(node[1])
                  _expr['expr'] += ';\n'
                  return _expr
            # --------------operators-----------------
            # <expr> + <expr>
            if node[0] == 'add':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if (_expr0['type'].category == 'all-nullable' or _expr1['type'].category == 'all-nullable') and (_expr0['type'].is_ptr != True or _expr0['type'].is_ptr != True) :
                        HascalError(f"'NULL' used in arithmetic:{_line}")
                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                        
                  expr = {
                        'expr' : '%s + %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr

            # <expr> - <expr>
            if node[0] == 'sub':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  
                  if (_expr0['type'].category == 'all-nullable' or _expr1['type'].category == 'all-nullable') and (_expr0['type'].is_ptr != True or _expr0['type'].is_ptr != True) :
                        HascalError(f"'NULL' used in arithmetic:{_line}")
                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")  
                  if _expr0['type'].category != 'number' or _expr1['type'].category != 'number':
                        HascalError(f"Cannot subtract {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  
                  expr = {
                        'expr' : '%s - %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr

            # <expr> * <expr>
            if node[0] == 'mul':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if (_expr0['type'].category == 'all-nullable' or _expr1['type'].category == 'all-nullable') and (_expr0['type'].is_ptr != True or _expr0['type'].is_ptr != True):
                        HascalError(f"'NULL' used in arithmetic:{_line}")
                  
                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}") 

                  if _expr0['type'].category != 'number' or _expr1['type'].category != 'number':
                        HascalError(f"Cannot multiply non-number type:{_line}")
                  
                  expr = {
                        'expr' : '%s * %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr

            # <expr> / <expr>
            if node[0] == 'div':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if (_expr0['type'].category == 'all-nullable' or _expr1['type'].category == 'all-nullable') and (_expr0['type'].is_ptr != True or _expr0['type'].is_ptr != True):
                        HascalError(f"'NULL' used in arithmetic:{_line}")
                  
                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  
                  if _expr0['type'].category != 'number' or _expr1['type'].category != 'number':
                        HascalError(f"Cannot divide non-number type:{_line}")
                  
                  else :
                        expr = {
                              'expr' : '%s / %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # (<expr>)
            if node[0] == 'paren_expr':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '(%s)' % (_expr['expr']),
                        'type' : _expr['type'] 
                  }
                  return expr
            
            # --------------end of operators-----------------  

            # ---------------conditions---------------------
            # <condition>
            if node[0] == 'cond':
                  _expr0 = self.walk(node[1])

                  expr = {
                        'expr' : '%s' % (_expr0['expr']),
                        'type' : copy.deepcopy(self.types['bool']) 
                  }
                  return expr

            # not <condition>
            if node[0] == 'not':
                  _expr0 = self.walk(node[1])

                  expr = {
                        'expr' : '!%s' % (_expr0['expr']), # may have bug
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr

            # <condition> and <condition>
            if node[0] == 'and':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  expr = {
                        'expr' : '%s && %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr

            # <condition> or <condition>
            if node[0] == 'or':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  expr = {
                        'expr' : '%s || %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr

            # <expr> == <expr>
            if node[0] == 'equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if is_nullable_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"'NULL' used in arithmetic:{_line}")
                  elif is_nullable_compatible_type(_expr0['type'],_expr1['type']) == False and is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  else :
                        expr = {
                              'expr' : '%s == %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr

            # <expr> != <expr>
            if node[0] == 'not_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s != %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr

            # <expr> >= <expr>
            if node[0] == 'greater_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s >= %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr

            # <expr> <= <expr>
            if node[0] == 'less_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s <= %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr
            
            # <expr> > <expr>
            if node[0] == 'greater':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s > %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr

            # <expr> < <expr>
            if node[0] == 'less':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  
                  if is_compatible_type(_expr0['type'],_expr1['type']) == False:
                        HascalError(f"Mismatched type {_expr0['type'].get_name_for_error()} and {_expr1['type'].get_name_for_error()}:{_line}")
                  # todo : check if type is int or bool else error    
                  else :
                        expr = {
                              'expr' : '%s < %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : copy.deepcopy(self.types['bool'])
                        }
                        return expr

            # not <expr>
            if node[0] == 'not_cond':
                  _expr0 = self.walk(node[1])
                  expr = {
                        'expr' : '!%s' % (_expr0['expr']), # may have bug
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr

            # true / false
            if node[0] == 'bool_cond':
                  expr = {
                        'expr' : '%s' % (node[1]),
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr
            
            # <expr>
            if node[0] == 'expr_cond':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '%s' % (_expr['expr']), # may have bug
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr
            
            # <expr>
            if node[0] == 'paren_cond':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '(%s)' % (_expr['expr']), # may have bug
                        'type' : copy.deepcopy(self.types['bool'])
                  }
                  return expr
            # ---------------end of conditions---------------------    
            # <name>
            if node[0] == 'var':
                  _name = node[1][0]
                  _line = node[2]
                  if len(node[1]) == 1:
                        if _name in self.vars:
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : self.vars[_name].type,
                                    'obj' : self.vars[_name]
                              }
                              return expr
                        elif _name in self.consts :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : self.consts[_name].type,
                                    'obj' : self.consts[_name]
                              }
                              return expr
                        elif _name in self.types :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : copy.deepcopy(self.types[_name]),
                                    'obj' : copy.deepcopy(self.types[_name])
                              }
                              return expr
                        elif _name in self.funcs :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : '', # todo : return function
                                    'obj' : self.funcs[_name]
                              }
                              return expr
                        else :
                              HascalError(f"'{_name}' is not reachable or not defined:{_line}")
                  else :
                        _full_name = ''
                  
                        if _name in self.vars:
                              if self.vars[_name].type.is_ptr :
                                    _full_name += _name + '->'
                              else :
                                    _full_name += _name + '.'
                              
                              if isinstance(self.vars[_name].type,Struct) :
                                    # if struct has no member show error else set current member to _current_member
                                    if self.vars[_name].type.members == {} :
                                          HascalError(f"Struct '{_name}' have not any members:{_line}")
                                    _members = copy.deepcopy(self.vars[_name].type.members)

                                    _back_member_name = _name
                                    _back_member_type = copy.deepcopy(self.vars[_name].type)

                                    for i in range(len(node[1])):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]

                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalError(f"Struct '{_name}' have not any members:{_line}")

                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            _full_name += _current_member
                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      if _members[_current_member].is_ptr :
                                                            _full_name += _current_member + '->'
                                                      else :
                                                            _full_name += _current_member + '.'
                                                      
                                                      _members = _members[_current_member].members
                                                      continue
                                                      
                                                else :
                                                      if not _current_member in _members :
                                                            HascalError(f"Struct '{node[1][i-1]}' has no member named '{_current_member}':{_line}")

                                                      _full_name += _current_member
                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 :    
                                                continue
                                          else :
                                                HascalError(f"Struct '{node[1][i-1]}' has no member named '{_current_member}':{_line}")  

                              elif str(self.vars[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s" % (_full_name),
                                          'type' : copy.deepcopy(self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]]),
                                    }
                                    return expr  
                              expr = {
                                    'expr' : "%s" % (_full_name),
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                        elif _name in self.consts :
                              if isinstance(self.types[str(self.vars[_name].type)],Struct) :
                                    # if struct has no member show error else set current member to _current_member
                                    if self.types[self.consts[_name].type].members == {} :
                                          HascalError(f"Struct '{_name}' has no member:{_line}")
                                    _members = copy.deepcopy(self.types[self.consts[_name].type]).members

                                    for i in range(len(node[1])-1):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]
                                          
                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalError(f"Struct '{_name}' has no member:{_line}")
                                                
                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            # check if current member is an vector
                                                            if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalError(f"Struct '{_name}' has no member:{_line}")

                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      _members = _members[_current_member].members
                                                      continue
                                                else :
                                                      if not _current_member in _members :
                                                            HascalError(f"Struct '{_name}' has no member:{_line}")
                                                      if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalError(f"Struct '{_name}' has no member:{_line}")

                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 : ...
                                          else :
                                                HascalError(f"'{node[1][i]}' is not a member of '{_name}':{_line}")  

                              if str(self.consts[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s" % (_name),
                                          'type' : copy.deepcopy(self.types[str(self.consts[_name].type).split('<')[1].split('>')[0]]),
                                    }
                                    return expr  

                              expr = {
                                    'expr' : "%s" % (_full_name),
                                    'type' : self.consts[_name].type,
                              }
                              return expr
                                                      
                        elif _name in self.types and isinstance(self.types[_name],Enum):
                              name = node[1]
                              name.pop(0)
                              if len(name) > 1 :
                                    HascalError(f"Request for nested enum in '{_name}' :{_line}")
                                    
                              if not name[0] in self.types[_name].members :
                                    HascalError(f"Enum '{_name}' has no member named '{name[0]}':{_line}")
                                          
                              expr = {
                                    'expr' : "%s" % (name[0]),
                                    'type' : copy.deepcopy(self.types[_name]),
                              }
                              return expr
                        else :
                              HascalError(f"'{_name}' is not reachable or not defined:{_line}")                             
            #---------------------------------------
            # <name>[<expr>]
            if node[0] == 'var_index':
                  _name = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if isinstance(_name['type'],Array) :
                        expr = {
                              'expr' : "%s[%s]" % (_name['expr'],_expr['expr']),
                              'type' : _name['type'].type_obj,
                        }
                        return expr
                  elif str(_name['type']) == 'string' :
                        expr = {
                              'expr' : "%s[%s]" % (_name['expr'],_expr['expr']),
                              'type' : copy.deepcopy(self.types['char']),
                        }
                        return expr
                  else :
                        HascalError(f"'{_name['expr']}' is not subscriptable:{_line}")
            #-------------------------------------------
            # <expr>, <expr>
            if node[0] == 'exprs':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                        
                  expr = {
                        'expr' : '%s,%s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr
            # [<expr>]
            if node[0] == 'list':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '{%s}' % (_expr['expr']),
                        'type' : Array(_expr['type']),
                  }
                  return expr
            #-------------------------------------------
            # <expr>.<name>
            if node[0] == '.':
                  _expr = self.walk(node[1])
                  _name = node[2]

                  expr = {
                        'expr' : '%s.%s' % (_expr['expr'],_name),
                        'type' : _expr['type'], # todo : return _name type
                  }
                  return expr
            # <expr>.<name>
            if node[0] == '.2':
                  # todo : name type and index type check
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[3])
                  _name = node[2]

                  expr = {
                        'expr' : '%s.%s[%s]' % (_expr0['expr'],_name,_expr1['expr']),
                        'type' : _expr['type'], # todo : return _name type
                  }
                  return expr
            #--------------------------------------------
            # <return_type>
            if node[0] == 'return_type':
                  _type_name = node[1]
                  _line = node[2]

                  if not _type_name in self.types:
                        HascalError(f"{_type_name} is not defined:{_line}")
                  
                  expr = {
                        'expr' : _type_name,
                        'type' : copy.deepcopy(self.types[_type_name]),
                        'name' : _type_name,
                  }
                  return expr
            
            # [<return_type>]
            if node[0] == 'return_type_array':
                  _type = self.walk(node[1])
                  _line = node[2]
                  
                  expr = {
                        'expr' : 'std::vector<%s>' % (_type['expr']),
                        'type' : Array(_type['type']),
                        'name' : _type['name'],
                  }
                  return expr
            
            # <return_type>^
            if node[0] == 'ptr_type':
                  _type = self.walk(node[1])
                  _line = node[2]

                  if isinstance(_type['type'],Struct):
                        expr = {
                              'expr' : "%s*" % (_type['expr']),
                              'type' : Struct(_type['type'].name,_type['type'].members,is_ptr=True,ptr_str='*',category=_type['type'].category),
                              'name' : _type['name'],
                        }
                        return expr
                  expr = {
                        'expr' : "%s*" % (_type['expr']),
                        'type' : Type(_type['type'].type_name,_type['type'].stdtype,is_ptr=True,ptr_str='*',category=_type['type'].category),
                        'name' : _type['name'],
                  }
                  return expr
            
            # <return_type>?
            if node[0] == 'nullable_type':
                  _type = self.walk(node[1])
                  _line = node[2]
                  _type['type'].nullable = True

                  expr = {
                        'expr' : "%s" % (_type['expr']),
                        'type' : _type['type'],
                        'name' : _type['name'],
                  }
                  return expr

            #--------------------------------------------
            if node[0] == 'param_no' :
                  expr = {
                        'expr' : '',
                        'type' : [],
                        'name' : [],
                  }
                  return expr
            
            if node[0] == 'param' :
                  _name = node[1]
                  _return_type = self.walk(node[2])
                  _type = _return_type['expr']
                  _type_name = _return_type['name']
                  _line = node[3]
                  
                  expr = {
                        'expr' : '%s %s,' % (_type,_name),
                        'type' : _return_type['type'],
                        'name' : _name,
                  }
                  return expr
            
            if node[0] == 'params' :
                  _params = self.walk(node[1])
                  _param = self.walk(node[2])

                  expr = {
                        'expr' : '%s %s' % (_params['expr'],_param['expr']),
                        'type' : _params['type'] + [_param['type']],
                        'name' : _params['name'] + [_param['name']],
                  }
                  return expr
            #--------------------------------------------
            if node[0] == 'decorator' :
                  _name = node[1]
                  _line = node[2]

                  if not _name in self.decorators:
                        HascalError(f"{_name} is not defined:{_line}")
                  
                  expr = {
                        'expr' : self.decorators[_name] + " ",
                        'type' : copy.deepcopy(self.types['void']),
                  }
                  return expr
            
            if node[0] == 'decorator_no' :
                  expr = {
                        'expr' : '',
                        'type' : self.types['void'],
                  }
                  return expr
            #--------------------------------------------
            if node[0] == 'string':
                  expr = {
                        'expr' : 'std::string("%s")' % node[1],
                        'type' : copy.deepcopy(self.types[node[0]]),
                  }
                  return expr
            if node[0] == "multiline_string" :
                  expr = {
                        'expr' : 'std::string(R"(%s)")' % node[1],
                        'type' : copy.deepcopy(self.types['string']),
                  }
                  return expr
            if node[0] == 'bool' or node[0] == 'float' or node[0] == 'int':
                  expr = {
                        'expr' : '%s' % node[1],
                        'type' : copy.deepcopy(self.types[node[0]]),
                  }
                  return expr

            if node[0] == 'char':
                  expr = {
                        'expr' : '\'%s\'' % node[1],
                        'type' : copy.deepcopy(self.types[node[0]]),
                  }
                  return expr         

class Var(object):
      def __init__(self,name,type,is_array=False,members={},nullable=False):
            self.name = name
            self.type = type
            self.is_array = is_array
            self.members = members
            self.nullable = nullable

class Const(Var):
      ...

class Function(object):
      def __init__(self,name,params,return_type):
            self.name = name
            self.params = params # type : dict
            self.return_type = return_type

class Struct(object):
      def __init__(self,name,members,category='',is_ptr=False,ptr_str='',nullable=False):
            self.name = name
            self.members = members
            self.stdtype = False
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            self.category = name
            self.nullable = nullable
      
      def __str__(self):
            return self.get_type_name()

      def get_type_name(self):
            return self.name + self.ptr_str
class Enum(Struct):
      ...

class Type(object):
      def __init__(self,type_name,stdtype,category='',is_ptr=False,ptr_str='',nullable=False):
            self.type_name = type_name
            self.stdtype = stdtype
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            self.category = category
            self.nullable = nullable
      
      def __str__(self):
            return self.get_type_name()

      def get_type_name(self):
            if self.is_ptr:
                  return '%s%s' % (self.type_name,self.ptr_str)
            else :
                  return self.type_name + self.ptr_str
      
      def get_name_for_error(self):
            ptr_str = self.ptr_str.replace("*","^")

            if self.is_ptr:
                  return '%s%s' % (self.type_name,ptr_str)
            else :
                  return self.type_name + ptr_str
class Array(Type):
      def __init__(self,type_obj,is_ptr=False,ptr_str=''):
            self.type_obj = type_obj
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            if isinstance(type_obj,Type):
                  super().__init__(type_obj.type_name,type_obj.stdtype)
            elif isinstance(type_obj,Struct):
                  super().__init__(type_obj.name,type_obj.members)            
      
      def __str__(self):
            if isinstance(self.type_obj,Type):
                  return "std::vector<%s>%s" % (self.ptr_str,self.get_type_name())
            elif isinstance(self.type_obj,Struct):
                  return "std::vector<%s>%s" % (str(self.type_obj),self.ptr_str)
      def get_name_for_error(self):
            ptr_str = self.ptr_str.replace("*","^")

            if isinstance(self.type_obj,Type):
                  return "[%s]%s" % (self.ptr_str,self.get_type_name())
            elif isinstance(self.type_obj,Struct):
                  return "[%s]%s" % (str(self.type_obj),self.ptr_str)
def is_compatible_ptr(type_a,type_b):
      if type_a.is_ptr == type_b.is_ptr:
            return True
      else:
            return False


def is_compatible_type(type_a,type_b):    
      if type_a == type_b:
            return True
      if is_nullable_compatible_type(type_a,type_b):
            return True

      if isinstance(type_a,Type) and isinstance(type_b,Type):
            if str(type_a.category) == str(type_b.category) and is_compatible_ptr(type_a,type_b):
                  return True
            else :
                  return False
      
      if isinstance(type_a,Struct) and isinstance(type_b,Struct):
            if str(type_a.category) == str(type_b.category) and is_compatible_ptr(type_a,type_b):
                  return True
            else :
                  return False

      return False

def is_nullable(type_obj):
      if type_obj.nullable == True :
            return True
      return False

def is_nullable_compatible_type(type_a,type_b):
      if (is_nullable(type_a) == True and type_b.category == 'all-nullable') or (is_nullable(type_b) == True and type_a.category == 'all-nullable'):
            return True
      if (is_nullable(type_a) == False and type_b.category == 'all-nullable') or (is_nullable(type_b) == False and type_a.category == 'all-nullable'):
            return False
      
      return True