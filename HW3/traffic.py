# Author: Chunhao Shen, Han Wang

import random
import copy

# data structure, 
# use adjactent matrix to represent the directed graph
#
# e.g. : a street map of 2x2 blocks 
#  'o' represent a segemtn of street
#  '[ ]' is a block
#  '+' is an intersection
#
#                     end node
#                     |
#   +  o  +  o  +  o  +     (0,0)(0,1)(0,2)
#   o [ ] o [ ] o [ ] o     (1,0)(1,1)(1,2)(1,3) 
#   +  o  +  o  +  o  +     (2,0)(2,1)(2,2)
#   |
#   start node
#  
# how to name the node? use tuple
# (ith-row, jth on each row), count from 0
#  even row has h + 2 nodes
#  odd row has h + 1 nodes

def even(n):
    return n % 2 == 0
def odd(n):
    return not even(n)

# ←
# even
# odd, even is judged by the index of the row (0,1,2,..)
def L(node):
    i, j = node
    return (i, j-1)

# →
# even
def R(node):
    i, j = node
    return (i, j+1)
# ↑
# odd
def U(node):
    i,j = node
    return (i-2, j)
# ↓
# odd
def D(node):
    i, j = node
    return (i+2, j)

# ←╮
# only appear in odd row
def UL(node):
    i, j = node
    return (i-1, j-1)
# ╭→
# only appear in odd row
def UR(node):
    i, j = node
    return (i-1, j)

# ←╯
# odd
def DL(node):
    i, j = node
    return (i+1, j-1)

# ╰→ 
# odd    
def DR(node):
    i, j = node
    return (i+1, j)

#  ↑
# -╯
# only appear in even row
def RU(node):
    i, j = node
    return (i-1, j+1)

# ↑
# ╰—-
# only appear in even row
def LU(node):
    i, j = node
    return (i-1, j)

# -╮
#  ↓
# even row
def RD(node):
    i, j = node
    return (i+1, j+1)

# ╭—-
# ↓
# even row
def LD(node):
    i, j = node
    return (i+1, j)

class Map(object):
    def __init__(self, w, h, start, end):
        # w :  number of blocks on a row
        # h : number of blocks on a colomn
        # start : the entry point, should be given as a pair e.g. (2,0)
        # end : the finish point, should be given as a pair e.g. (4,3)
        self.w = w
        self.h = h 
        self.start = start
        self.end = end
        assert even(start[0]) and start[1] == 0
        assert even(end[0]) and end[1] == w + 1
        self.n_nodes = (h + 1)*w +  (w + 1)*h # number of nodes
        self.adj = [[0 for _ in range(self.n_nodes)] for _ in range(self.n_nodes)]

    def __str__(self):
        pass
        # out = ""
        # for _ in range(self.h):
        #     out += "o  +  " * (self.w + 1) + "o\n"
        #     out += "  " + " o [ ]" * (self.w) + " o\n"
        # out += "o  +  " * (self.w +1) + "o\n"
        # return out

    # map node: a pair of int to index in adj matrix
    # return the index in the matrix of the coordinate of that node in original map
    def node2idx(self, node):
        i, j = node
        assert j >= 0 and j < self.h * 2
        assert i >= 0 and i < self.w + 2
        if even(i):
            return self.w * (i/2) + (self.w + 1)* (i/2)  +j
        else:
            return self.w * (i//2) + (self.w +1)*(i//2 +1 ) -1 + j
        
    def cut(self, a, b):
        i = self.node2idx(a) 
        j = self.node2idx(b)
        self.adj[i][j] = 0

    def cut2(self, a, b):
        i = self.node2idx(a) 
        j = self.node2idx(b)
        self.adj[i][j] = 0
        self.adj[j][i] = 0

    def conn(self, a, b):
        i = self.node2idx(a) 
        j = self.node2idx(b)
        self.adj[i][j] = 1
        
    def conn2(self, a, b):
        i = self.node2idx(a) 
        j = self.node2idx(b)
        self.adj[i][j] = 1
        self.adj[j][i] = 1

    # apply f on all nodes
    # what is f??
    def forall_nodes(self, f, cond=None):
        # for i in range(2 * self.h + 1):
        #     if even(i):
        #         for j in range(self.w + 2): # why this??    
        #                                     # I think it's supposed to be w for even, w+1 for odd
        #             f((i,j))
        #     else:
        #         for j in range(self.w + 1):
        #             f((i,j))
        for i in range(2 * self.h + 1):
            if even(i):
                for j in range(self.w): 
                                        
                    f((i,j))
            else:
                for j in range(self.w + 1):
                    f((i,j))

    # node : a pair of int
    # extra nodes means the node is in the 1st, last colomu
    def is_nodes_on_weight(self, node):
        i,j = node
        return i == 0 or i == self.h *2

    def is_nodes_on_height(self, node):
        i,j = node
        return j == 0 or j == self.w + 1
    
    # return all nodes "around" the 'node'
    # by "around", I mean, all legal neighbor nodes
    # this function take care of all the edge cases
    # TODO: finished all the situations.
    # TODO: ends: (0,0),(1,0),(0,w-1),(1,w),(2h-1,0),(2h,0),(2h,w-1),(2h-1,w)
    # TODO: boundaries: 
    # TODO: if top edge: L/R/LD/UD; if bottom edge: L/R/LU/RU
    # TODO: if left edge: U/D/DR/UR; if right edge: U/D/UL/DL
    def nodes_around(self, node):
        res = []
        # case 1: nodes on weight
        i,j = node
        # if is_nodes_on_weight(node):
        #     if is_nodes_on_height(node):
        #         res += [R(node), (node), UR(node), DR(node)]
        #     else: # finish
        #         res += [U(node), D(node), UL(node), DL(node)]
        # # case 2: first/last row
        # elif i == 0 or i == self.h * 2:
        #     if i == 0:
        #         res += [LD(node), RD(node)]
        #     else:
        #         res += [UL(node), UR(node)]
        # # case 3: first/last col
        # elif odd(i) and (j == 0 or j == self.w):
        #     if j == 0:
        #         res += [UR(node), LR(node)]
        #     else:
        #         res += [UL(node), LL(node)]
        
        
    # permissive, all directions are allowed
    def connect_all(self):
        for i in range(2 * self.h + 1):
            if even(i):
                for j in range(self.w ): # +2
                    nodes_list = self.nodes_around(i,j)
                    for each in nodes_list:
                        self.conn2((i,j),each)        
            else:
                for j in range(self.w + 1):
                    nodes_list = self.nodes_around(i,j)
                    for each in nodes_list:
                        self.conn2((i,j),each)

    #randomly delete some point
    def delete_randomly(self):
        del_num=1
        for i in range(del_num):
            rani1=random.randint(0,self.h*2)
            rani2=random.randint(0,self.h*2)
            #little bug: all the nodes on the right edge are connected
            ranj1=random.randint(0, self.w-1)
            ranj2=random.randint(0, self.w-1)
            self.cut((rani1,ranj1),(rani2,ranj2))



def search(node,stack,maps,visited_edge):
    # possible_edge=[]
    # for i in range(len(maps[0])):
    #     if i == 1:
    pass


def dfs(node,stack,maps,visited_edge):
    possible_edge=search(node,stack,maps,visited_edge)
    if len(possible_edge) == 0:
        stack.pop()
        dfs(stack[-1],stack,maps,visited_edge)
    pass

def find_soultion(start,finish,maps,visited_edge):
    #maps_sub=copy.copy(maps)
    visited_edge=[]
    stack=[]
    stack.append(start)
    dfs(stack[-1],stack,mapsere,visited_edge)

def examine(edge):
    pass

if __name__ == "__main__":
    # str_input=input("Please type in the height or width(same) of the puzzle, like 5:")
    # height=int(str_input)
    # #Initialize n*n points in adjacency matrix which has size (n*n)*(n*n). if (A,B) ==1 then A has a way to B.
    # start,finish,maps=init_map(height) 
    # sol=find_soultion(start,finish,maps)

    map = Map(2,2, (2,0), (4,3))
    s = str(map)
    print(s.count("o",0,len(s)))
    print(map.n_nodes)
    print(map.node2idx((0,0)))
    print(map.node2idx((1,1)))
    print(map.node2idx((2,1)))

    map.forall_nodes(print)
    

    print(map)