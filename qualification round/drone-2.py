from read_input import *

def nearest_wh(od, p): # find the nearest warehouse that have product-p for order `od`
    res = -1 # if no sigle wh can satisfy this demand, return -1
    ### find one nearest WH 
    max_nb, min_d = -1, 999999999
    for w in xrange(W):
        if stock[w][p]<=0: continue 
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

def nearest_drone(w, p, n): # find the nearest drone that can carry `n` items of prod-p from warehouse `w`
    res = -1 # if no sigle drone can satisfy this demand, return -1
    # find one drone with smallest time(priority)
    max_cap, min_priority = -1, 999999999 
    for d in xrange(D):
        dr = drones[d]
        cap = (MaxLoad-dr.load)//weight[p]
        if cap<=0: continue 
        priority = dist(warehouse[w], dr.coord)+times[d] # !!!the priority should be time[i]+distance!!!
        if priority==min_priority: # if have same priority --> take larger capacity
            if cap>max_cap: 
                res = d
                max_cap = cap
        elif priority<min_priority: 
            min_priority = priority
            max_cap = cap
            res = d
    return res, min(max_cap, n)

commands = [] # list of instructions
cmds = []

def deliver_drones():
    for d in xrange(D):
        dr = drones[d]
        if dr.load==0: continue
        for o in xrange(C):
            if len(dr.cargo[o])==0: continue # cargo[o] is a map: mapping p to the nb of items to send for order o=cargo[o][p]
            for p in dr.cargo[o]:
                cmd = '%d D %d %d %d' % (d, o, p, dr.cargo[o][p]) # deliver product p to order i
                cmds.append(cmd)
                od = all_orders[o]
                dst = dist(dr.coord, od.coord)
                times[d] += (dst+1)
                #~ od.cmds.append(cmd)
                od.finish_time = max(od.finish_time, times[d])
                dr.load -= dr.cargo[o][p]*weight[p]
                dr.coord = order[o]
            dr.cargo[o] = {}

def __nearest_wh(od):
    res, min_dst = -1, 999999999
    for w in xrange(W):
        if sum(stock[w])==0: continue
        dst = dist(warehouse[w], od.coord)
        if dst < min_dst: res, min_dst = w, dst
    return res, min_dst

def __nearest_dr(w):
    res, min_dst = -1, 999999999
    for d in xrange(D):
        dr = drones[d]
        if MaxLoad-dr.load < min(weight): continue
        dst = dist(warehouse[w], dr.coord)
        if dst < min_dst: res, min_dst = w, dst
    return res, min_dst

from copy import deepcopy # pretty SLOW......
def estimate_finishtime(od, min_ft):
    global times, drones, stock, cmds
    # speedup: let's estimate a (very loose) lower bound of the finish time for this order!
    w, min_wh_dst = __nearest_wh(od)
    d, min_dr_dst = __nearest_dr(w)
    sum_dmd = sum(od.dmd)
    max_cap = MaxLoad - min([dr.load for dr in drones])
    min_turns = sum_dmd/(MaxLoad*D) + 1
    if min(times) + od.nb_types()*2*min_turns + min_wh_dst*(min_turns*2-1) + min_dr_dst > min_ft: 
        return 999999999
    # copy vars to restore states later on...
    _times = times[:] 
    _cmds = cmds[:]
    _stock = deepcopy(stock)
    _drones = deepcopy(drones)
    _od = deepcopy(od)
    for p in xrange(P): # satisfy demand for product-p
        dmd_p = od.dmd[p]
        while dmd_p>0:
            w,nb = nearest_wh(od, p)
            if nb<=0: print 'err: warehouse %d, nb=%d'%(w,nb)
            while nb>0: 
                d, nb_i = nearest_drone(w, p, nb)
                if d!=-1 and nb_i<=0: print 'err: nbi=%d'%nb_i
                if d==-1: 
                    deliver_drones()
                else: 
                    dr = drones[d]
                    dst = dist(dr.coord, warehouse[w])
                    times[d] += (dst+1)
                    nb -= nb_i
                    dmd_p -= nb_i
                    stock[w][p] -= nb_i
                    dr.cargo[od.id][p] = nb_i
                    dr.load += nb_i*weight[p]
                    dr.coord = warehouse[w]
        # demand p is satisfied
    deliver_drones()
    # od is satisfied 
    # restore states
    res = od.finish_time
    od = _od
    drones = _drones
    stock = _stock
    times = _times
    cmds = _cmds
    return res

def next_order():
    min_finishtime = 999999999
    res = None
    for od in all_orders:
        if od.finished()==True: continue
        ft = estimate_finishtime(od, min_finishtime)
        if ft < min_finishtime: 
            min_finishtime = ft
            res = od
    return res, min_finishtime

for _ in xrange(C):
    cmds = []
    od, ft = next_order() # get the easiest order
    if ft>T: break
    print od.id, ft
    for p in xrange(P): # satisfy demand for product-p
        if od.dmd[p]==0: continue
        while od.dmd[p]>0:
            w,nb = nearest_wh(od, p)
            if nb<=0: print 'err: warehouse %d, nb=%d'%(w,nb)
            while nb>0: 
                d, nb_i = nearest_drone(w, p, nb)
                if d!=-1 and nb_i<=0: print 'err: nbi=%d'%nb_i
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
                    #~ od.cmds.append(cmd)
                    cmds.append(cmd)
        # satisfy demand for product-p
    deliver_drones()
    #~ if max(times)>T : break 
    commands.extend(cmds) 

score = sum( ceil( (T-od.finish_time)*100.0/T ) if T>=od.finish_time>=0 else 0 for od in all_orders)
print int(score)

print len(commands)
for cmd in commands:
    print cmd

