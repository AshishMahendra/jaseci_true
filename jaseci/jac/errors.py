"""Error handling for Jac."""
import sys
from typing import TypeVar

from jaseci.utils.sly.yacc import YaccProduction

_ = None  # For flake8 linting
JacParser = TypeVar("JacParser")


class JacParseErrorMixIn:
    """Error handling for Jac Parse Errors."""

    def __init__(self: "JacParseErrorMixIn") -> None:
        """Initialize Jac Parse Error Mixin."""
        super().__init__()
        self.had_error = False

    def error(self: "JacParseErrorMixIn", p: YaccProduction) -> None:
        """Panic mode skip forward skip."""
        self.had_error = True
        super().error(p)
        print("Whoa. You are seriously hosed.")
        if not p:
            print("End of File!")
            return

        # Read ahead looking for a closing '}'
        while True:
            tok = next(self.tokens, None)
            if not tok or tok.type == "RBRACE":
                break
        self.restart()

    def error_out(self: "JacParseErrorMixIn", msg: str) -> None:
        """Error out."""
        sys.stderr.write("Jac Parse Error" + msg)

    @_(
        "KW_GLOBAL global_var_clause error SEMI",
        "KW_GLOBAL error global_var_clause  SEMI",
    )
    def global_var(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global variable errors."""
        self.error_out(
            "Global variable not formatted correctly, should be `global <name> = <value>, ...;`"
        )


#     @_(
#         "name_literal EQ connect",
#         "global_var_clause COMMA name_literal EQ connect",
#     )
#     def global_var_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Global variable tail rule."""
#         return p

#     @_(
#         "KW_TEST name_literal multistring KW_WITH walker_ref code_block",
#         "KW_TEST name_literal multistring KW_WITH walker_ref spawn_ctx code_block",
#         "KW_TEST name_literal multistring KW_WITH attr_block code_block",
#         "KW_TEST name_literal multistring KW_WITH attr_block spawn_ctx code_block",
#     )
#     def test(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Test rule."""
#         return p

#     # Import Statements
#     # -----------------
#     @_(
#         "KW_IMPORT COLON name_literal import_path SEMI",
#         "KW_IMPORT COLON name_literal import_path KW_AS name_literal SEMI",
#         "KW_IMPORT COLON name_literal KW_FROM import_path COMMA name_as_list SEMI",
#     )
#     def import_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Import rule."""
#         return p

#     @_(
#         "import_path_prefix",
#         "import_path_prefix import_path_tail",
#     )
#     def import_path(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Import path rule."""
#         return p

#     @_(
#         "name_literal",
#         "DOT name_literal",
#         "DOT DOT name_literal",
#     )
#     def import_path_prefix(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Import path prefix rule."""
#         return p

#     @_(
#         "DOT name_literal",
#         "import_path_tail DOT name_literal",
#     )
#     def import_path_tail(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Import path tail rule."""
#         return p

#     @_(
#         "name_literal KW_AS name_literal",
#         "name_as_list COMMA name_literal KW_AS name_literal",
#     )
#     def name_as_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Name as list rule."""
#         return p

#     # Architype elements
#     # ------------------
#     @_(
#         "KW_NODE name_literal arch_decl_tail",
#         "KW_EDGE name_literal arch_decl_tail",
#         "KW_OBJECT name_literal arch_decl_tail",
#         "KW_WALKER name_literal arch_decl_tail",
#     )
#     def architype(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Architype rule."""
#         return p

#     @_(
#         "attr_block",
#         "inherited_archs attr_block",
#     )
#     def arch_decl_tail(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Architype tail rule."""
#         return p

#     @_(
#         "sub_name",
#         "inherited_archs sub_name",
#     )
#     def inherited_archs(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Sub name list rule."""
#         return p

#     @_("COLON name_literal")
#     def sub_name(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Sub name rule."""
#         return p

#     # Attribute blocks
#     # ----------------
#     @_(
#         "LBRACE RBRACE",
#         "LBRACE attr_stmt_list RBRACE",
#         "LBRACE doc_string_literal attr_stmt_list RBRACE",
#         "COLON attr_stmt",
#         "SEMI",
#     )
#     def attr_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Attribute block rule."""
#         return p

#     @_(
#         "attr_stmt",
#         "attr_stmt_list attr_stmt",
#     )
#     def attr_stmt_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Attribute statement list rule."""
#         return p

#     @_(
#         "has_stmt",
#         "can_stmt",
#     )
#     def attr_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Attribute statement rule."""
#         return p

#     # Has statements
#     # --------------
#     @_("KW_HAS has_assign_clause SEMI")
#     def has_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Has statement rule."""
#         return p

#     @_(
#         "has_assign",
#         "has_assign_clause COMMA has_assign",
#     )
#     def has_assign_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Has assign list rule."""
#         return p

#     @_(
#         "has_tag name_literal type_spec",
#         "has_tag name_literal type_spec EQ expression",
#         "name_literal type_spec",
#         "name_literal type_spec EQ expression",
#     )
#     def has_assign(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Has assign rule."""
#         return p

#     @_(
#         "has_tag KW_HIDDEN",
#         "has_tag KW_ANCHOR",
#         "KW_HIDDEN",
#         "KW_ANCHOR",
#     )
#     def has_tag(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Has tag rule."""
#         return p

#     @_("COLON type_name")
#     def type_spec(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Type hint rule."""
#         return p

#     @_(
#         "builtin_type",
#         "name_literal",
#         "TYP_LIST LSQUARE type_name RSQUARE",
#         "TYP_DICT LSQUARE type_name COMMA type_name RSQUARE",
#     )
#     def type_name(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Type hint rule."""
#         return p

#     @_(
#         "TYP_STRING",
#         "TYP_BYTES",
#         "TYP_INT",
#         "TYP_FLOAT",
#         "TYP_LIST",
#         "TYP_DICT",
#         "TYP_BOOL",
#         "KW_TYPE",
#     )
#     def builtin_type(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Any type rule."""
#         return p

#     # Can statements
#     # --------------
#     @_("KW_CAN name_literal event_clause code_block")
#     def can_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Can statement rule."""
#         return p

#     @_(
#         "KW_WITH KW_ENTRY",
#         "KW_WITH KW_EXIT",
#         "KW_WITH name_list KW_ENTRY",
#         "KW_WITH name_list KW_EXIT",
#     )
#     def event_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Event clause rule."""
#         return p

#     @_(
#         "name_literal",
#         "name_list COMMA name_literal",
#     )
#     def name_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Name list rule."""
#         return p

#     @_(
#         "LBRACE RBRACE",
#         "LBRACE statement_list RBRACE",
#     )
#     def code_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Code block rule."""
#         return p

#     # Codeblock statements
#     # --------------------
#     @_(
#         "statement statement_list",
#         "statement",
#     )
#     def statement_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Statement list rule."""
#         return p

#     @_(
#         "expression SEMI",
#         "if_stmt",
#         "try_stmt",
#         "for_stmt",
#         "while_stmt",
#         "assert_stmt SEMI",
#         "ctrl_stmt SEMI",
#         "delete_stmt SEMI",
#         "report_stmt SEMI",
#         "walker_stmt",
#     )
#     def statement(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Statement rule."""
#         return p

#     @_(
#         "KW_IF expression code_block",
#         "KW_IF expression code_block else_stmt",
#         "KW_IF expression code_block elif_stmt_list else_stmt",
#     )
#     def if_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """If statement rule."""
#         return p

#     @_(
#         "KW_ELIF expression code_block",
#         "KW_ELIF expression code_block elif_stmt_list",
#     )
#     def elif_stmt_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Else if statement list rule."""
#         return p

#     @_("KW_ELSE code_block")
#     def else_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Else statement rule."""
#         return p

#     @_(
#         "KW_TRY code_block",
#         "KW_TRY code_block else_from_try",
#     )
#     def try_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Try statement rule."""
#         return p

#     @_(
#         "KW_ELSE KW_WITH name_literal code_block",
#         "KW_ELSE code_block",
#     )
#     def else_from_try(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Else from try rule."""
#         return p

#     @_(
#         "KW_FOR atom EQ expression KW_TO expression KW_BY expression code_block",
#         "KW_FOR atom KW_IN expression code_block",
#         "KW_FOR atom COMMA atom KW_IN expression code_block",
#     )
#     def for_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """For statement rule."""
#         return p

#     @_("KW_WHILE expression code_block")
#     def while_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """While statement rule."""
#         return p

#     @_("KW_ASSERT expression")
#     def assert_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Assert statement rule."""
#         return p

#     @_(
#         "KW_CONTINUE",
#         "KW_BREAK",
#         "KW_SKIP",
#     )
#     def ctrl_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Control statement rule."""
#         return p

#     @_("KW_DELETE expression")
#     def delete_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Delete statement rule."""
#         return p

#     @_(
#         "KW_REPORT expression",
#         "KW_REPORT sub_name EQ expression",
#     )
#     def report_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Report statement rule."""
#         return p

#     @_(
#         "ignore_stmt",
#         "take_stmt",
#         "disengage_stmt",
#         "yield_stmt",
#     )
#     def walker_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Walker statement rule."""
#         return p

#     @_("KW_IGNORE expression SEMI")
#     def ignore_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Ignore statement rule."""
#         return p

#     @_(
#         "KW_TAKE expression SEMI",
#         "KW_TAKE sub_name expression SEMI",
#         "KW_TAKE expression else_stmt",
#         "KW_TAKE sub_name expression else_stmt",
#     )
#     def take_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Take statement rule."""
#         return p

#     @_("KW_DISENGAGE SEMI")
#     def disengage_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Disengage statement rule."""
#         return p

#     @_("KW_YIELD SEMI")
#     def yield_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Yield statement rule."""
#         return p

#     # Expression rules
#     # ----------------
#     @_(
#         "connect",
#         "connect assignment_op expression",
#     )
#     def expression(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Expression rule."""
#         return p

#     @_(
#         "EQ",
#         "CPY_EQ",
#         "ADD_EQ",
#         "SUB_EQ",
#         "MUL_EQ",
#         "DIV_EQ",
#     )
#     def assignment_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Production Assignment rule."""
#         return p

#     @_(
#         "logical",
#         "logical NOT edge_op_ref connect",
#         "logical connect_op connect",
#     )
#     def connect(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Connect rule."""
#         return p

#     @_(
#         "compare",
#         "compare KW_AND logical",
#         "compare KW_OR logical",
#     )
#     def logical(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Logical rule."""
#         return p

#     @_(
#         "arithmetic",
#         "NOT compare",
#         "arithmetic cmp_op compare",
#     )
#     def compare(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Compare rule."""
#         return p

#     @_(
#         "EE",
#         "LT",
#         "GT",
#         "LTE",
#         "GTE",
#         "NE",
#         "KW_IN",
#         "KW_NIN",
#     )
#     def cmp_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Compare operator rule."""
#         return p

#     @_(
#         "term",
#         "term PLUS arithmetic",
#         "term MINUS arithmetic",
#     )
#     def arithmetic(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Arithmetic rule."""
#         return p

#     @_(
#         "factor",
#         "factor STAR_MUL term",
#         "factor DIV term",
#         "factor MOD term",
#     )
#     def term(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Term rule."""
#         return p

#     @_(
#         "PLUS factor",
#         "MINUS factor",
#         "power",
#     )
#     def factor(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Factor rule."""
#         return p

#     @_(
#         "atom",
#         "atom POW factor",
#         "ref",
#         "deref",
#         "KW_SYNC atom",
#     )
#     def power(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Power rule."""
#         return p

#     @_("KW_REF atom")
#     def ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Production for reference rule."""
#         return p

#     @_("STAR_MUL atom")
#     def deref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Dereference rule."""
#         return p

#     # Atom rules
#     # --------------------
#     @_(
#         "int_literal",
#         "float_literal",
#         "multistring",
#         "bool_literal",
#         "null_literal",
#         "name_literal",
#         "list_val",
#         "dict_val",
#         "LPAREN connect RPAREN",
#         "ability_op",
#         "atom atom_trailer",
#         "builtin_type",
#         "global_ref",
#         "atom node_edge_ref",
#         "spawn",
#     )
#     def atom(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Atom rule."""
#         return p

#     @_(
#         "string_literal",
#         "doc_string_literal",
#         "string_literal multistring",
#         "doc_string_literal multistring",
#     )
#     def multistring(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Multistring rule."""
#         return p

#     @_(
#         "LSQUARE RSQUARE",
#         "LSQUARE expr_list RSQUARE",
#     )
#     def list_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """List value rule."""
#         return p

#     @_(
#         "connect",
#         "expr_list COMMA connect",
#     )
#     def expr_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Expression list rule."""
#         return p

#     @_(
#         "LBRACE RBRACE",
#         "LBRACE kv_pairs RBRACE",
#     )
#     def dict_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Production for dictionary value rule."""
#         return p

#     @_(
#         "connect COLON connect",
#         "connect COLON connect COMMA kv_pairs",
#     )
#     def kv_pairs(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Key/value pairs rule."""
#         return p

#     @_(
#         "DBL_COLON name_literal",
#     )
#     def ability_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Ability operator rule."""
#         return p

#     @_(
#         "DOT name_literal",
#         "index_slice",
#         "ability_call",
#         "PIPE_FWD built_in",
#     )
#     def atom_trailer(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Atom trailer rule."""
#         return p

#     @_(
#         "LPAREN RPAREN",
#         "LPAREN param_list RPAREN",
#         "ability_op",
#     )
#     def ability_call(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Ability call rule."""
#         return p

#     @_(
#         "expr_list",
#         "kw_expr_list",
#         "expr_list COMMA kw_expr_list",
#     )
#     def param_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Parameter list rule."""
#         return p

#     @_(
#         "name_literal EQ connect",
#         "name_literal EQ connect COMMA kw_expr_list",
#     )
#     def kw_expr_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Keyword expression list rule."""
#         return p

#     @_(
#         "LSQUARE expression RSQUARE",
#         "LSQUARE expression COLON expression RSQUARE",
#     )
#     def index_slice(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Index/slice rule."""
#         return p

#     @_(
#         "KW_GLOBAL DOT obj_built_in",
#         "KW_GLOBAL DOT name_literal",
#     )
#     def global_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Global reference rule."""
#         return p

#     @_(
#         "node_ref filter_ctx",
#         "edge_op_ref",
#     )
#     def node_edge_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Node/edge reference rule."""
#         return p

#     # Spawn rules
#     # -----------
#     @_("KW_SPAWN spawn_arch")
#     def spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Spawn rule."""
#         return p

#     @_(
#         "node_spawn spawn_ctx",  # captures edge and node spawns
#         "walker_spawn spawn_ctx",
#         "object_spawn spawn_ctx",
#     )
#     def spawn_arch(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Spawn object rule."""
#         return p

#     @_("logical connect_op")
#     def spawn_edge(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Spawn edge rule."""
#         return p

#     @_(
#         "node_ref",
#         "spawn_edge node_ref",
#     )
#     def node_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Node spawn rule."""
#         return p

#     @_(
#         "KW_ASYNC connect walker_ref",
#         "connect walker_ref",
#         "walker_ref",
#     )
#     def walker_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Walker spawn rule."""
#         return p

#     @_("obj_ref")
#     def object_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Type spawn rule."""
#         return p

#     # Built-in function rules
#     # -----------------------
#     @_(
#         "obj_built_in",
#         "cast_built_in",
#     )
#     def built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Built-in rule."""
#         return p

#     @_(
#         "KW_CONTEXT",
#         "KW_INFO",
#         "KW_DETAILS",
#     )
#     def obj_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Object built-in rule."""
#         return p

#     @_(
#         "builtin_type",
#         "arch_ref",
#     )
#     def cast_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Cast built-in rule."""
#         return p

#     # Architype reference rules
#     # -------------------------
#     @_("node_ref", "edge_ref", "walker_ref", "obj_ref")
#     def arch_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Architype reference rule."""
#         return p

#     @_("KW_NODE DBL_COLON name_literal")
#     def node_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Node reference rule."""
#         return p

#     @_("KW_EDGE DBL_COLON name_literal")
#     def edge_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Node reference rule."""
#         return p

#     @_("KW_WALKER DBL_COLON name_literal")
#     def walker_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Walker reference rule."""
#         return p

#     @_("KW_OBJECT DBL_COLON name_literal")
#     def obj_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Type reference rule."""
#         return p

#     # Node / Edge reference and connection rules
#     # ------------------------------------------
#     @_(
#         "edge_to",
#         "edge_from",
#         "edge_any",
#     )
#     def edge_op_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Edge reference rule."""
#         return p

#     @_(
#         "ARROW_R",
#         "ARROW_R_p1 name_literal filter_ctx ARROW_R_p2",
#     )
#     def edge_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Edge to rule."""
#         return p

#     @_(
#         "ARROW_L",
#         "ARROW_L_p1 name_literal filter_ctx ARROW_L_p2",
#     )
#     def edge_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Edge from rule."""
#         return p

#     @_(
#         "ARROW_BI",
#         "ARROW_L_p1 name_literal filter_ctx ARROW_R_p2",
#     )
#     def edge_any(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Edge any rule."""
#         return p

#     @_(
#         "connect_to",
#         "connect_from",
#         "connect_any",
#     )
#     def connect_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Connect operator rule."""
#         return p

#     @_(
#         "CARROW_R",
#         "CARROW_R_p1 name_literal spawn_ctx CARROW_R_p2",
#     )
#     def connect_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Connect to rule."""
#         return p

#     @_(
#         "CARROW_L",
#         "CARROW_L_p1 name_literal spawn_ctx CARROW_L_p2",
#     )
#     def connect_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Connect from rule."""
#         return p

#     @_(
#         "CARROW_BI",
#         "CARROW_L_p1 name_literal spawn_ctx CARROW_R_p2",
#     )
#     def connect_any(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Connect any rule."""
#         return p

#     @_(
#         "LPAREN filter_compare_list RPAREN",
#         # "",
#     )
#     def filter_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Filter context rule."""
#         return p

#     @_("LPAREN spawn_assign_list RPAREN")
#     def spawn_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Spawn context rule."""
#         return p

#     @_(
#         "name_literal EQ expression",
#         "name_literal EQ expression COMMA spawn_assign_list",
#         # "",
#     )
#     def spawn_assign_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Spawn assignment list rule."""
#         return p

#     @_(
#         "name_literal cmp_op expression",
#         "name_literal cmp_op expression COMMA filter_compare_list",
#         # "",
#     )
#     def filter_compare_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Filter comparison list rule."""
#         return p

#     # Literal rules (overcomes sly limitations)
#     # -----------------------------------------

#     @_("INT")
#     def int_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Integer literal rule."""
#         return p

#     @_("FLOAT")
#     def float_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Float literal rule."""
#         return p

#     @_("STRING")
#     def string_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Str literal rule."""
#         return p

#     @_("DOC_STRING")
#     def doc_string_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Doc_string literal rule."""
#         return p

#     @_("BOOL")
#     def bool_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Boolean literal rule."""
#         return p

#     @_("NULL")
#     def null_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Null literal rule."""
#         return p

#     @_("NAME")
#     def name_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
#         """Name literal rule."""
#         return p
