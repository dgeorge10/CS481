#!/usr/bin/env python3

import numpy as np
np.set_printoptions(suppress=True, precision=2)

CHUTES_LADDERS = {1:38, 4:14, 9:31, 16:6, 21:42, 28:84, 36:44,
                  47:26, 49:11, 51:67, 56:53, 62:19, 64:60,
                  71:91, 80:100, 87:24, 93:73, 95:75, 98:78}
	
def cl_markov_matrix():
    # Create the basic transition matrix:
    mat = np.zeros((101, 101))
    for i in range(101):
        mat[i + 1:i + 1 + 6, i] = 1. / 6 
        
    # rolls off the end of the board don't change the state;
    # add these probabilities to the diagonal
    mat[range(101), range(101)] += 1 - mat.sum(0)

    # account for the presence of chutes and ladders
    # we'll do this via  another transition matrix
    cl_mat = np.zeros((101, 101))
    ind = [CHUTES_LADDERS.get(i, i) for i in range(101)]
    cl_mat[ind, range(101)] = 1

    return cl_mat @ mat

mat = cl_markov_matrix()
np.savetxt("test.csv", mat, delimiter=",", fmt="%.3e")
