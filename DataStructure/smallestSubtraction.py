# -*- coding: utf-8 -*-


def bag(w):
    lengths = len(w)
    # 背包容量
    package_sum = sum(w) // 2
    dp = [[0] * (package_sum + 1) for _ in range(lengths + 1)]
    for i in range(1, lengths + 1):
        for j in range(1, package_sum + 1):
            dp[i][j] = dp[i - 1][j]
            if j > w[i - 1] and dp[i][j] < dp[i - 1][j - w[i - 1]] + w[i - 1]:
                dp[i][j] = dp[i - 1][j - w[i - 1]] + w[i - 1]
    return dp


def show(w, dp):
    x = [False for _ in range(len(w))]
    j = sum(w) // 2
    for i in range(len(w), 0, -1):
        if dp[i][j] > dp[i - 1][j]:
            x[i - 1] = True
            j -= w[i - 1]
    a = []
    for i in range(len(w)):
        if x[i]:
            a.append(w[i])
    return a


a = [2, 3, 3, 3, 3, 2]
b = bag(a)
c = show(a, b)
print(c)
