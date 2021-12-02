class AVLNode:
    def __init__(self, val):
        self.val = val
        self.height = 0
        self.left = None
        self.right = None

class Tree:
    def insertAVL(self, items, threshold):
        '''
        :type items: list of int
        :type threshold: int
        :rtype: TreeNode
        '''
        if not items:
            return None

        root = AVLNode(items[0])

        for idx in range(1, len(items)):
            root = self.insert(root, items[idx], threshold)

        # O(n) conversion for testing reasons
        return self.convert_avl_nodes_to_treenode(root)

    def insert(self, node, key, threshold):
        if not node:
            return AVLNode(key)

        if (key < node.val):
            node.left = self.insert(
                node.left, key, threshold)  # insert to the left
        else:  # key >= node.val
            node.right = self.insert(node.right, key, threshold)

        # When we return to this node going up in the recursion
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > threshold:  # Did we create a left imbalance? > threshold, positive
            if self.get_balance(node.left) >= 0:
                node = self.rotate_right(node)
            else:
                node = self.rotate_left_right(node)  # node.left is right-heavy
        elif balance < -threshold:  # Did we create a right imbalance? < -threshold, negative
            if self.get_balance(node.right) <= 0:
                node = self.rotate_left(node)
            else:
                node = self.rotate_right_left(node)  # node.right is left-heavy

        return node

    # For left-heavy rebalance
    def rotate_right(self, node):
        left_temp = node.left

        node.left = left_temp.right
        left_temp.right = node

        # Update heights of rotated nodes based on subtree heights
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))
        left_temp.height = 1 + max(self.get_height(left_temp.left),
                                   self.get_height(left_temp.right))

        return left_temp

    # For right-heavy rebalance
    def rotate_left(self, node):
        right_temp = node.right

        node.right = right_temp.left
        right_temp.left = node

        # Update heights of rotated nodes based on subtree heights
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))
        right_temp.height = 1 + max(self.get_height(right_temp.left),
                                    self.get_height(right_temp.right))

        return right_temp

    # For left-heavy rebalance (& node.left has negative balance, right-heavy)
    def rotate_left_right(self, node):
        node.left = self.rotate_left(node.left)

        return self.rotate_right(node)

    # For right-heavy rebalance (& node.right has positive balance, left-heavy)
    def rotate_right_left(self, node):
        node.right = self.rotate_right(node.right)

        return self.rotate_left(node)

    def get_balance(self, node):
        if not node:
            return 0

        return self.get_height(node.left) - self.get_height(node.right)

    def get_height(self, node):
        if not node:
            return -1

        return node.height