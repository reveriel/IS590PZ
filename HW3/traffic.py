# Author: Chunhao Shen, Han Wang

import random
import copy

# data structure, 
# use adjactent matrix to represent the directed graph
#
# e.g. : a street map of 2x2 blocks 
#  'o' represent a segemtn of street
#
#                     end node
#                     |
#   o  +  o  +  o  +  o,      nodes: (0,0), (0,1), (0,2), (0,3)
#      o [ ] o [ ] o               :    (1,0), (1,1), (1,2)
#   o  +  o  +  o  +  o            : (2,0)
#      o [ ] o [ ] o               ;    (3,0)
#   o  +  o  +  o  +  o            : (4,0), (4,1), (4,2), (4,3)
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
        self.n_nodes = h * (w + w + 3) + w + 2 # number of nodes
        self.adj = [[0 for _ in range(self.n_nodes)] for _ in range(self.n_nodes)]

    def __str__(self):
        out = ""
        for _ in range(self.h):
            out += "o  +  " * (self.w + 1) + "o\n"
            out += "  " + " o [ ]" * (self.w) + " o\n"
        out += "o  +  " * (self.w +1) + "o\n"
        return out

    # map node: a pair of int to index in adj matrix
    def node2idx(self, node):
        i, j = node
        assert j >= 0 and j < self.h * 2
        assert j >= 0 and j < self.w + 2
        if even(i):
            return j + (i // 2) * (self.w + 2 + self.w + 1)
        else:
            return j + (i // 2) * (self.w + 2 + self.w + 1) + self.w + 2
        
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

    # permissive, all directions are allowed
    def connect_all(self):
        for i in range(2 * self.h + 1):
            if even(i):
                for j in range(2 * self.w + 2):
                    print(i,j)
            else:
                for j in range(2 * self.w + 1):
                    print(i,j)

        

def cut_two_edge(a,b,maps):
    maps[a][b]=0
    maps[b][a]=0

def conn_two_edge(a,b,maps):
    maps[a][b]=1
    maps[b][a]=1

def conn_edge(a,b,maps):
    maps[a][b]=1

def cut_edge(a,b,maps):
    maps[a][b]=0

def init_map(height):
    size=height*(2*height-1)
    maps = [[0 for _ in range(size)] for _ in range(size)]
    #At first all way is through
    for i in range(2*height-1):
        for j in range(height):
            if i == 0:
                if j == 0: continue
                else:
                    conn_two_edge(i*height+j,i*height+j+height,maps)
                    conn_two_edge(i*height+j,i*height+j+height-1,maps)
            elif i ==  2*height-2:
                if j == 0: continue
                else:
                    conn_two_edge(i*height+j,i*height+j-height,maps)
                    conn_two_edge(i*height+j,i*height+j-height-1,maps)
            elif i/2 == 0:
                if j == 0: continue
                else:
                    conn_two_edge(i*height+j,i*height+j-height,maps)
                    conn_two_edge(i*height+j,i*height+j-height-1,maps)
                    conn_two_edge(i*height+j,i*height+j+height,maps)
                    conn_two_edge(i*height+j,i*height+j+height-1,maps)
            else:#i/2!=0
                if j == 0:
                    conn_two_edge(i*height+j,i*height+j+height+1,maps)
                    conn_two_edge(i*height+j,i*height+j-height+1,maps)
                elif j == height-1:
                    conn_two_edge(i*height+j,i*height+j+height,maps)
                    conn_two_edge(i*height+j,i*height+j-height,maps)
                else:
                    conn_two_edge(i*height+j,i*height+j+height,maps)
                    conn_two_edge(i*height+j,i*height+j-height,maps)
                    conn_two_edge(i*height+j,i*height+j+height+1,maps)
                    conn_two_edge(i*height+j,i*height+j-height+1,maps)

    #randomly delete some point
    del_num=1
    for i in range(del_num):
        rani=random.randint(2,(2*height-4))
        if height<=3:
            ranj=2
        else:
            ranj=random.randint(2,height-2)
        #index_del=rani*height+ranj
        if rani/2==0:
            cut_two_edge(rani*height+ranj,rani*height+ranj-height,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj-height-1,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj+height,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj+height-1,maps)
        else:
            cut_two_edge(rani*height+ranj,rani*height+ranj-height,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj-height+1,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj+height,maps)
            cut_two_edge(rani*height+ranj,rani*height+ranj+height+1,maps)



    #index 0, 2height, 4height....height(2height-2) is out of the map, randomly choose one to be the start point.
    ran1=random.randint(0,height-1)
    index_start=ran1*2*height
    
    if index_start==0:
        conn_two_edge(0,1,maps)
        conn_two_edge(0,height,maps)
    elif(index_start==height*(2*height-2)):
        conn_two_edge(height*(2*height-2),height*(2*height-3),maps)
        conn_two_edge(height*(2*height-2),height*(2*height-2)+1,maps)

    #We do not have a space for the index finish, we assume only one of the point on the most right can go to the finish point
    #The point on the most right has index 2height-1, 4height-1... height(2height-2)-1
    ran2=random.randint(1,height-1)
    index_finish=ran2*2*height-1
    for x in maps:
        print(x)
        print("\n")
    print(index_start,index_finish)
    return maps, index_start, index_finish

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

    map.connect_all()
    

    print(map)