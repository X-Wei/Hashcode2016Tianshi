from read_input import *
from math import sqrt, ceil
''' ***global vars: ***
Rows, Cols, D, T, MaxLoad
warehouse(coord), stock
order(coord), demand
'''
def dist(a,b):
    r1,c1 = a
    r2,c2 = b
    return  ceil( sqrt((r1-r2)**2+(c1-c2)**2) )

class Order: 
    def __init__(self, _id, r, c, demand_i):
        self.id = _id
        self.r, self.c = r, c # location of order
        self.coord = (r,c)
        self.dmd = demand_i # dmd[p] is the number of required product-p for order i, i=0..C-1
    def nb_types(self): # return the nb of product types of this order
        return sum([1 if dmdi!=0 else 0 for dmdi in self.dmd ])
    def total_weight(self): # return total weight
        return sum([self.dmd[i]*weight[i] for i in xrange(P)])
    def __cmp__(self, other):# self-defined compare: first compare by nb_types(), if equal, compare order_weight()
        nt1,nt2 = self.nb_types(), other.nb_types()
        tw1, tw2 = self.total_weight(), other.total_weight()
        if nt1!=nt2: return nt1-nt2
        else: return tw1-tw2
        #~ if tw1!=tw2: return tw1-tw2
        #~ return nt1-nt2

class Drone:
    def __init__(self, r, c, w):
        self.r, self.c = r, c # location of drone
        self.coord = (r,c)
        self.load = w # the weight that is already on the drone
        self.cargo = [ [0 for _ in xrange(P)] for i in xrange(C)] # cargo[i][p] is nb of prod-p on drone for order[i]

r0,c0 = warehouse[0]
drones = [ Drone(r0,c0,0) for _ in xrange(D) ]
times = [0 for _ in xrange(D)] # time used by drone
orders = []
for i in xrange(C):
    r,c = order[i]
    orders.append( Order(i,r,c,demand[i]) )

from Queue import PriorityQueue
pq_orders = PriorityQueue()
for od in orders: 
    pq_orders.put(od) # the order with least nb of types is on top of pq

def nearest_wh(od, p): # find the nearest warehouse that have product-p for order `od`
    min_d = 999999999
    res = -1 # if no sigle wh can satisfy this demand, return -1
    for i in xrange(W):
        if stock[i][p]<od.dmd[p]: continue # first want a WH that can satisfy the demand on its own
        d = dist(warehouse[i], od.coord)
        if d<min_d: 
            min_d=d
            res = i
    if res!=-1: return res, od.dmd[p]
    # if such WH do not exists -- find one that have the most nb of prod-p
    max_nb,min_d = -1, 999999999
    for i in xrange(W):
        if stock[i][p]==0: continue 
        if stock[i][p]==max_nb: # if nb are the same --> take the nearer one
            d = dist(warehouse[i], od.coord)
            if d<min_d: 
                res = i
                min_d = d
        elif stock[i][p]>max_nb: 
            max_nb = stock[i][p]
            res = i
            min_d = dist(warehouse[i], od.coord)
    return res, max_nb

def nearest_drone(wh, p, n): # find the nearest drone that can carry `n` itmes of prod-p from warehouse `wh`
    min_d = 999999999
    res = -1 # if no sigle drone can satisfy this demand, return -1
    # first: find the drones that have ***dist==0***
    max_cap = -1
    for i in xrange(D):
        dr = drones[i]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap==0: continue 
        d = dist(warehouse[wh], dr.coord)
        if dist>0: continue
        if cap>max_cap: 
            max_cap = cap
            res = i
    if res!=-1: return res, min(max_cap,n)
    # second: want a drone that can satisfy the demand on its own
    for i in xrange(D):
        dr = drones[i]
        if MaxLoad-dr.load < n*weight[p]: continue
        d = dist(warehouse[wh], dr.coord)
        if d<min_d: 
            min_d=d
            res = i
    if res!=-1: return res, n
    # if such drone do not exists -- find one that have the most capacity
    max_cap,min_priority = -1, 999999999
    for i in xrange(D):
        dr = drones[i]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap==0: continue # UN BUG CON...
        priority = dist(warehouse[wh], dr.coord)+times[i] # !!!the priority should be time[i]+distance!!!
        if priority==min_priority: # if have same priority --> take larger capacity
            if cap>max_cap: 
                res = i
                max_cap = cap
        elif priority<min_priority: 
            min_priority = priority
            max_cap = cap
            res = i
        #~ if cap==max_cap: # if capacities are the same --> take the one with smaller priority
            #~ if priority<min_priority: 
                #~ res = i
                #~ min_priority = priority
        #~ elif cap>max_cap: 
            #~ max_cap = cap
            #~ res = i
            #~ min_priority = priority
    return res, max_cap

def all_drone_full():
    for dr in drones: 
        if dr.load<MaxLoad: return False
    return True

commands = [] # list of instructions
cmds = []

def deliver_drones():
    for dr_id in xrange(D):
        dr = drones[dr_id]
        if dr.load==0: continue
        for od_id in xrange(C):
            for p in xrange(P):
                if dr.cargo[od_id][p]==0: continue
                cmd = '%d D %d %d %d' % (dr_id, od_id, p, dr.cargo[od_id][p]) # deliver product p to order i
                cmds.append(cmd)
                dst = dist(dr.coord, od.coord)
                times[dr_id] += (dst+1)
                dr.load -= dr.cargo[od_id][p]*weight[p]
                dr.cargo[od_id][p] = 0
                dr.coord = order[od_id]

while not pq_orders.empty(): # treat orders one by one
    cmds = []
    od = pq_orders.get() # satisfy order `od`
    #~ print od.id
    for p in xrange(P): # satisfy demand for product-p
        if od.dmd[p]==0: continue
        while od.dmd[p]>0:
            wh_id,nb = nearest_wh(od, p)
            while nb>0: 
                dr_id, nb_i = nearest_drone(wh_id, p, nb)
                if dr_id==-1: 
                    deliver_drones()
                else: 
                    dr = drones[dr_id]
                    dst = dist(dr.coord, warehouse[wh_id])
                    times[dr_id] += (dst+1)
                    nb -= nb_i
                    od.dmd[p] -= nb_i
                    stock[wh_id][p] -= nb_i
                    dr.cargo[od.id][p] += nb_i
                    dr.load += nb_i*weight[p]
                    dr.coord = warehouse[wh_id]
                    cmd = '%d L %d %d %d' % (dr_id, wh_id, p, nb_i) # load to drones
                    cmds.append(cmd)
        # satisfy demand for product-p
    #~ deliver_drones()
    if max(times)>T : break # 
    commands.extend(cmds) # satisfy order `od`


print len(commands)
for cmd in commands:
    print cmd
