import numpy as np

import random as rnd
rnd.seed(1)

from copy import deepcopy

import prod_predict as pp
import cons_predict as cp
import dev_info as di
import gen_pop as gp
import pymongo

# indicates how much energy will be
# generated each hour by renewable
# sources
HOURLY_PROD = pp.get_hourly_prod()

# used for selection
ROULETTE = None

CROSSOVER_PROB = 0.8

MUTATION_PROB = 0.02
MUTATION_SWAP_SIZE = 5


# my fave binary search 
def bi_se(val: int, h):
    l, r = 0, len(h) - 1
    while l < r:
        lm = int((l + r) / 2)
        if h[lm] < val:
            l = lm + 1
        else:
            r = lm

    return l - (val != h[l])


# evaluate the solution using the 
# consumption estimator and comparing
# it to the HOURLY_PROD 
def fitness_func(sol):
    hourly_cons = cp.get_hourly_cons(sol) 
    score = 0
    
    for h in range(24):
        # add to score the percentage of the needed
        # energy covered by renewable sources in that hour
        score += hourly_cons[h] / HOURLY_PROD[h];  
    
    return score


def selection():
    rand = rnd.randint(0, int(ROULETTE[-1]))
    return bi_se(rand, ROULETTE)


def crossover(p1, p2):
    prob = rnd.random()

    if prob < CROSSOVER_PROB:
        p3 = np.zeros(24 * di.DEVICES_PER_HOUR)
        # these could be zeroes, SURE
        sumdevp3 = deepcopy(di.HOURS_DEVICES)
        
        point = rnd.randint(0, len(p3))

        for i in range(point):
            p3[i] = p1[i]
            sumdevp3[int(p3[i])] -= 1
        
        for i in range(point, len(p3)):
            if sumdevp3[int(p2[i])] >= 1:
                p3[i] = p2[i]
                sumdevp3[int(p2[i])] -= 1
        
        return p3
    
    return []
        

def mutation(sol):
    prob = rnd.random()

    if prob < MUTATION_PROB:
        swap_size = rnd.randint(0, MUTATION_SWAP_SIZE)
        ind1 = rnd.randint(0, len(sol) - swap_size)
        ind2 =  rnd.randint(0, len(sol) - swap_size)
        
        tmp = deepcopy(sol[ind1: ind1 + swap_size])
        for i in range(swap_size):
            sol[i + ind1] = sol[i + ind2]

        for i in range(swap_size):
            sol[i + ind2] = tmp[i]
        
    
    # more like pass by ASSignment 
    return sol
        



def main(pop_size: int, max_iters: int):
    pop = gp.gen_pop(pop_size)
    

    while max_iters >= 0:
        max_iters -= 1
        
        sol_score = fitness_func(pop[0])
        max_score = sol_score

        global ROULETTE
        ROULETTE = [sol_score]
        

        for i in range(1, len(pop)):
            sol_score = fitness_func(pop[i])
            max_score = max(sol_score, max_score)
            ROULETTE.append(sol_score + ROULETTE[i - 1])
        
        print("max_iters:", max_iters, "max_score:", max_score)
        new_pop = []

        while len(new_pop) < len(pop):
            p1 =pop[selection()]
            p2 = pop[selection()]

            p3 = crossover(p1, p2)
            if len(p3) > 0:
                p3 = mutation(p3)
                new_pop.append(p3)    
        pop = new_pop

    best = None
    best_score = 0
    for sol in pop:
        score = fitness_func(sol)
        if score > best_score:
            best_score = score
            best = sol
    return best        


best = main(200, 10000)
best = best.reshape((24, di.DEVICES_PER_HOUR))
print(best)

horario = {}
for i in range(24):
    label = f"hora_{i+1}"
    horario[label] = []
    for d in best[i]:
        if int(d) != 0:
            horario[label].append(di.DEVICE_NAMES[int(d)])
print(horario)


client = pymongo.MongoClient("mongodb+srv://luis:bbkNOQ65@scrapping.w5sjz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.integrador
db.schedule.delete_many({})
db.schedule.insert_one(horario)