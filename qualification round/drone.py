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
    for w in xrange(W):
        if stock[w][p]<od.dmd[p]: continue # first want a WH that can satisfy the demand on its own
        d = dist(warehouse[w], od.coord)
        if d<min_d: 
            min_d=d
            res = w
    if res!=-1: return res, od.dmd[p]
    max_nb,min_d = -1, 999999999 # if such WH do not exists -- find one that have the most nb of prod-p
    for w in xrange(W):
        if stock[w][p]==0: continue 
        if stock[w][p]==max_nb: # if nb are the same --> take the nearer one
            dst = dist(warehouse[w], od.coord)
            if dst<min_d: 
                res = w
                min_d = dst
        elif stock[w][p]>max_nb: 
            max_nb = stock[i][p]
            res = w
            min_d = dist(warehouse[w], od.coord)
    return res, max_nb

def nearest_drone(w, p, n): # find the nearest drone that can carry `n` itmes of prod-p from warehouse `w`
    min_d = 999999999
    res = -1 # if no sigle drone can satisfy this demand, return -1
    # first: find the drones that have ***dist==0***
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
    if res!=-1: return res, n
    # if such drone do not exist -- find one that have the most capacity/min priority
    max_cap,min_priority = -1, 999999999
    for d in xrange(D):
        dr = drones[d]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap==0: continue # UN BUG CON...
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
    return res, max_cap

commands = [] # list of instructions
cmds = []

def deliver_drones():
    for d in xrange(D):
        dr = drones[d]
        if dr.load==0: continue
        for o in xrange(C):
            if len(dr.cargo[o])==0: continue # cargo[o] is a map: mapping p to the nb of items to send to order o=cargo[o][p]
            for p in dr.cargo[o]:
                cmd = '%d D %d %d %d' % (d, o, p, dr.cargo[o][p]) # deliver product p to order i
                cmds.append(cmd)
                od = all_orders[o]
                dst = dist(dr.coord, od.coord)
                times[d] += (dst+1)
                od.cmds.append(cmd)
                od.finish_time = max(od.finish_time, times[d])
                dr.load -= dr.cargo[o][p]*weight[p]
                dr.coord = order[o]
            dr.cargo[o] = {}

while not pq_orders.empty(): # treat orders one by one
    cmds = []
    od = pq_orders.get() # satisfy order `od`
    #~ print od.id
    for p in xrange(P): # satisfy demand for product-p
        if od.dmd[p]==0: continue
        while od.dmd[p]>0:
            w,nb = nearest_wh(od, p)
            while nb>0: 
                d, nb_i = nearest_drone(w, p, nb)
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
    #~ if max(times)>T : break 
    commands.extend(cmds) 

#~ import cPickle as pickle
#~ finish_times = [od.finish_time for od in all_orders] 
#~ pickle.dump( finish_times, open( "finish_times.pk", "wb" ) )

#~ commands=[]
#~ for o in xrange(C):
    #~ od = all_orders[o]
    #~ if od.finish_time<0 or od.finish_time>T: continue
    #~ commands.extend(od.cmds)

print len(commands)
for cmd in commands:
    print cmd
