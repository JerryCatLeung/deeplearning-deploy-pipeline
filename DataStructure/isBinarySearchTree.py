# -*- coding: utf-8 -*-


# 是否是二叉搜索树
def isValid(root, min, max):
    if not root:
        return True
    if min is not None and root._value <= min:
        return False
    if max is not None and root._value >= max:
        return False
    return isValid(root._left, min, root._value) and isValid(root._right, root._value, max)


def isBST(root):
    return isValid(root, None, None)
