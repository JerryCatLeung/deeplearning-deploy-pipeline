# -*- coding: utf-8 -*-

"""回文链表"""
"""
   空间复杂度o(1)
   1、首先用快慢指针找到链表中部
   2、后半部分反转
   3、判断前半部分和后半部分相同位置的值是否一致
"""


def huiwenLinkedList(head):
    """

    :param head:
    :return:
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow._next
        fast = fast._next._next

    if fast._next:
        # 如果fast指针没有指向None，说明链表的长度为奇数
        slow = slow._next

    node = None
    while slow:
        nxt = slow._next
        slow._next = node
        node = slow
        slow = nxt

    while node and head:
        if node._value != head._value:
            return False
        node = node._next
        head = head._next
        return True
