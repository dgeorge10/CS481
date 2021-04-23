#!/usr/bin/env python3

import numpy as np
np.set_printoptions(suppress=True, precision=2, threshold=10000)

CHUTES_LADDERS = {1:38, 4:14, 9:31, 16:6, 21:42, 28:84, 36:44,
                  47:26, 49:11, 51:67, 56:53, 62:19, 64:60,
                  71:91, 80:100, 87:24, 93:73, 95:75, 98:78}

def get_matrix():
    mat = [[0 for j in range(101)] for i in range(101)]
    
    for i in range(101):
        for j in range(1,7):
            mat[i][i+j] = 1/6

    
    return mat
    


mat = get_matrix()
npmat = np.array(mat)
print(npmat)
