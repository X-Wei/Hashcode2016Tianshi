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
        return sum(self.dmd)
    def __cmp__(self, other):# self-defined compare: first compare by nb_types(), if equal, compare order_weight()
        nt1,nt2 = self.nb_types(), other.nb_types()
        if nt1!=nt2: return nt1-nt2
        else: return self.total_weight() - other.total_weight()

class Drone:
    def __init__(self, r, c, w):
        self.r, self.c = r, c # location of drone
        self.coord = (r,c)
        self.load = w # the weight that is already on the drone
        self.cargo = [0 for _ in xrange(P)] # cargo[p] is nb of prod-p on drone

r0,c0 = warehouse[0]
drones = [ Drone(r0,c0,0) for _ in xrange(D) ]

orders = []
for i in xrange(C):
    r,c = order[i]
    orders.append( Order(i,r,c,demand[i]) )

from Queue import PriorityQueue
pq_orders = PriorityQueue()
for od in orders: 
    pq_orders.put(od) # the order with least nb of types is on top of pq

def nearest_wh(od, p): # find the nearest warehouse that have the required nb of product-p for order `od`
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
    for i in xrange(D):
        dr = drones[i]# first want a drone that can satisfy the demand on its own
        if MaxLoad-dr.load < n*weight[p]: continue
        d = dist(warehouse[wh], dr.coord)
        if d<min_d: 
            min_d=d
            res = i
    if res!=-1: return res, n
    # if such drone do not exists -- find one that have the most capacity
    max_cap,min_d = -1, 999999999
    for i in xrange(W):
        dr = drones[i]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap: continue 
        if cap==max_cap: # if capacities are the same --> take the nearer one
            d = dist(warehouse[wh], dr.coord)
            if d<min_d: 
                res = i
                min_d = d
        elif cap>max_cap: 
            max_cap = cap
            res = i
            min_d = dist(warehouse[wh], dr.coord)
    return res, max_cap
    

commands = [] # list of instructions
while not pq_orders.empty(): # treat orders one by one
    #~ print od.id
    od = pq_orders.get() # satisfy order `od`
    cmds = []
    for p in xrange(P): # satisfy demand for product-p
        while od.dmd[p]>0:
            wh_id,nb = nearest_wh(od, p)
            while nb>0: 
                dr_id, nb_i = nearest_drone(wh_id, p, nb)
                nb -= nb_i
                od.dmd[p] -= nb_i
                stock[wh_id][p] -= nb_i
                dr = drones[dr_id]
                dr.cargo[p] += nb_i
                dr.load += nb_i*weight[p]
                dr.coord = warehouse[wh_id]
                cmd = '%d L %d %d %d' % (dr_id, wh_id, p, nb_i) # load
                cmds.append(cmd)
        # now all demand product-p are loaded on drones: deliver!
        for dr_id in xrange(D):
            dr = drones[dr_id]
            if dr.load==0: continue
            for p in xrange(P):
                if dr.cargo[p]==0: continue
                cmd = '%d D %d %d %d' % (dr_id, od.id, p, dr.cargo[p]) # deliver
                cmds.append(cmd)
                dr.load -= dr.cargo[p]*weight[p]
                dr.cargo[p] = 0
                dr.coord = od.coord
        # satisfy demand for product-p
    commands.extend(cmds) # satisfy order `od`
    if len(commands)>6000: break

print len(commands)
for cmd in commands:
    print cmd
