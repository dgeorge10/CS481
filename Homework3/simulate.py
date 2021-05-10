#!/usr/bin/env python3
import numpy as np

Pa = np.array(( 
    [0, 1/4, 1/4, 1/4, 1/4, 0],
    [0, 0, 1/4, 1/4, 1/4, 1/4],
    [0, 0, 0, 1/4, 1/4, 1/2],
    [0, 0, 0, 0, 1/4, 3/4],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
));


Pc = np.array(( 
    [0, 1/4, 1/4, 1/4, 1/4, 0],
    [0, 0, 1/4, 1/4, 1/4, 1/4],
    [0, 0, 0, 1/4, 1/4, 1/2],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
));

current = Pc

iterations = 10000

for starting_state in range(6):
    X = np.zeros(iterations)
    print("starting state:", starting_state)
    X[0] = starting_state #np.random.choice(np.array([0,1,2,3,4,5]), size=1, replace=False)
    
    for i in range(1, iterations):
        index = int(X[i-1])
        if index == 5 or index == 4 or index == 3:
            index = 0
        X[i] = np.random.choice(np.array([0,1,2,3,4,5]), size=1, replace=False, p=current[index])
    
    scores = {}
    for item in X:
        if item in scores:
            scores[item] += 1
        else:
            scores[item] = 1
    print(scores)
    
    for score in scores:
        print("state:", int(score),  ": ", scores[score] / iterations)
    
