import sys

# these are the global variables that can be used in painting.py
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
for _ in xrange(W):
    r,c = map(int , raw_input().split() )
    order.append( (r,c) )
    Li = int(raw_input())
    ctr = Counter( map(int , raw_input().split() ) )
    demand_i = [ ctr[i] for i in xrange(P) ]
    demand.append(demand_i)
