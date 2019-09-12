# data structure:
# map is a 2-D list of size height*width. Each map[i][j] contains a Point (a class defined below)
# line is a 3-D list of current line. For example[[[0,0],[2,1]],[[2,1],[2,2]]] represent there are two line
# in the map which is (0,0),(2,1) and (2,1),(2,2)
# IMPORTANT!!! For a lineA, lineA[0] should be where it starts(one of two ends) ,and lineA[1] should be where it ends. 
# endPoint should be a 1*2 list 
map=[]
line=[]
endPoint1=[]
endPoint2=[]

class Point:
    #ind_x and idx_y is the index of the point in height and width
    #Value: * for unconnected point, numbers for connected point and show in ?th move this point is connected
    #Only update the number in new end
    
    def __init__(self, idx_x, idx_y, value):
        self.idx_x=idx_x
        self.idx_y=idx_y
        self.value=value
    

def init_map():
    while True:
        str=input("input map size, for example 3,3:")
        height=str[0]
        width=str[2]
        if(height>0 & width>0 & str[1]==","):
            break
        else:
            print("Invlid size! Please try again.")

    global map

    for i in range(height):
        map_sub=[]
        for j in range(width):
            map_sub.append(Point(i,j,"*"))
        map.append(map_sub)

    return height,width

def is_twoline_cross(lineA,lineB): #lineA and lineB should be a 2-D list with size 2*2 ([[0,0],[2,1]])
    x0=lineA[0][0]
    y0=lineA[0][1]
    x1=lineA[1][0]
    y1=lineA[1][1]

    x2=lineB[0][0]
    y2=lineB[0][1]
    x3=lineB[1][0]
    y3=lineB[1][1]

    #assume ax+by+1=0

    a1=(y1-y0)/(y0*x1-y1*x0)
    b1=(x0-y1)/(y0*x1-y1*x0)

    a2=(y3-y2)/(y2*x3-y3*x2)
    b2=(x2-y3)/(y2*x3-y3*x2)

    test1=(a1*x2+b1*y2+1)*(a1*x3+b1*y3+1)
    if test1==0:
        if (a1*x2+b1*y2+1)==0 & (a1*x3+b1*y3+1)!=0:
            if ((x2-x0)*(x2-x1))<=0: return True
        elif (a1*x2+b1*y2+1)!=0 & (a1*x3+b1*y3+1)==0:
            if ((x3-x0)*(x3-x1))<=0: return True
        else:
            if ((x2-x0)*(x2-x1))<=0 or ((x3-x0)*(x3-x1))<=0: return True

    test2=(a2*x0+b2*y0+1)*(a2*x1+b2*y1+1)
    if test2==0:
        if (a2*x0+b2*y0+1)==0 & (a2*x1+b2*y1+1)!=0:
            if ((x0-x2)*(x0-x3))<=0: return True
        elif (a2*x0+b2*y0+1)!=0 & (a2*x1+b2*y1+1)==0:
            if ((x1-x2)*(x1-x3))<=0: return True
        else:
            if ((x0-x2)*(x0-x3))<=0 or ((x1-x2)*(x1-x3)): return True
            
    if test1<0 and test2<0 return True
    return False

def is_valid_line(point1,point2):
    lineA=[]
    lineA.append(point1)
    lineA.append(point2)
    line_copy=line
    
    for i in line:
        if i[1]==point1:
            if (point2[1]-point1[1])/(point2[0]-point1[0]) == -(i[1][1]-i[0][1])/(i[1][0]-i[0][0]): return False
            line_copy.remove(i)
            break

    for j in line_copy:
        if is_twoline_cross(lineA,j): return False
    
    return True




def is_valid_input(str):
    if len(str!=11): return False
    bo1=(str[0]=="(" and str[2]=="," and str[4]==")" and str[5]=="," and str[6]=="(" and str[8]=="," and str[10]==")")
    bo2=(str[1].isdigit() and str[3].isdigit() and str[7].isdigit() and str[9].isdigit())
    bo3=(str[1]>=0 and str[1]<height and str[7]>=0 and str[7]<height and str[3]>=0 and str[3]<width and str[9]>=0 and str[9]<width)
    if (bo1 and bo2 and bo3) == False: return False

    pointA1=[]
    pointA1.append(int(str[1]))
    pointA1.append(int(str[3]))

    pointA2=[]
    pointA2.append(int(str[7]))
    pointA2.append(int(str[9]))

    lineA=[]
    lineA.append(pointA1,pointA2)

    if is_valid_line(pointA1,pointA2): return True
    return False

    

def get_possible_move(map):
    # This fuction has map as input. 
    # Find all possible new lines (point pairs) and append them in a 3-D list: possible_move
    # Use is_twoline_cross() here, check all unconnected(go through map[] and find whether a point has value "*")

    possible_move=[]
    
    return possible_move

def choose_move(possible_move):
    # Choose a move from the possible_move.
    # now we use random choose, may be next time we can have a smart AI
    # Return the move represented by two point. Each point is a 1-D list like [0,0]

    return pointA,pointB

def move(pointA,pointB):
    # connect the two point and upgrade the map[], line[]
    # update endPoint1, endPoint2
    # update endPoint1, endPoint2


if __name__ == "__main__":
    height,width=init_map()
    global map
    while True:
        New_Move=input("input the two points you want to connect, in the format of (0,0),(2,1) with no blank space:")
        if is_valid_input(New_Move) == False:
            print("Invalid points input! Please try again.")
            continue

        pointA1=[]
        pointA1.append(int(New_Move[1]))
        pointA1.append(int(New_Move[3]))

        pointA2=[]
        pointA2.append(int(New_Move[7]))
        pointA2.append(int(New_Move[9]))

        move(pointA1,pointA2)

        possible_move=get_possible_move(map)
        if not possible_move:
            print("AI wins!")
            break
        pointA, pointB=choose_move(possible_move)
        move(pointA,pointB)
        possible_move=get_possible_move(map)
        if not possible_move:
            print("You wins!")
            break

