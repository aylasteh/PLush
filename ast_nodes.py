from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ASTNode(ABC):
    position: int
    XXXXX: str


class Declaration(ASTNode):
    pass


class Type(ASTNode):
    pass


class Expression(ASTNode):
    pass

@dataclass
class ExpressionList(ASTNode):
     expr_list: [Expression]

class Variable(ASTNode):
    pass


class Oper(Enum):
    plus = 1
    minus = 2
    times = 3
    divide = 4
    eq = 5
    neq = 6
    lt = 7
    le = 8
    gt = 9
    ge = 10


# DECLARATION


@dataclass
class DeclarationBlock(ASTNode):
    declaration_list: List[Declaration]


@dataclass
class Field(ASTNode):
    name: str
    type: str


@dataclass
class RecordTy(Type):
    field_list: List[Field]


@dataclass
class ArrayTy(Type):
    array: str

class ValueDec(Declaration):
    name: str
    type: Type
    value: Expression

@dataclass
class VariableDec(Declaration):
    name: str
    type: Optional[str]
    exp: Expression
    escape: bool = False


@dataclass
class FunctionDec(ASTNode):
    name: str
    params: List[Field]
    param_escapes: List[bool]
    return_type: Optional[str]
    body: Expression




@dataclass
class FunctionCall:
    name: str
    args: List[Expression] 
    position: int 


# EXPRESSION


@dataclass
class VarExp(Expression):
    var: Variable

@dataclass
class ValExp(Expression):
    val: Variable


@dataclass
class NilExp(Expression):
    pass

@dataclass
class BoolExp(Expression):
    value: bool

@dataclass
class FloatExp(Expression):
    value: float

@dataclass
class IntExp(Expression):
    int: int


@dataclass
class StringExp(Expression):
    string: str


@dataclass
class AssignExp(Expression):
    var: Variable
    exp: Expression


@dataclass
class IfExp(Expression):
    test: Expression
    then_do: ExpressionList
    else_do: Optional[ExpressionList]


@dataclass
class WhileExp(Expression):
    test: Expression
    body: Expression


@dataclass
class ArrayExp(Expression):
    type: str
    size: Expression
    init: Expression


@dataclass
class EmptyExp(Expression):
    pass

@dataclass
class OpExp(Expression):
    oper: Oper
    left: Expression
    right: Expression



# VARIABLE

@dataclass
class ValDeclaration(Declaration):
    name: str
    type: Type
    value: Expression

@dataclass
class VarDeclaration(Declaration):
    name: str
    type: Type
    initial_value: Expression

@dataclass
class VarList(ASTNode):
    args: List[VarDeclaration]

@dataclass
class ValList(ASTNode):
    args: List[ValDeclaration]

@dataclass
class FunctionDec(ASTNode):
    name: str
    params: ValList
    param_escapes: List[bool]
    return_type: Optional[str]
    body: ExpressionList




@dataclass
class FunctionDecBlock(Declaration):
    function_dec_list: List[FunctionDec]
@dataclass
class Field(ASTNode):
    name: str
    type: Type


@dataclass
class ArgsList(ASTNode):
    args: List[Expression]

'''@dataclass
class SimpleVar(Variable):
    sym: str


@dataclass
class FieldVar(Variable):
    var: Variable
    sym: str


@dataclass
class SubscriptVar(Variable):
    var: Variable
    exp: Expression'''


'''from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ASTNode(ABC):
    position: int
    typecheck: str


class Declaration(ASTNode):
    pass


class Type(ASTNode):
    pass


class Expression(ASTNode):
    pass

@dataclass
class ExpressionList(ASTNode):
    expr_list: [Expression] # type: ignore

class Variable(ASTNode):
    pass


class Oper(Enum):
    plus = 1
    minus = 2
    times = 3
    divide = 4
    eq = 5
    neq = 6
    lt = 7
    le = 8
    gt = 9
    ge = 10


# DECLARATION


@dataclass
class DeclarationBlock(ASTNode):
    declaration_list: List[Declaration]

@dataclass
class Field(ASTNode):
    name: str
    type: str


@dataclass
class RecordTy(Type):
    field_list: List[Field]


@dataclass
class ArrayTy(Type):
    array: str

class ValueDec(Declaration):
    name: str
    type: Type
    value: Expression

@dataclass
class VariableDec(Declaration):
    name: str
    type: Optional[str]
    exp: Expression
    escape: bool = False


@dataclass
class FunctionDec(ASTNode):
    name: str
    params: List[Field]
    param_escapes: List[bool]
    return_type: Optional[str]
    body: Expression


@dataclass
class FunctionDecBlock(Declaration):
    function_dec_list: List[FunctionDec]

@dataclass
class FunctionCall:
    name: str
    args: List[Expression] 
    position: int 


# EXPRESSION


@dataclass
class VarExp(Expression):
    var: Variable

@dataclass
class ValExp(Expression):
    val: Variable


@dataclass
class NilExp(Expression):
    pass

@dataclass
class BoolExp(Expression):
    value: bool

@dataclass
class FloatExp(Expression):
    value: float

@dataclass
class IntExp(Expression):
    int: int


@dataclass
class StringExp(Expression):
    string: str


@dataclass
class AssignExp(Expression):
    var: Variable
    exp: Expression


@dataclass
class IfExp(Expression):
    test: Expression
    then_do: ExpressionList
    else_do: Optional[ExpressionList]


@dataclass
class WhileExp(Expression):
    test: Expression
    body: Expression


@dataclass
class ArrayExp(Expression):
    type: str
    size: Expression
    init: Expression


@dataclass
class EmptyExp(Expression):
    pass

@dataclass
class OpExp(Expression):
    oper: Oper
    left: Expression
    right: Expression



# VARIABLE

@dataclass
class ValDeclaration(Declaration):
    name: str
    type: Type
    value: Expression

@dataclass
class VarDeclaration(Declaration):
    name: str
    type: Type
    initial_value: Expression

@dataclass
class VarList(ASTNode):
    args: List[VarDeclaration]

@dataclass
class ValList(ASTNode):
    args: List[ValDeclaration]

@dataclass
class FunctionDec(ASTNode):
    name: str
    params: ValList
    param_escapes: List[bool]
    return_type: Optional[str]
    body: ExpressionList

@dataclass
class FuncrionDecBlock(Declaration):
    function_dec_list: List[FunctionDec]

@dataclass
class Field(ASTNode):
    name: str
    type: Type

@dataclass
class ArgsList(ASTNode):
    args: List[Expression]

'''
'''@dataclass
class SimpleVar(Variable):
    sym: str


@dataclass
class FieldVar(Variable):
    var: Variable
    sym: str


@dataclass
class SubscriptVar(Variable):
    var: Variable
    exp: Expression'''