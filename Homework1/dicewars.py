#!/usr/bin/env python3
import numpy as np

def F(m,n):
    if m < 1 or n < m:
        return 0
    if m == 1:
        return 0 if n > 6 else 1
    else:
        return sum([F(m-1,n-i) for i in [1,2,3,4,5,6]])

def P(m,n):
    return F(m,n) / 6**m

def tie(m,k):
    n1 = np.arange(m,6*m + 1, 1)
    n2 = np.arange(k, 6*k + 1, 1)
    return sum([P(m,n) * P(k,n) for n in n1 if n in n2])

def win(m,k):
    if m > k:
        win_prob_flipped = win(k,m)
        tie_prob_flipped = tie(k,m)
        return 1 - win_prob_flipped - tie_prob_flipped

    n1 = np.arange(m,6*m + 1, 1)
    n2 = np.arange(k, 6*k + 1, 1)

    return sum([P(k,i) * sum([P(m,j) for j in n1 if j > i]) for i in n2])


if __name__ == "__main__":
    tie_table = np.zeros(shape=(8,8))
    win_table = np.zeros(shape=(8,8))

    all_ms = all_ks = np.arange(1, 9, 1)
    for m in all_ms:
        for k in all_ks:
            print(m,k)
            tie_table[m-1][k-1] = tie(m,k)
            win_table[m-1][k-1] = win(m,k)
    
    np.set_printoptions(precision=6, suppress=True)
    print("Tie table:")
    print(tie_table) 
    print("Win table:")
    print(win_table) 
