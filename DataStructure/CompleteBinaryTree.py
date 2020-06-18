# -*- coding: utf-8 -*-

"""
   1、首先，什么是二叉树
   二叉树是指度为二的树，二叉树的每个节点最多只有两个子节点，且两个子节点有序

   二叉树的重要特性
   1）二叉树第i层上节点组多有2^(i-1)
   2）高度为k的二叉树中，最多有2^k - 1个节点
   3）二叉树的子树有左右之分，顺序不能颠倒
   4）若采用连续存储的方式存放二叉树，则节点与下标之间的关系：
        若某个节点的下标为i，则这个节点的父节点的下标为i/2
        若某个节点的下标为i，且节点的度为2，则这个节点的左子节点的下标为2 * i + 1，右子节点的下标为2 * i + 2

   2、满二叉树
   树最后一层没有任何子节点，其余每一层的所有节点都有两个子节点

   满二叉树的特性
   1）满二叉树的第i层的节点数为2^(i-1)个
   2）深度为k的满二叉树必有2^k - 1个节点 ，叶子数为2^(k-1)
   3）满二叉树中不存在度为1的节点，每一个分支点中都两棵深度相同的子树，且叶子节点都在最底层
   4）具有n个节点的满二叉树的深度为log2(n+1)

   3、完全二叉树
   如果二叉树的深度为k，则除第k层外其余所有层节点的度都为2，且叶子节点从左到右依次存在。
   也即是，将满二叉树的最后一层从左到右依次删除若干节点就得到完全二叉树。满二叉树是一棵特殊的完全二叉树，但完全二叉树不一定是满二叉树。

   完全二叉树的性质
   1）满二叉树是一棵特殊的完全二叉树，但完全二叉树不一定是满二叉树
   2）在满二叉树中最下一层，连续删除若干个节点得到完全二叉树
   3）在完全二叉树中，若某个节点没有左子树，则一定没有有子树。
   4）若采用连续储存的方式存放二叉树，则节点下标之间的关系（根节点下标为0）
        若某个节点的下标为 i ，则这个节点的父节点的下标为 i / 2
        若某个节点下标为 i ，且节点的度为2，则这个节点的左子节点的下标为 2 * i + 1 ，右子节点的下标为 2 * i + 2
"""


# 获取完全二叉树的所有节点
class Node(object):
    def __init__(self, data):
        self._value = data
        self._left = None
        self._right = None

    @property
    def get_left(self):
        return self._left

    @property
    def get_right(self):
        return self._right


##################### 方案一 #####################
def getNodeNums(root):
    if not root:
        return 0
    left_nums = getNodeNums(root.get_left)
    right_nums = getNodeNums(root.get_right)
    return left_nums + right_nums + 1


##################### 方案二 #####################
def mostLeftLevel(root, level):
    while root:
        level += 1
        root = root.get_left
    return level - 1


def bs(root, level, height):
    if level == height:
        return 1
    if mostLeftLevel(root.get_right, level + 1) == height:
        # 如果右子树的高度+1等于树的高度，那么左子树为满二叉树，可以
        # 用公式计算，递归计算右子树
        return 2 ** (height - level) + bs(root.right, level + 1, height)
    else:
        # 如果右子树的高度+1不等于树的高度，右子树为满二叉树，
        # 可以用公式计算，递归计算左子树
        return 2 ** (height - level - 1) + bs(root.left, level + 1, height)


def NodeNums(root):
    if not root:
        return 0
    return bs(root, 1, mostLeftLevel(root, 1))
