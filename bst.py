class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BSTree:
    def __init__(self):
        self.root = None
        self.node_count = 0

    def insert(self, node, value):
        if node is None:
            self.node_count += 1
            return Node(value)

        current = node
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    self.node_count += 1
                    return node
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    self.node_count += 1
                    return node
                current = current.right
            else:
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

        parent = None
        current = node
        while current is not None and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if current is None:
            return node

        left_of_parent = parent is not None and parent.left is current

        if current.left is None and current.right is None:
            self.node_count -= 1
            if parent is None:
                return None
            if left_of_parent:
                parent.left = None
            else:
                parent.right = None
            return node

        if current.left is None:
            self.node_count -= 1
            replacement = current.right
            if parent is None:
                return replacement
            if left_of_parent:
                parent.left = replacement
            else:
                parent.right = replacement
            return node

        if current.right is None:
            self.node_count -= 1
            replacement = current.left
            if parent is None:
                return replacement
            if left_of_parent:
                parent.left = replacement
            else:
                parent.right = replacement
            return node

        parent = current
        child = current.right
        while child.left is not None:
            parent = child
            child = child.left

        current.value = child.value

        if parent is current:
            parent.right = child.right
        else:
            parent.left = child.right
        self.node_count -= 1
        return node

    def get_height(self, node):
        if node is None:
            return -1
        best = -1
        stack = [(node, 0)]
        while stack:
            n, edges = stack.pop()
            if n.left is None and n.right is None:
                best = max(best, edges)
            else:
                if n.left is not None:
                    stack.append((n.left, edges + 1))
                if n.right is not None:
                    stack.append((n.right, edges + 1))
        return best
