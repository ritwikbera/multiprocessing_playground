import math

# Two basic autograd implementations

'''
This implementation is source from here: https://rufflewind.com/2016-12-30/reverse-mode-automatic-differentiation

THe version recursively calls The definition of children is opposite to that of the 
one used in Karpathy's version. Here child nodes are defines as the nodes that emanates as output
from the current node.

The gradient call starts at any of the input nodes and recursively find its base termination condition
at the output and then backtracks from there toward the input finding all intermediate gradients

The weight parameter in every child can be though of as a local gradient that multiplies with
the incoming output gradient during the backward pass and propagates towards the input.
'''
class Var:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.grad_value = None

    def grad(self):
        if self.grad_value is None:

        	# this is the chain rule/backprop step that is explicitly defined in .backward() functions
            self.grad_value = sum(weight * var.grad()
                                  for weight, var in self.children)
        return self.grad_value

    def __add__(self, other):
        z = Var(self.value + other.value)

        self.children.append((1.0, z))
        other.children.append((1.0, z))

        return z

    def __mul__(self, other):
        z = Var(self.value * other.value)

        self.children.append((other.value, z))
        other.children.append((self.value, z))

        return z

def sin(x):
    z = Var(math.sin(x.value))

    x.children.append((math.cos(x.value), z))

    return z

'''
This implementation is by Andrej Karpathy (@github.com/karpathy/micrograd)

Karpathy's version starts its gradient calculation call from the output node 
and performs backward calls toward the input nodes in topological order.

Similar to the above version, the __add__ and __mul__ operators generate their own
nodes with their own backward functions as they are called and how those backward operations
affect the gradients of their child nodes.
'''

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

if __name__=='__main__'
    x = Var(0.5)
    y = Var(4.2)
    z = x * y + sin(x)
    z.grad_value = 1.0

    assert abs(z.value - 2.579425538604203) <= 1e-15
    assert abs(x.grad() - (y.value + math.cos(x.value))) <= 1e-15
    assert abs(y.grad() - x.value) <= 1e-15
