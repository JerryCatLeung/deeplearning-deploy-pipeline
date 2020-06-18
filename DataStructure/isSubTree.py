# -*- coding: utf-8 -*-

"""
   判断一棵树是两一颗的子树
"""


############## 方案一 ##############
# 通过任意的顺序遍历两棵树，如果一棵树的遍历结果是另一棵树的字串，返回True；否则，返回False
def pre_order(root, result):
    if root:
        result.append(str(root._value))
        pre_order(root._left, result)
        pre_order(root._right, result)


def isSubTree(s, t):
    s_result = []
    t_result = []

    pre_order(s, s_result)
    pre_order(t, t_result)

    return ''.join(t_result) in ''.join(s_result)


############## 方案二 ##############
# 遍历二叉树A，定位B的根节点在A中可能的位置；定位后，验证B是不是A当前位置的子结构
# 三种情况：
#     1、t就是s本身
#     2、t是s的左子树
#     3、t是s的右子树
def isSame(s, t):
    if s and t:
        return s._value == t._value and isSame(t._left, s._left) and isSame(t._right, s._right)
    elif s == t:
        return True
    else:
        return False


def subTree(s, t):
    if not s:
        return False
    return isSame(s, t) or subTree(s._left, t) or subTree(s._right, t)
