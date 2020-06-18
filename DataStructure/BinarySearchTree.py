# -*- coding: utf-8 -*-
import random


#
#
# 二叉搜索树的各项操作
#
#


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST(object):
    def insert(self, root, value):
        if not root:
            root = TreeNode(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        elif value >= root.value:
            root.right = self.insert(root.right, value)
        return root

    def query(self, root, value):
        if not root:
            return False
        if root.value == value:
            return True
        elif value < root.value:
            return self.query(root.left, value)
        elif value >= root.value:
            return self.query(root.right, value)

    def findMin(self, root):
        if not root:
            return
        else:
            if root.left:
                return self.findMin(root.left)
            else:
                return root

    def findMax(self, root):
        if not root:
            return
        else:
            if root.right:
                return self.findMax(root.right)
            else:
                return root

    def delNode(self, root, value):
        if not root:
            return
        if value < root.value:
            root.left = self.delNode(root.left, value)
        elif value > root.value:
            root.right = self.delNode(root.right, value)
        else:
            """
            当value值等于根节点时，分为三种情况：
            1、只有左子树或者右子树
            2、左右子树都有
            3、左右子树都没有
            """
            if root.left and root.right:
                # 首先找到右子树的最小值节点
                temp = self.findMin(root.right)
                root.value = temp.value
                # 删除右子树的最小值节点
                root.right = self.delNode(root.right, temp.value)
            elif not root.left and not root.right:
                root = None
            elif not root.right:
                root = root.left
            elif not root.left:
                root = root.right

        return root

    def printTree(self, root):
        if not root:
            return
        self.printTree(root.left)
        print(root.value, end=",")
        self.printTree(root.right)


if __name__ == "__main__":
    a = [2, 2, 2, 2, 4, 5, 3, 2, 6, 8, 6, 5]
    # for i in range(1000):
    #    a.append(i)
    print("The number list before shuffling\n", a)
    random.shuffle(a)
    print("The number list after shuffling\n", a)
    root = None
    bst = BST()
    for val in a:
        root = bst.insert(root, val)

    print("")
    bst.printTree(root)
    print("")
    print(root.value)
    print("")
    while True:
        if bst.query(root, 2):
            root = bst.delNode(root, 2)
        else:
            break

    bst.printTree(root)
    print("")
