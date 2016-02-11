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
        if stock[i][p]<od.dmd[p]: continue
        d = dist(warehouse[i], od.coord)
        if d<min_d: 
            min_d=d
            res = i
    return res

def nearest_drone(od, p, wh): # find the nearest drone that can carry prod-p from warehouse wh
    min_d = 999999999
    res = -1 # if no sigle drone can satisfy this demand, return -1
    for i in xrange(D):
        dr = drones[i]
        if MaxLoad-dr.load < od.dmd[p]: continue
        d = dist(warehouse[wh], dr.coord)
        if d<min_d: 
            min_d=d
            res = i
    return res


commands = [] # list of instructions
while not pq_orders.empty(): # treat orders one by one
    od = pq_orders.get()
    success = True # indicates whether this order is satisfied or not 
    cmds = []
    for p in xrange(P): # satisfy demand for product-p
        if od.dmd[p]==0: 
            success = False
            break
        wh_id = nearest_wh(od, p)
        if wh_id==-1: # if cannot find such a wh --> just ignore this order
            success = False
            break
        dr_id = nearest_drone(od, p, wh_id)
        if dr_id==-1: continue
        cmd = '%d L %d %d %d' % (dr_id, wh_id, p, od.dmd[p]) # load
        cmds.append(cmd)
        dr = dr = drones[dr_id]
        dr.cargo[p] = od.dmd[p]
        dr.load += od.dmd[p]*weight[p]
        dr.coord = (warehouse[wh_id])
    if success==False: # treat next order if this order cannot be satisfied (TODO: didn't track back!)
        continue 
    for dr_id in xrange(D):
        if dr.load==0: continue
        for p in xrange(P):
            if dr.cargo[p]==0: continue
            cmd = '%d D %d %d %d' % (dr_id, od.id, p, dr.cargo[p]) # deliver
            cmds.append(cmd)
    commands.extend(cmds)

print len(commands)
for cmd in commands:
    print cmd



    

