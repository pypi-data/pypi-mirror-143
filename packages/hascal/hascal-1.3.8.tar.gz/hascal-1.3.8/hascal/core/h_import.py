from .h_lexer import Lexer
from .h_parser import Parser
from .h_error import HascalError, HascalWarning
from sys import platform
from os.path import isfile
from pathlib import Path

def use(gen_class,path_,BASE_DIR,filename=None):
    result = {}
    path = path_
    if type(path_) == str : 
        name = path_
        path = [path_]
    else : 
        name = '.'.join(name for name in path_)

    final_path = Path(BASE_DIR)  / "hlib"
    final_path_local = Path("")

    for x in path:
        final_path = final_path / x
        final_path_local = final_path_local / x

    final_path = str(final_path) + ".has"
    final_path_local = str(final_path_local) + ".has"

    if isfile(final_path) :
        with open(final_path,'r') as f :
            parser = Parser()
            tree = parser.parse(Lexer().tokenize(f.read()))
                                                
            generator = gen_class(BASE_DIR)
            output_cpp = generator.generate(tree,True)

            result['generator'] = generator
            result['output_cpp'] = output_cpp
            return result
    elif isfile(final_path_local):
        with open(final_path_local,'r') as f :
            parser = Parser()
            tree = parser.parse(Lexer().tokenize(f.read()))
                                                
            generator = gen_class(BASE_DIR)
            output_cpp = generator.generate(tree,True)

            result['generator'] = generator
            result['output_cpp'] = output_cpp
            return result
    else :
        HascalError(f"cannot found '{name}' library. Are you missing a library ?")


def cuse(gen_class,path_,BASE_DIR,filename=None):
    result = {}
    path = path_
    if type(path_) == str : 
        name = path_
        path = [path_]
    else : 
        name = '.'.join(name for name in path_)

    final_path = Path(BASE_DIR)  / "hlib"
    final_path_local = Path("")

    for x in path:
        final_path = final_path / x
        final_path_local = final_path_local / x

    final_path = str(final_path)
    final_path_local = str(final_path_local)
    
    final_path_h = final_path + ".hpp"
    final_path_cc = final_path + ".cc"
    final_path_ld = final_path + ".ld"
    # final_path_local_wld = final_path + ".wld"

    final_path_local_h = final_path_local + ".hpp"
    final_path_local_cc = final_path_local + ".cc"
    final_path_local_ld = final_path_local + ".ld"
    # final_path_local_wld = final_path_local + ".wld"

    if isfile(final_path_cc) :
        with open(final_path_cc, 'r') as fd:
            result["cpp_code"] = fd.read()
            
            # read header file
            if isfile(final_path_h):
                with open(final_path_h, 'r') as fd:
                    result["header_code"] = fd.read()
            else :
                result["header_code"] = ""
            
            if isfile(final_path_ld):
                with open(final_path_ld, 'r') as fd:
                    result["LDFLAGS"] = list(fd.read().split(','))
            else :
                result["LDFLAGS"] = []
            
        return result
    
    elif isfile(final_path_local_cc) :
        with open(final_path_local_cc, 'r') as fd:
            result["cpp_code"] = fd.read()
            
            # read header file
            if isfile(final_path_local_h):
                with open(final_path_local_h, 'r') as fd:
                    result["header_code"] = fd.read()
            else :
                result["header_code"] = ""

            if isfile(final_path_local_ld):
                with open(final_path_local_ld, 'r') as fd:
                    result["LDFLAGS"] = list(fd.read().split(','))
            else :
                result["LDFLAGS"] = []
            
        return result
    else :
        HascalError(f"cannot found '{name}' library. Are you missing a library ?")