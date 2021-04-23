import random as rnd
import numpy as np
import dev_info as di
from copy import deepcopy

MAX_CONS_HOURS = 5 # maximum consecutive hours of activity
MAX_INACT = 5


def gen_pop(n: int):
    pop = []
    for _ in range(n):
        sol = np.zeros(24 * di.DEVICES_PER_HOUR)
        sumdev = deepcopy(di.HOURS_DEVICES)
        ind = 0
    
        while ind < len(sol):
            dev = rnd.randint(0, di.NUM_DEVICES - 1)
           
            while sumdev[dev] < 1:
                dev = rnd.randint(0, di.NUM_DEVICES - 1)
            
            maxdur = MAX_INACT
            if dev != 0:
                maxdur = min(sumdev[dev], MAX_CONS_HOURS)

            dur = rnd.randint(1, maxdur)
            sumdev[dev] -= dur
            
            for i in range(ind, min(ind + dur, len(sol))):
                sol[i] = dev
            
            ind += dur
    
        pop.append(sol)
                               
    

    return pop


