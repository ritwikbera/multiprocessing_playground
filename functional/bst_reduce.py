from functools import *

class Tree(object):
    def __init__(self, val=None):
        self.value = val
        self.left = None
        self.right = None

    def add(self, val):
        if not self.value:
            self.value = val
            self.left = Tree()
            self.right = Tree()
        elif val < self.value:
            self.left.add(val)
        elif val > self.value:
            self.right.add(val)
        
        return self

    def __str__(self):
        to_print=''
        if self.left is not None and self.right is not None:
            to_print+=str(self.left)+' '+str(self.value)+' '+str(self.right)

        return to_print



def insert_into_tree(tree, number):
    return tree.add(number)

def build_tree(numbers):
    return reduce(insert_into_tree, numbers, Tree())

if __name__=='__main__':
    numbers = [13, 3, 7, 23, 76, 32]
    tree = build_tree(numbers)
    print(tree)
