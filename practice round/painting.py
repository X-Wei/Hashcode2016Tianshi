import sys
import Queue
#~ filename,comment = sys.argv[1:3]

N,M = map( int, raw_input().split() )
img = [] # array of string (each line)
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
    while( is_valid_sq(r,c,s) ): s+=1
    return s-1

def mark_sq(r,c,s):
    for i in xrange(r-s, r+s+1):
        for j in xrange(c-s,c+s+1):
            marked[i][j]=True

# greedy algo for using paint square instruction and nothing else
pq = Queue.PriorityQueue() # maxpq: squares with largest `s` is on top
for r in xrange(N):
    for c in xrange(M):
        char = img[r][c]
        if char=='#': 
            s = max_valid_s(r,c)
            cmd = "PAINT_SQUARE %d %d %d" % (r,c,s)
            pq.put( (-s,r,c,cmd) ) 
        else: pass
res = [] # instructions
while not pq.empty():
    s,r,c,cmd = pq.get()
    s *= -1
    if marked[r][c]: continue
    mark_sq(r,c,s)
    res.append( cmd )

print len(res)
for cmd in res: 
    print cmd
