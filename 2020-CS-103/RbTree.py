
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# value = ['abc','data','a','b']
# attr = [('static','1'),('static','2'),('static,3'),('static,4')]

import random
class RBNode:
    def __init__(self, val):
        self.red = False
        self.parent = None
        self.val = val
        self.attr = None
        self.attribute = None
        self.left = None
        self.right = None


class RBTree:
    def __init__(self):
        self.allocate()
    def allocate(self):
        self.nil = RBNode(None)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert(self, val,attr):
        # Ordinary Binary Search Insertion
        new_node = RBNode(val)
        new_node.attr = attr
        new_node.parent = None
        new_node.left = self.nil
        
        new_node.right = self.nil
        new_node.red = True  # new node must be red
        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                return

        # Set the parent and insert the new node
        new_node.parent = parent
        if parent == None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

        # Fix the tree
        self.fix_insert(new_node)

    def fix_insert(self, new_node):
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left  # uncle
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_left(new_node.parent.parent)
            else:
                u = new_node.parent.parent.right  # uncle

                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_right(new_node.parent.parent)
        self.root.red = False

    def exists(self, val):
        curr = self.root
        while curr != self.nil and val != curr.val:
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    # rotate left at node x
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def __repr__(self):
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)
    
def lookup(node, key):
        if node == None or key == node.val:
            return node.val + " " + str(id(node.val))

        if key < node.val:
            return lookup(node.left, key)
        return lookup(node.right, key)

def get_attribute(node,key):
    if node == None or key == node.val:
        return node.attr

    if key < node.val:
        return lookup(node.left, key)
    return lookup(node.right, key)
 
def free(node):
    if node:

        # recurse: visit all nodes in the two subtrees
        free(node.left)           
        free(node.right)

        # after both subtrees have been visited, set pointers of this node to None
        node.left = None
        node.right = None

def print_tree(node, lines, level=0):
    if node.val != None:
        print_tree(node.left, lines, level + 1)
        lines.append('-' * 4 * level + '> ' +
                     str(node.val) + ' ' + ('red' if node.red else 'black') + ' ' + str(node.attr))
        print_tree(node.right, lines, level + 1)

def visualize_tree(node, parent_x=0, parent_y=0, x=0, y=0, level=1, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    if node.val is not None:
        color = 'red' if node.red else 'black'
        text_color = 'white' if node.red else 'white'
        ax.add_patch(Rectangle((x, y), 0.02, 0.02, fill=True, color=color))
        ax.text(x + 0.010, y + 0.01, str(node.val), ha='center', va='center', color=text_color)

    if node.left.val is not None:
        child_x = x - 0.05 / level
        child_y = y - 0.05
        ax.plot([x, child_x], [y, child_y], color='black')
        visualize_tree(node.left, x, y, child_x, child_y, level * 2, ax)

    if node.right.val is not None:
        child_x = x + 0.05 / level
        child_y = y - 0.05
        ax.plot([x, child_x], [y, child_y], color='black')
        visualize_tree(node.right, x, y, child_x, child_y, level * 2, ax)

    ax.axis('off')
    return ax



def main_function(tokens):
    tree = RBTree()
    # for i in range(0,len(value)):
    #     
    for token in tokens:
        print(token)
        tree.insert(token.value,token.token_type)
    print(tree)
    # value_search = lookup(tree.root,'abc')
    # print(value_search)
    # attribute = get_attribute(tree.root, 'abc')
    # print(attribute)
    print("Free the storage of Symbol Table")
    # print("Again print tree: ")
    visualize_tree(tree.root)
    plt.show()
    free(tree.root)