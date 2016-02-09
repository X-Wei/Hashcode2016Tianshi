'''this file contains snippets for customized sorting and pq'''

class FooCls: # demo class -- just a tuple...
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return '(%d,%d)'%(self.x, self.y)
    def __cmp__(self, other):# self-defined compare: first compare the x field, if equal, compare the y field
        if self.x != other.x: return self.x-other.x
        else: return self.y-other.y

foos = [ FooCls(x,y) for x,y in [(3,5), (1,3), (5,2), (3,1)] ] 


print '===sort example==='

print 'sort using `key` parameter'
foos.sort(key=lambda f:f.x) # sort by `x` field of FooCls
print map(str, foos)

print 'sort using `cmp` parameter'
def foocmp(f1,f2): # return `f1-f2`, first compare the x field, if equal, compare the y field
    if f1.x != f2.x: return f1.x-f2.x
    else: return f1.y-f2.y
foos.sort(cmp=foocmp)
print map(str, foos)

print 'sort by desc order'
foos.sort(key=lambda f:f.x, reverse=True)
print map(str, foos)


print '===pq example==='

print 'using the PriorityQueue class, use self-defined class with `__cmp__` overridden'
import Queue
pq = Queue.PriorityQueue() # NB: pq is a MinHeap, can change the __cmp__ method if we want MaxHeap
for f in foos:
    pq.put(f) # the __cmp__ method is already overridden in FooCls
while not pq.empty(): 
    top = pq.get()
    print top,
print ''

print 'using the PriorityQueue class and put just tuples'
pq2 = Queue.PriorityQueue()
tuples = [(3,5), (1,3), (5,2), (3,1)]
for x,y in tuples: # for each tuple we calculate a priority=x*MaxX+y
    p = x*10+y # priority
    pq2.put( (-p,x,y) ) # the first element in the tuple is considered as priority key, put -1*p: MaxHeap!
while not pq2.empty():
    p,x,y = pq2.get()
    print (x,y),
print ''

print 'otherwise we can use the `heapq` module and write a wrapper class: https://joernhees.de/blog/2010/07/19/min-heap-in-python/'
    

