Rows, Cols, D, T, MaxLoad = map(int , raw_input().split() )

P = int(raw_input()) # nb of product types
weight = map(int , raw_input().split() ) # weight[i]=weight for product-i, i=0..P-1
    
W = int(raw_input()) # nb of warehouses
warehouse = [] # warehouse[i] = (r,c), the location of warehouse i, i=0..W-1
stock = [] # stock[i][p] is the number of product-p in warehouse i, i=0..W-1
for _ in xrange(W):
    r,c = map(int , raw_input().split() )
    warehouse.append( (r,c) )
    stock_i = map(int , raw_input().split() )
    stock.append(stock_i)

C = int(raw_input()) # nb of orders
order = []  # order[i] = (r,c), the location of destination of order i, i=0..C-1
demand = [] # demand[i][p] is the number of product-p for order i, i=0..C-1
from collections import Counter
for _ in xrange(C):
    r,c = map(int , raw_input().split() )
    order.append( (r,c) )
    Li = int(raw_input())
    ctr = Counter( map(int , raw_input().split() ) )
    demand_i = [ ctr[i] for i in xrange(P) ]
    demand.append(demand_i)


from math import sqrt, ceil
def dist(a,b):
    r1,c1 = a
    r2,c2 = b
    return  ceil( sqrt((r1-r2)**2+(c1-c2)**2) )


class Drone:
    def __init__(self, r, c, w):
        self.r, self.c = r, c # location of drone
        self.coord = (r,c)
        self.load = w # the weight that is already on the drone
        self.cargo = [ {} for i in xrange(C)] # cargo[i] is a map: mapping p to the nb of items to send to order i

r0,c0 = warehouse[0]
drones = [ Drone(r0,c0,0) for _ in xrange(D) ]
times = [0 for _ in xrange(D)] # time used by drone


class Order: 
    def __init__(self, _id, r, c, demand_i):
        self.id = _id
        self.r, self.c = r, c # location of order
        self.coord = (r,c)
        self.dmd = demand_i # dmd[p] is the number of required product-p for order i, i=0..C-1
        self.finish_time = -1
        self.cmds = [] # list of commands for this order
    def nb_types(self): # return the nb of product types of this order
        return sum([1 if dmdi!=0 else 0 for dmdi in self.dmd ])
    def total_weight(self): # return total weight
        return sum([self.dmd[i]*weight[i] for i in xrange(P)])
    def __cmp__(self, other):# self-defined compare: first compare by nb_types(), if equal, compare order_weight()
        #~ return self.finish_time - other.finish_time
        #~ if self.r!=other.r: return self.r-other.r
        #~ else: return self.c-other.c
        nt1,nt2 = self.nb_types(), other.nb_types()
        tw1, tw2 = self.total_weight(), other.total_weight()
        #~ if nt1!=nt2: return nt1-nt2
        #~ else: return tw1-tw2
        if tw1!=tw2: return tw1-tw2
        else: return nt1-nt2

all_orders = []
from Queue import PriorityQueue
pq_orders = PriorityQueue()
for i in xrange(C):
    r,c = order[i]
    od = Order(i,r,c,demand[i])
    all_orders.append(od)
    pq_orders.put( od ) # the order with least nb of types is on top of pq
