from collections import Counter


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 0


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert_root(self, value):
        self.root = Node(value)

    def insert_left(self, node, value):
        node.left = Node(value)

    def insert_right(self, node, value):
        node.right = Node(value)

    def delete_left(self, node):
        node.left = None

    def delete_right(self, node):
        node.right = None

    def delete_root(self):
        self.root = None


class AVLTree(BinaryTree):
    def __init__(self):
        super().__init__()
        self.rotation_counts = Counter()
        self.node_count = 0

    def reset_rotation_counts(self):
        self.rotation_counts = Counter()

    def get_height(self, node):
        if node is None:
            return -1
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        self.rotation_counts["Left"] += 1

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        self.rotation_counts["Right"] += 1

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def LR_rotate(self, node):
        self.rotation_counts["Left-Right"] += 1
        node.left = self.left_rotate(node.left)
        return self.right_rotate(node)

    def RL_rotate(self, node):
        self.rotation_counts["Right-Left"] += 1
        node.right = self.right_rotate(node.right)
        return self.left_rotate(node)

    def insert(self, node, value):
        if node is None:
            self.node_count += 1
            return Node(value)

        if value < node.value:
            node.left = self.insert(node.left, value)
        elif value > node.value:
            node.right = self.insert(node.right, value)
        else:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        if balance > 1 and value > node.left.value:
            return self.LR_rotate(node)

        if balance < -1 and value < node.right.value:
            return self.RL_rotate(node)

        return node

    def search(self, node, value):
        current = node
        while current is not None:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def min_value_node(self, node):
        current = node
        while current and current.left is not None:
            current = current.left
        return current

    def delete(self, node, value):
        if node is None:
            return node

        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        else:
            if node.left is None and node.right is None:
                self.node_count -= 1
                return None
            elif node.left is None:
                self.node_count -= 1
                return node.right
            elif node.right is None:
                self.node_count -= 1
                return node.left
            else:
                successor = self.min_value_node(node.right)
                node.value = successor.value
                node.right = self.delete(node.right, successor.value)

        if node is None:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        if balance > 1 and self.get_balance(node.left) < 0:
            return self.LR_rotate(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        if balance < -1 and self.get_balance(node.right) > 0:
            return self.RL_rotate(node)

        return node
