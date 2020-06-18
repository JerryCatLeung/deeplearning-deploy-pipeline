class Node(object):
    def __init__(self, name=None, value=None):
        self._name = name
        self._value = value
        self._left = None
        self._right = None

    @property
    def get_value(self):
        return self._value

    @property
    def get_name(self):
        return self._name

    @property
    def get_left(self):
        return self._left

    @property
    def get_right(self):
        return self._right


class HuffmanTree(object):
    def __init__(self, weights):
        self.leaves = [Node(part[0], part[1]) for part in weights]
        while len(self.leaves) != 1:
            self.leaves.sort(key=lambda node: node.get_value, reverse=True)
            c = Node(value=(self.leaves[-1].get_value + self.leaves[-2].get_value))
            c._left = self.leaves.pop(-1)
            c._right = self.leaves.pop(-1)
            self.leaves.append(c)
        self.root = self.leaves[0]
        self.Buffer = list(range(10))

    def pre(self, root, length):
        node = root
        if not node:
            print("树为空")
            return None
        elif node.get_name:
            "判断节点是否为原始节点，如果是原始节点一定为叶子节点，打印编码后返回；如果是由最小的结点生成，则不走一下逻辑"
            print(node.get_name + '\'s encoding:', end='')
            for i in range(length):
                print(self.Buffer[i], end='')
            print("\n")
            return None

        self.Buffer[length] = 0
        self.pre(node.get_left, length + 1)
        self.Buffer[length] = 1
        self.pre(node.get_right, length + 1)

    def get_code(self):
        self.pre(self.root, 0)


if __name__ == '__main__':
    char_weights = [("a", 6), ("b", 4), ("c", 10), ("d", 8), ("f", 12), ("g", 2), ("z", 34)]
    tree = HuffmanTree(char_weights)
    tree.get_code()
