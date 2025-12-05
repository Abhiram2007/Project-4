from nodes import *
from expressionParser import parseExpression


def computeNthDerivative(f, var, n):
    for _ in range(n):
        f = f.derivative(var)
        f = simplify(f)
    return f

def numericMode():
    print("\nNumeric Differention")
    expressionString = input("enter a function in x: ")

    try:
        f = parseExpression(expressionString)
    except Exception as e:
        print("Parsing Error: ", e)
        return
    
    xval = float(input("Enter x-value: "))
    fVar = None

    def assignValues(node):
        if isinstance(node, InputNode):
            node.value = xval
        for char in node.inputs:
            assignValues(char)

    assignValues(f)

    h = float(input("Enter step size h: "))

    f1 = (f.get_value() - computeShifted(f, xval - h).get_value()) / h
    print("Approx derivative: ", f1)


def computeShifted(f, x):
    expressionString = "FAKE"
    import copy
    newf = copy.deepcopy(f)
    assignXValue(newf, x)
    return newf

def assignXValue(node, x):
    if isinstance(node, InputNode):
        node.value = x
    for c in node.inputs:
        assignXValue(c, x)


def symbolicMode():
    print("\nSymbolic Differentiation")
    expressionString = input("enter a function in x: ")

    try:
        f = parseExpression(expressionString)
    except Exception as e:
        print("Parsing Error: ", e)
        return
    
    f.dump_structure()
    
    n = int(input("Enter derivative order n: "))

    df = computeNthDerivative(f, "x", n)
    dfSimplified = simplify(df)
    
    
    print("\nSymbolic Derivative created.")
    print(dfSimplified)


# x = cn(5) * cn(10) * sin(cn(m.pi)) + ln(m.e)

# print(simplify(x))

while True:
    print("\nDerivative Calculator") 
    print("1. Numeric Differentiation")
    print("2. Symbolic Derivative")
    mode = input("Choose mode (1/2): ")

    if mode == "1":
        numericMode()
    
    elif mode == "2":
        symbolicMode()

    else:
        print("Invalid choice.")
    
    runAgain = input("\nRun Again? (y/n): ")
    if runAgain.lower() != "y":
        print("Thank you for using this!")
        break



