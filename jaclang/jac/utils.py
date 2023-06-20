"""Utility functions and classes for Jac compilation toolchain."""
import re

import jaclang.jac.jac_ast as ast
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser


def get_all_jac_keywords() -> str:
    """Get all Jac keywords as an or string."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


if __name__ == "__main__":
    print(get_all_jac_keywords())


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string


def jac_file_to_ast(mod_path: str, base_path: str = None) -> ast.AstNode:
    """Convert a Jac file to an AST."""
    from jaclang.jac.passes.ast_build_pass import AstBuildPass
    from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa

    if base_path is None:
        base_path = ""
    lex = JacLexer()
    prse = JacParser()
    builder = AstBuildPass(mod_path=mod_path)
    prse.cur_file = mod_path
    ptree = prse.parse(
        lex.tokenize(open(base_path + mod_path).read()), filename=mod_path
    )
    return builder.run(node=ptoa(ptree))


def load_ast_and_print_pass_template() -> str:
    """Load and print classes."""
    import inspect
    import sys

    module_name = ast.__name__
    module = sys.modules[module_name]

    # Retrieve the source code of the module
    source_code = inspect.getsource(module)

    classes = inspect.getmembers(module, inspect.isclass)
    ast_node_classes = [cls for _, cls in classes if issubclass(cls, ast.AstNode)]

    ordered_classes = sorted(
        ast_node_classes, key=lambda cls: source_code.find(f"class {cls.__name__}")
    )
    output = ""
    for cls in ordered_classes:
        class_name = cls.__name__
        snake_case_name = pascal_to_snake(class_name)

        output += f"def exit_{snake_case_name}(self: 'PyCodeGenPass', node: ast.{class_name}) -> None:\n"
        output += '    """Sub objects.\n\n'

        init_func = cls.__init__
        init_signature = inspect.signature(init_func)

        for param_name, param in init_signature.parameters.items():
            if param_name not in ["self", "parent", "kid", "line"]:
                param_type = (
                    param.annotation
                    if param.annotation != inspect.Parameter.empty
                    else "Any"
                )
                param_default = (
                    param.default if param.default != inspect.Parameter.empty else None
                )
                output += f"    {param_name}: {param_type}{' ='+param_default if param_default else ''},\n"

        output += '    """\n\n'
    output = output.replace("jaclang.jac.jac_ast.", "")
    output = output.replace("typing.", "")
    output = output.replace("<enum '", "")
    output = output.replace("'>", "")
    output = output.replace("<class '", "")
    return output
