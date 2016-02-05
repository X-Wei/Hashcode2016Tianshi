import sys
import Queue
#~ filename,comment = sys.argv[1:3]

N,M = map( int, raw_input().split() )
img = [] # array of string (each line)
res = [] # instructions
marked = [ [False for i in xrange(M)] for j in xrange(N)]
for line in sys.stdin:
    img.append(line)

def is_valid_sq(r,c,s):
    if not (r-s>=0 and c-s>=0 and r+s<=N-1 and c+s<=M-1): 
        return False
    for i in xrange(r-s, r+s+1):
        for j in xrange(c-s,c+s+1):
            if img[i][j]=='.': return False
    return True

def max_valid_s(r,c):
    s = 0
    while ( is_valid_sq(r,c,s) ) : s+=1
    return s-1

def max_valid_horizontal_line(r,c):
    r2,c2=r,c
    while ( 0<=c2<=M-1 and img[r2][c2]=='#' ): c2+=1
    return r2,c2-1

def max_valid_vertical_line(r,c):
    r2,c2=r,c
    while ( 0<=r2<=N-1 and img[r2][c2]=='#' ): r2+=1
    return r2-1,c2

def max_valid_line(r,c):
    r2,c2=r,c
    while ( 0<=r2<=N-1 and img[r2][c]=='#' ): r2+=1
    while ( 0<=c2<=M-1 and img[r][c2]=='#' ): c2+=1
    if r2-r > c2-c: return r2-1,c  
    else: return r,c2-1

def mark_sq(r,c,s):
    for i in xrange(r-s, r+s+1):
        for j in xrange(c-s,c+s+1):
            marked[i][j]=True

def mark_line(r1,c1,r2,c2):
    for i in xrange(r1,r2+1):
        for j in xrange(c1,c2+1):
            marked[i][j]=True

# greedy algo for using paint square instruction and nothing else
def greedy_sq():
    pq = Queue.PriorityQueue() # maxpq: squares with largest `s` is on top
    for r in xrange(N):
        for c in xrange(M):
            char = img[r][c]
            if char=='#': 
                s = max_valid_s(r,c)
                cmd = "PAINT_SQUARE %d %d %d" % (r,c,s)
                pq.put( (-s,r,c,cmd) ) 
            else: pass
    while not pq.empty():
        s,r,c,cmd = pq.get()
        s *= -1
        if marked[r][c]: continue
        mark_sq(r,c,s)
        res.append( cmd )

def greedy_line():
    pq = Queue.PriorityQueue() 
    for r in xrange(N):
        for c in xrange(M):
            char = img[r][c]
            if char=='#': 
                r2,c2 = max_valid_line(r,c)
                l = max(r2-r, c2-c)
                cmd = "PAINT_LINE %d %d %d %d" % (r,c,r2,c2)
                pq.put( (-l,r,c,r2,c2,cmd) ) 
            else: pass
    while not pq.empty():
        _,r,c,r2,c2,cmd = pq.get()
        if marked[r][c]: continue
        mark_line(r,c,r2,c2)
        res.append( cmd )

def greedy_line_and_sq():
    pq = Queue.PriorityQueue() 
    for r in xrange(N):
        for c in xrange(M):
            char = img[r][c]
            if char=='#': 
                r2,c2 = max_valid_line(r,c)
                l = max(r2-r, c2-c)+1
                cmd = "PAINT_LINE %d %d %d %d" % (r,c,r2,c2)
                pq.put( (-l,r,c,r2,c2,cmd) ) 
            else: pass
    for r in xrange(N):
        for c in xrange(M):
            char = img[r][c]
            if char=='#': 
                s = max_valid_s(r,c)
                if s==0: continue
                area = (s*2+1)**2
                cmd = "PAINT_SQUARE %d %d %d" % (r,c,s)
                pq.put( (-area,s,r,c,cmd) ) 
            else: pass
    while not pq.empty():
        item = pq.get()
        if len(item)==5:
            _,s,r,c,cmd = item
            if marked[r][c]: continue
            mark_sq(r,c,s)
        else:
            _,r,c,r2,c2,cmd = item
            if marked[r][c]: continue
            mark_line(r,c,r2,c2)
        res.append( cmd )

#~ greedy_sq()
#~ greedy_line()
greedy_line_and_sq()

print len(res)
for cmd in res: 
    print cmd

