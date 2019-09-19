# Author: Chunhao Shen, Han Wang

import random
import copy
import math
import time
time1=0
time2=0

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
    maps=[]
    for i in range(size):
        maps_sub=[]
        for j in range(size):
            maps_sub.append(0)
        maps.append(maps_sub)
    #At first all way is through
    for i in range(2*height-1):
        for j in range(height):
            if i == 0:
                if j == 0: continue
                else:
                    conn_edge(i*height+j,i*height+j+height,maps)
                    conn_edge(i*height+j,i*height+j+height-1,maps)
                    if(j!=height-1):
                        conn_two_edge(i*height+j,i*height+j+1,maps)
            elif i ==  2*height-2:
                if j == 0: continue
                else:
                    conn_edge(i*height+j,i*height+j-height,maps)
                    conn_edge(i*height+j,i*height+j-height-1,maps)
                    if(j!=height-1):
                        conn_two_edge(i*height+j,i*height+j+1,maps)
            elif i%2 == 0:
                if j == 0: continue
                else:
                    conn_edge(i*height+j,i*height+j-height,maps)
                    conn_edge(i*height+j,i*height+j-height-1,maps)
                    conn_edge(i*height+j,i*height+j+height,maps)
                    conn_edge(i*height+j,i*height+j+height-1,maps)
                    if(j!=height-1):
                        conn_two_edge(i*height+j,i*height+j+1,maps)
            else:#i%2!=0
                if j == 0:
                    conn_edge(i*height+j,i*height+j+height+1,maps)
                    conn_edge(i*height+j,i*height+j-height+1,maps)
                elif j == height-1:
                    conn_edge(i*height+j,i*height+j+height,maps)
                    conn_edge(i*height+j,i*height+j-height,maps)
                else:
                    conn_edge(i*height+j,i*height+j+height,maps)
                    conn_edge(i*height+j,i*height+j-height,maps)
                    conn_edge(i*height+j,i*height+j+height+1,maps)
                    conn_edge(i*height+j,i*height+j-height+1,maps)

    #randomly delete some point
    
    del_num=1
    for i in range(del_num):
        rani=random.randint(2,(2*height-4))
        if height<=3:
            ranj=2
        else:
            ranj=random.randint(2,height-2)
        #index_del=rani*height+ranj
        if rani%2==0:
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
    #index_start=6
    
    if index_start==0:
        conn_two_edge(0,1,maps)
        conn_two_edge(0,height,maps)
    elif(index_start==height*(2*height-2)):
        conn_two_edge(height*(2*height-2),height*(2*height-3),maps)
        conn_two_edge(height*(2*height-2),height*(2*height-2)+1,maps)
    else:
        conn_two_edge(index_start,index_start-height,maps)
        conn_two_edge(index_start,index_start+height,maps)
        conn_two_edge(index_start,index_start+1,maps)

    #We do not have a space for the index finish, we assume only one of the point on the most right can go to the finish point
    #The point on the most right has index 2height-1, 4height-1... height(2height-2)-1
    ran2=random.randint(1,height-1)
    index_finish=ran2*2*height-1
    #index_finish=5

    print(maps)
    print(index_start,index_finish)
    return index_start, index_finish,maps

def search(node,stack,maps,visited_edge):
    possible_edge=[]
    l=len(maps[0])
    for i in range(l):
        if maps[node][i]==1:
            edge=[node,i]
            if edge not in visited_edge:
                if len(stack)<2:
                    possible_edge.append(edge)
                else:
                    if edge[1]!=stack[-2] and edge[1]!=start:
                        possible_edge.append(edge)
    return possible_edge


def dfs(node,stack,maps,visited_edge,start,finish,sol):
    time2=time.time()
    possible_edge=search(node,stack,maps,visited_edge)
    for i in possible_edge:
        if i[1]==finish:
            stack.append(i[1])
            if stack not in sol:
                return          #warn
            else:
                possible_edge.remove(i)
                stack.pop()

    if len(possible_edge) == 0:
        stack.pop()
        if len(stack)==0:
            return
        dfs(stack[-1],stack,maps,visited_edge,start,finish,sol)
    else:
        ran=random.randint(0,len(possible_edge)-1)
        stack.append(possible_edge[ran][1])
        visited_edge.append(possible_edge[ran])
        dfs(stack[-1],stack,maps,visited_edge,start,finish,sol)

def find_soultion(start,finish,maps):
    #maps_sub=copy.copy(maps)
    sol=[]
    while True: 
        # sub_sol=[]
        visited_edge=[]
        stack=[]
        stack.append(start)
        dfs(stack[-1],stack,maps,visited_edge,start,finish,sol)
        if len(stack)==0:
            break
        else:
            '''for i in range(len(stack)-1):
                edge=[stack[i],stack[i+1]]
                sub_sol.append(edge)'''

            sol.append(stack)
    return sol

def two_d_sol(sol): #if sol=[[0,1,3],[0,2,5,3]], then this function return a edge_sol in the form of edge, which is [[[0,1],[1,3]],[[0,2],[2,5],[5,3]]]
    edge_sol=[]
    for i in range(len(sol)):
        sub=[]
        for j in range(len(sol[i])-1):
            sub.append([sol[i][j],sol[i][j+1]])
        edge_sol.append(sub)
    return edge_sol

def mulfind_sol(start,finish,maps,sol):
    for k in range(20):
        sub_sol=find_soultion(start,finish,maps)
        for x in sub_sol:
            if x not in sol:
                sol.append(x)
    return sol


def reduce_edge(maps):
    all1=[]
    for i in range(len(maps)):
        for j in range(len(maps[0])):
            if maps[i][j]==1:
                all1.append([i,j])
    
    for i in range(math.ceil(len(maps))):
        ran=random.randint(0,len(all1)-1)
        cut_two_edge(all1[ran][0],all1[ran][1],maps)
        all1.remove(all1[ran])

if __name__ == "__main__":
    str_input=input("Please type in the height or width(same) of the puzzle, like 5:")
    height=int(str_input)
    #Initialize n*n points in adjacency matrix which has size (n*n)*(n*n). if (A,B) ==1 then A has a way to B.
    start,finish,maps=init_map(height)
    reduce_edge(maps)
    sol=[]
    time1=time.time()
    sol=find_soultion(start,finish,maps)
    edge_sol=two_d_sol(sol)
    if (not sol) :
        print("No solution, please run the program again to delete different random edges.")
    else:
        times=0
        while(len(sol)!=1):
            times+=1
            if times>height*height*height: break
            while True:
                flag=0

                m=len(edge_sol)
                ran1=random.randint(0,m-1)
                n=len(edge_sol[ran1])
                ran2=random.randint(0,n-1)

                test_edge=edge_sol[ran1][ran2]

                for l in edge_sol:
                    if test_edge not in l:
                        flag=1
                        break

                if flag==1:
                    break
                else:
                    continue
            
            cut_edge(test_edge[0],test_edge[1],maps)
            sol=[]
            sol=find_soultion(start,finish,maps)
                


    print(sol)
