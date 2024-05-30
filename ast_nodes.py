from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ASTNode(ABC):
    position: int

class Declaration(ASTNode):
    pass


class Type(ASTNode):
    pass


class Expression(ASTNode):
    pass
    def pp(self):
        print("expression")


@dataclass
class ExpressionList(ASTNode):
    expr_list: [Expression]
    def pp(self):
        print("{")
        for i in self.expr_list:
            i.pp()
        print("}")

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
    exponent = 11
    andop = 12
    orop = 13
    mod = 14
    notop = 15


# DECLARATION


@dataclass
class DeclarationBlock(ASTNode):
    declaration_list: List[Declaration]
    dimension: List[int]


@dataclass
class Field(ASTNode):
    name: str
    type: str

'''
@dataclass
class RecordTy(Type):
    field_list: List[Field]

'''


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


# EXPRESSION

@dataclass
class VarExp(Expression):
    var: Variable
    sem_type: str = None

'''
@dataclass
class ValExp(Expression):
    val: Variable


@dataclass
class NilExp(Expression):
    pass
'''

@dataclass
class BoolExp(Expression):
    value: bool

@dataclass
class FloatExp(Expression):
    value: float

@dataclass
class IntExp(Expression):
    int: int
    sem_type: str = None

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
    body: ExpressionList


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
    opt : int = None
    sem_type: str = None



# VARIABLE


@dataclass
class ValVarDeclaration(Declaration):
    isval: bool
    name: str
    type: Type
    value: Expression
    dimension: List[int]
    complex_type: str = ""

    def pp(self):
        print("ValVarDeclaration")



'''  
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
'''

@dataclass
class ValVarList(ASTNode):
    args: List[ValVarDeclaration]

'''    
@dataclass
class VarList(ASTNode):
    args: List[VarDeclaration]

@dataclass
class ValList(ASTNode):
    args: List[ValDeclaration]
'''

@dataclass
class FunctionDec(ASTNode):
    name: str
    params: ValVarList
    param_escapes: List[bool]
    return_type: Optional[str]
    body: ExpressionList
    arg_types: List[str]

    def pp(self):
        print("FunctionDec")

@dataclass
class ArgsList(ASTNode):
    args: List[DeclarationBlock]
    
@dataclass
class FunctionCall(ASTNode):
    name: str
    args: ArgsList

@dataclass
class FunctionDecBlock(Declaration):
    function_dec_list: List[FunctionDec]
@dataclass
class Field(ASTNode):
    name: str
    type: Type

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
