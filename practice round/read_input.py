import sys
#~ filename,comment = sys.argv[1:3]

# these are the global variables that can be used in painting.py
N,M = map( int, raw_input().split() )
img = [] # array of string (each line)
res = [] # instructions
marked = [ [False for i in xrange(M)] for j in xrange(N)]
for line in sys.stdin:
    img.append(line)
