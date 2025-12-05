#nodes

from abc import ABC, abstractmethod
import math as m
from collections import defaultdict
from copy import deepcopy


precAdd = 10
precMul = 20
precPow = 30
precAtom = 40


def constantConverter(x):
    if isinstance(x, ComputationalNode):
        return x
    return ConstantNode(x)

class ComputationalNode(ABC):
    def __init__(self, inputs):
        self.inputs = inputs

    @abstractmethod
    def get_value(self):
        pass

    def derivative(self, var):
        pass



    def __add__(self, other): return BinaryAddNode([self, constantConverter(other)])
    def __radd__(self, other): return BinaryAddNode([constantConverter(other), self])
    def __sub__(self, other): return BinarySubNode([self, constantConverter(other)])
    def __rsub__(self, other): return BinarySubNode([constantConverter(other), self])
    def __mul__(self, other): return BinaryMulNode([self, constantConverter(other)])
    def __rmul__(self, other): return BinaryMulNode([constantConverter(other), self])
    def __truediv__(self, other): return BinaryDivNode([self, constantConverter(other)]) 
    def __rtruediv__(self, other): return BinaryDivNode([constantConverter(other), self])
    def __pow__(self, other): return BinaryPowNode([self, constantConverter(other)])
    def __rpow__(self, other): return BinaryPowNode([constantConverter(other), self])
    def __neg__(self): return ConstantNode(-1) * self

    def __str__(self): return self.to_str()

    def to_str(self, parent_prec=0):
        raise NotImplementedError("String conversion is not possible for this mathematical operation.")
    
    def dump_structure(self, depth=0):
        print("  " * depth + self.__class__.__name__ + "  " + self.__str__())
        for i in self.inputs:
            i.dump_structure(depth + 1)


#binary operators

class BinaryAddNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() + self.inputs[1].get_value()
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) + self.inputs[1].derivative(var)

    def to_str(self, parent_prec=0):
        s = f"{self.inputs[0].to_str(precAdd)} + {self.inputs[1].to_str(precAdd)}"
        return s if parent_prec <= precAdd else f"({s})"

class BinarySubNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() - self.inputs[1].get_value()
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) - self.inputs[1].derivative(var)
    
    def to_str(self, parent_prec=0):
        s = f"{self.inputs[0].to_str(precAdd)} - {self.inputs[1].to_str(precAdd + 1)}"
        return s if parent_prec <= precAdd else f"({s})"

class BinaryMulNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() * self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return u.derivative(var) * v + u * v.derivative(var)
    
    def to_str(self, parent_prec=0):
        a = self.inputs[0]
        b = self.inputs[1]

        def factorString(node):
            if isinstance(node, ConstantNode):
                return node.to_str(precMul)
            return node.to_str(precMul)


        if isinstance(a, ConstantNode) and a.value == 1:
            s = b.to_str(precMul)
        elif isinstance(b, ConstantNode) and b.value == 1:
            s = a.to_str(precMul)
        elif isinstance(a, ConstantNode) and a.value == -1:
            s = "-" + b.to_str(precMul)
        elif isinstance(b, ConstantNode) and b.value == -1:
            s = "-" + a.to_str(precMul)
        elif isinstance(a, ConstantNode) and not isinstance(b, ConstantNode):
            s = f"{a.to_str(precMul)}{b.to_str(precMul)}"
        elif isinstance(b, ConstantNode) and not isinstance(a, ConstantNode):
            s = f"{b.to_str(precMul)}{a.to_str(precMul)}"
        else:
            s = f"{a.to_str(precMul)} * {b.to_str(precMul)}"

        return s if parent_prec <= precMul else f"({s})"

class BinaryDivNode(ComputationalNode):
    def get_value(self):
        denominator = self.inputs[1].get_value()
        if denominator == 0:
            raise ZeroDivisionError("Division by Zero")
        return self.inputs[0].get_value() / self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return (u.derivative(var) * v - u * v.derivative(var)) / (v ** 2)
    
    def to_str(self, parent_prec=0):
        s = f"{self.inputs[0].to_str(precMul)} / {self.inputs[1].to_str(precMul + 1)}"
        return s if parent_prec <= precMul else f"({s})"

class BinaryPowNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() ** self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return (u ** v) * (v.derivative(var) * ln(u) + v * u.derivative(var) / u)
    
    def to_str(self, parent_prec=0):
        s = f"{self.inputs[0].to_str(precPow)}^{self.inputs[1].to_str(precPow)}"
        return s if parent_prec <= precPow else f"({s})"
#single operators

class ExpNode(ComputationalNode):
    def get_value(self):
        return m.exp(self.inputs[0].get_value())
    
    def derivative(self, var):
        u = self.inputs[0]
        return ExpNode([u]) * u.derivative(var)

    def to_str(self, parent_prec=0):
        return f"e^{self.inputs[0].to_str()}"

class NaturalLogNode(ComputationalNode):
    def get_value(self):
        if self.inputs[0].get_value <= 0:
            raise ValueError("ln undefined for non-positive results")
        return m.log(self.inputs[0].get_value())
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) / self.inputs[0]
    
    def to_str(self, parent_prec=0):
        return f"ln({self.inputs[0].to_str()})"

    
class SinNode(ComputationalNode):
    def get_value(self):
        return m.sin(self.inputs[0].get_value())
    
    def derivative(self, var):
        return cos(self.inputs[0]) * self.inputs[0].derivative(var)
    
    def to_str(self, parent_prec=0):
        return f"sin({self.inputs[0].to_str()})"
    
class CosNode(ComputationalNode):
    def get_value(self):
        return m.cos(self.inputs[0].get_value())

    def derivative(self, var):
        return -sin(self.inputs[0]) * self.inputs[0].derivative(var)

    def to_str(self, parent_prec=0):
        return f"cos({self.inputs[0].to_str()})"

class TanNode(ComputationalNode):
    def get_value(self):
        return m.tan(self.inputs[0].get_value())
    
    def derivative(self, var):
        return (sec(self.inputs[0]) ** 2) * self.inputs[0].derivative(var)
    
    def to_str(self, parent_prec=0):
        return f"tan({self.inputs[0].to_str()})"


#data

class ConstantNode(ComputationalNode):
    def __init__(self, value):
        super().__init__([])
        self.value = float(value)

    def get_value(self):
        return self.value
    
    def derivative(self, var):
        return ConstantNode(0)
    
    def to_str(self, parent_prec=0):
        if abs(self.value - round(self.value)) < 1e-12:
            return str(int(round(self.value)))
        else:
            return str(self.value)
    
class InputNode(ComputationalNode):
    def __init__(self, name, value=None):
        super().__init__([])
        self.name = name
        self.value = value
    
    def get_value(self):
        if self.value is None:
            raise ValueError(f"Variable {self.name} has no value.")
        return self.value
    
    def derivative(self, var):
        return ConstantNode(1) if self.name == var else ConstantNode(0)
    
    def to_str(self, parent_prec=0):
        return self.name
    
#simplifications bc im not about to type out the whole ass difficult sin cos tan shi for the stuff

def inp(name, value=None): return InputNode(name, value)
def cn(value): return ConstantNode(value)
def exp(x): return ExpNode([constantConverter(x)])
def ln(x): return NaturalLogNode([constantConverter(x)])

def sin(x): return SinNode([constantConverter(x)])
def cos(x): return CosNode([constantConverter(x)])
def tan(x): return TanNode([constantConverter(x)])
def sec(x): return BinaryDivNode([cn(1), cos(x)])

#Simplifier

def isConstant(node):
    return isinstance(node, ConstantNode)

def isVariable(node):
    return isinstance(node, InputNode)

def copyNode(node):
    return deepcopy(node)

def gatherAddTerms(node, terms):
    if isinstance(node, BinaryAddNode):
        gatherAddTerms(node.inputs[0], terms)
        gatherAddTerms(node.inputs[1], terms)
    else:
        terms.append(node)


def gatherMultFactors(node, factors):
    if isinstance(node, BinaryMulNode):
        gatherMultFactors(node.inputs[0], factors)
        gatherMultFactors(node.inputs[1], factors)
    else:
        factors.append(node)


def buildAdditionTree(termList):
    if not termList:
        return ConstantNode(0)
    node = termList[0]
    for t in termList[1:]:
        node = BinaryAddNode([node, t])
    return node

def buildMultTree(factorList):
    if not factorList:
        return ConstantNode(1)
    node = factorList[0]
    for f in factorList[1:]:
        node = BinaryMulNode([node, f])
    return node

def simplify(node):
    #AAAAAAAAAAAAAAAAAAAAAAAAAAAAGH
    if isinstance(node, ConstantNode) or isinstance(node, InputNode):
        return node
    
    simplifiedChildNodes = [simplify(ch) for ch in node.inputs]
    node.inputs = simplifiedChildNodes

    try:
        if isinstance(node, BinaryAddNode) and all(isConstant(c) for c in node.inputs):
            return ConstantNode(node.get_value())
        if isinstance(node, BinarySubNode) and all(isConstant(c) for c in node.inputs):
            return ConstantNode(node.get_value())
        if isinstance(node, BinaryMulNode) and all(isConstant(c) for c in node.inputs):
            return ConstantNode(node.get_value())
        if isinstance(node, BinaryDivNode) and all(isConstant(c) for c in node.inputs):
            return ConstantNode(node.get_value())
        if isinstance(node, BinaryPowNode) and all(isConstant(c) for c in node.inputs):
            return ConstantNode(node.get_value())
    except Exception:
        pass

    if isinstance(node, BinaryAddNode):
        terms = []
        gatherAddTerms(node, terms)
        constantSum = 0
        newTerms = []
        simpleCoefficients = defaultdict(float)
        complexTerms = []

        for t in terms:
            if isConstant(t):
                constantSum += t.value
            elif isinstance(t, BinaryMulNode):
                factors = []
                gatherMultFactors(t, factors)
                constantFactor = 1
                variablePart = None
                other = []
                for f in factors:
                    if isConstant(f):
                        constantFactor *= f.value
                    elif isVariable(f) and variablePart is None:
                        variablePart = f
                    else:
                        other.append(f)
                if variablePart is not None and not other:
                    simpleCoefficients[variablePart.name] += constantFactor
                else:
                    complexTerms.append(t)
            elif isVariable(t):
                simpleCoefficients[t.name] += 1
            else:
                complexTerms.append(t)

        for name, coeff in simpleCoefficients.items():
            if abs(coeff) < 1e-12:
                continue
            variableNode = InputNode(name)
            if abs(coeff - 1) < 1e-12:
                newTerms.append(variableNode)
            else:
                newTerms.append(BinaryMulNode([ConstantNode(coeff), variableNode]))

        newTerms.extend(complexTerms)
        if abs(constantSum) > 1e-12:
            newTerms.append(ConstantNode(constantSum))

        if not newTerms:
            return ConstantNode(0)
        if len(newTerms) == 1:
            return newTerms[0]
        
        node = buildAdditionTree(newTerms)
        return node
    
    if isinstance(node, BinarySubNode):
        a, b = node.inputs
        if isConstant(b) and abs(b.value) < 1e-12:
            return a
        return BinarySubNode([a, b])
    
    if isinstance(node, BinaryMulNode):
        factors = []
        gatherMultFactors(node, factors)
        constantProduct = 1
        newFactors = []
        for f in factors:
            if isConstant(f):
                constantProduct *= f.value
            else:
                newFactors.append(f)

        if abs(constantProduct) < 1e-12:
            return ConstantNode(0)
        
        if not newFactors:
            return ConstantNode(constantProduct)
        
        if abs(constantProduct - 1) > 1e-12:
            newFactors.insert(0, ConstantNode(constantProduct))

        if len(newFactors) == 1:
            return newFactors[0]
        node = buildMultTree(newFactors)
        return node
    
    if isinstance(node, BinaryDivNode):
        a, b = node.inputs
        if isConstant(a) and abs(a.value) < 1e-12:
            return ConstantNode(0)
        if isConstant(b) and abs(b.value - 1) < 1e-12:
            return a
        return node
    
    if isinstance(node, BinaryPowNode):
        base, exp = node.inputs
        if isConstant(exp):
            if abs(exp.value - 1) < 1e-12:
                return base
            if abs(exp.value) < 1e-12:
                return ConstantNode(1)
        if isConstant(base):
            if abs(base.value - 1) < 1e-12:
                return ConstantNode(1)
            if isConstant(exp):
                pass
        return node
    
    if isinstance(node, NaturalLogNode):
        inner = node.inputs[0]
        if isinstance(inner, ExpNode):
            return inner.inputs[0]
        return node
    
    if isinstance(node, ExpNode):
        inner = node.inputs[0]
        if isinstance(inner, NaturalLogNode):
            return inner.inputs[0]
        return node
    
    if isinstance(node, SinNode) and isConstant(node.inputs[0]):
        return ConstantNode(node.get_value())
    
    if isinstance(node, CosNode) and isConstant(node.inputs[0]):
        return ConstantNode(node.get_value())
    
    if isinstance(node, TanNode) and isConstant(node.inputs[0]):
        return ConstantNode(node.get_value())

    return node

