#nodes

from abc import ABC, abstractmethod
import math as m

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

    def __str__(self): return self.to_string()

    def to_string(self):
        raise NotImplementedError("String conversion is not possible.")

    def __add__(self, other): return BinaryAddNode([self, constantConverter(other)])
    def __sub__(self, other): return BinarySubNode([self, constantConverter(other)])
    def __mul__(self, other): return BinaryMulNode([self, constantConverter(other)])
    def __truediv__(self, other): return BinaryDivNode([self, constantConverter(other)]) 
    def __pow__(self, other): return BinaryPowNode([self, constantConverter(other)])


#binary operators

class BinaryAddNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() + self.inputs[1].get_value()
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) + self.inputs[1].derivative(var)

    def to_string(self):
        return f"({self.inputs[0]} + {self.inputs[1]})"

class BinarySubNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() - self.inputs[1].get_value()
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) - self.inputs[1].derivative(var)
    
    def to_string(self):
        return f"({self.inputs[0]} - {self.inputs[1]})"

class BinaryMulNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() * self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return u.derivative(var) * v + u * v.derivative(var)
    
    def to_string(self):
        return f"({self.inputs[0]} * {self.inputs[1]})"

class BinaryDivNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() / self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return (u.derivative(var) * v - u * v.derivative(var)) / (v ** 2)
    
    def to_string(self):
        return f"({self.inputs[0]} / {self.inputs[1]})"

class BinaryPowNode(ComputationalNode):
    def get_value(self):
        return self.inputs[0].get_value() ** self.inputs[1].get_value()
    
    def derivative(self, var):
        u, v = self.inputs
        return (u ** v) * (v.derivative(var) * ln(u) + v * u.derivative(var) / u)
    
    def to_string(self):
        return f"({self.inputs[0]} ^ {self.inputs[1]})"

#single operators

class ExpNode(ComputationalNode):
    def get_value(self):
        return m.exp(self.inputs[0].get_value())
    
    def derivative(self, var):
        return exp(self.inputs[0] * self.inputs[0].derivative(var)) 

    def to_string(self):
        return f"exp({self.inputs[0]})"

class NaturalLogNode(ComputationalNode):
    def get_value(self):
        return m.log(self.inputs[0].get_value())
    
    def derivative(self, var):
        return self.inputs[0].derivative(var) / self.inputs[0]
    
    def to_string(self):
        return f"ln({self.inputs[0]})"

    
class SinNode(ComputationalNode):
    def get_value(self):
        return m.sin(self.inputs[0].get_value())
    
    def derivative(self, var):
        return cos(self.inputs[0]) * self.inputs[0].derivative(var)
    
    def to_string(self):
        return f"sin({self.inputs[0]})"
    
class CosNode(ComputationalNode):
    def get_value(self):
        return m.cos(self.inputs[0].get_value())

    def derivative(self, var):
        return -sin(self.inputs[0]) * self.inputs[0].derivative(var)

    def to_string(self):
        return f"cos({self.inputs[0]})"

class TanNode(ComputationalNode):
    def get_value(self):
        return m.tan(self.inputs[0].get_value())
    
    def derivative(self, var):
        return (sec(self.inputs[0]) ** 2) * self.inputs[0].derivative(var)
    
    def to_string(self):
        return f"tan({self.inputs[0]})"


#data

class ConstantNode(ComputationalNode):
    def __init__(self, value):
        super().__init__([])
        self.value = float(value)

    def get_value(self):
        return self.value
    
    def derivative(self, var):
        return ConstantNode(0)
    
    def to_string(self):
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
        return ConstantNode(1 if self.name == var else 0)
    
    def to_string(self):
        return self.name
    
#simplifications bc im not about to type out the whole ass difficult sin cos tan shi for the stuff

def inp(name, value=None): return InputNode(name, value)
def cn(value): return ConstantNode(value)
def exp(x): return ExpNode([constantConverter(x)])
def ln(x): return NaturalLogNode([constantConverter(x)])

def sin(x): return SinNode([x])
def cos(x): return CosNode([x])
def tan(x): return TanNode([x])
def sec(x): return BinaryDivNode([cn(1), cos(x)])
