from .Stack import Stack

class Tree:
    def __init__(self, x=None):
        self.val = x
        self.left = None
        self.right = None
        self.room = None

    def search(self, root, data):
        s = Stack([root])
        while(s.size() != 0):
            curr = s.pop()
            if(data < curr.val.id):
                s.push(curr.left)
                if(curr.left is None):
                    return curr.val
            elif(data > curr.val.id):
                s.push(curr.right)
                if(curr.right is None):
                    return curr.val
            else:
                return curr.val

    def printTree(self, node, level = 0):
        if node != None:
            self.printTree(node.right, level + 1)
            print('     ' * level, node.val)
            self.printTree(node.left, level + 1)


    def list_to_bst(self, list_nums):
        if(len(list_nums) == 0):
            return None

        mid = (len(list_nums)) // 2
        node = Tree(list_nums[mid])
        node.left = self.list_to_bst(list_nums[:mid])
        node.right = self.list_to_bst(list_nums[mid+1:])
        return node
