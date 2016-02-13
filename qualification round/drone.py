from read_input import *
''' ***global vars: ***
Rows, Cols, D, T, MaxLoad
warehouse(coord), stock
order(coord), demand
drones, times
pq_orders
'''

def nearest_wh(od, p): # find the nearest warehouse that have product-p for order `od`
    min_d = 999999999
    res = -1 # if no sigle wh can satisfy this demand, return -1
    ### find one nearest WH 
    max_nb, min_d = -1, 999999999
    for w in xrange(W):
        if stock[w][p]<=0: continue # first want a WH that can satisfy the demand on its own
        dst = dist(warehouse[w], od.coord)
        if dst==min_d: 
            if max_nb < stock[w][p]:
                res = w
                max_nb = stock[w][p]
        elif dst<min_d: 
            min_d = dst
            res = w
            max_nb = stock[w][p]
    return res, min(max_nb, od.dmd[p])
    ###
    for w in xrange(W):
        if stock[w][p]<od.dmd[p]: continue # first want a WH that can satisfy the demand on its own
        dst = dist(warehouse[w], od.coord)
        if dst<min_d: 
            min_d=dst
            res = w
    if res!=-1: return res, od.dmd[p]
    max_nb, min_d = -1, 999999999 # if such WH do not exists -- find one that have the most nb of prod-p
    for w in xrange(W):
        if stock[w][p]<=0: continue 
        if stock[w][p]==max_nb: # if nb are the same --> take the nearer one
            dst = dist(warehouse[w], od.coord)
            if dst<min_d: 
                res = w
                min_d = dst
        elif stock[w][p]>max_nb: 
            max_nb = stock[w][p]
            res = w
            min_d = dist(warehouse[w], od.coord)
    return res, max_nb

def nearest_drone(w, p, n): # find the nearest drone that can carry `n` items of prod-p from warehouse `w`
    min_d = 999999999
    res = -1 # if no sigle drone can satisfy this demand, return -1
    '''# first: find the drones that have ***dist==0***
    max_cap = -1
    for d in xrange(D):
        dr = drones[d]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap==0: continue 
        dst = dist(warehouse[w], dr.coord)
        if dist>0: continue
        if cap>max_cap: 
            max_cap = cap
            res = d
    if res!=-1: return res, min(max_cap,n)
    # second: want a drone that can satisfy the demand on its own
    for d in xrange(D):
        dr = drones[d]
        if MaxLoad-dr.load < n*weight[p]: continue
        dst = dist(warehouse[w], dr.coord)
        if dst<min_d: 
            min_d=dst
            res = d
    if res!=-1: return res, n'''
    # if such drone do not exist -- find one that have the most capacity/min priority
    max_cap, min_priority = -1, 999999999
    for d in xrange(D):
        if times[d]>T: continue
        dr = drones[d]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap<=0: continue # UN BUG CON...
        priority = dist(warehouse[w], dr.coord)+times[d] # !!!the priority should be time[i]+distance!!!
        if priority==min_priority: # if have same priority --> take larger capacity
            if cap>max_cap: 
                res = d
                max_cap = cap
        elif priority<min_priority: 
            min_priority = priority
            max_cap = cap
            res = d
        #~ if cap==max_cap: # if capacities are the same --> take the one with smaller priority
            #~ if priority<min_priority: 
                #~ res = d
                #~ min_priority = priority
        #~ elif cap>max_cap: 
            #~ max_cap = cap
            #~ res = d
            #~ min_priority = priority
    return res, min(max_cap, n)

commands = [] # list of instructions
cmds = []

_orders = [od.id for od in sorted(all_orders)] # deliver in the same order as load
def deliver_drones():
    for d in xrange(D):
        dr = drones[d]
        if dr.load==0: continue
        for o in _orders:
            if len(dr.cargo[o])==0: continue # cargo[o] is a map: mapping p to the nb of items to send to order o=cargo[o][p]
            for p in dr.cargo[o]:
                od = all_orders[o]
                dst = dist(dr.coord, od.coord)
                times[d] += (dst+1)
                od.finish_time = max(od.finish_time, times[d])
                if times[d]>T: break
                cmd = '%d D %d %d %d' % (d, o, p, dr.cargo[o][p]) # deliver product p to order i
                cmds.append(cmd)
                #~ od.cmds.append(cmd)
                dr.load -= dr.cargo[o][p]*weight[p]
                dr.coord = order[o]
            dr.cargo[o] = {}

#~ def run():
while not pq_orders.empty(): # treat orders one by one
    cmds = []
    od = pq_orders.get() # satisfy order `od`
    #~ print od.id
    for p in xrange(P): # satisfy demand for product-p
        if od.dmd[p]==0: continue
        while od.dmd[p]>0:
            w,nb = nearest_wh(od, p)
            if nb<=0: print 'err: warehouse %d, nb=%d'%(w,nb)
            while nb>0: 
                d, nb_i = nearest_drone(w, p, nb)
                if d!=-1 and nb_i<=0: 
                    print 'err: nbi=%d'%nb_i
                if d==-1: 
                    deliver_drones()
                else: 
                    dr = drones[d]
                    dst = dist(dr.coord, warehouse[w])
                    times[d] += (dst+1)
                    nb -= nb_i
                    od.dmd[p] -= nb_i
                    stock[w][p] -= nb_i
                    dr.cargo[od.id][p] = nb_i
                    dr.load += nb_i*weight[p]
                    dr.coord = warehouse[w]
                    cmd = '%d L %d %d %d' % (d, w, p, nb_i) # load to drones
                    od.cmds.append(cmd)
                    cmds.append(cmd)
        # satisfy demand for product-p
    from random import random 
    #~ if random() <= sum([1 if dr.load==0 else 0 for dr in drones])*1.0/D:
    if random() <= ( sum([dr.load for dr in drones])*1.0 / (MaxLoad*D) )**0.5:
        deliver_drones()
    if min(times)>T : break 
    commands.extend(cmds) 

score = sum( od.score() for od in all_orders)
print int(score)

print len(commands)
for cmd in commands:
    print cmd

