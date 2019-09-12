# data structure:
# map is a 2-D list of size height*width. Each map[i][j] contains a Point (a class defined below)
# line is a 3-D list of current line. For example[[[0,0],[2,1]],[[2,1],[2,2]]] represent there are two line
# in the map which is (0,0),(2,1) and (2,1),(2,2)
#  
map=[]
line=[]

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



def is_valid_input(str):
    if len(str!=11): return False
    bo1=(str[0]=="(" and str[2]=="," and str[4]==")" and str[5]=="," and str[6]=="(" and str[8]=="," and str[10]==")")
    bo2=(str[1].isdigit() and str[3].isdigit() and str[7].isdigit() and str[9].isdigit())
    bo3=(str[1]>=0 and str[1]<height and str[7]>=0 and str[7]<height and str[3]>=0 and str[3]<width and str[9]>=0 and str[9]<width)
    if (bo1 and bo2 and bo3) == False: return False
    bool_cross=is_twoline_cross

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

def ai_move(pointA,pointB):
    # connect the two point and upgrade the map[], line[]


if __name__ == "__main__":
    height,width=init_map()
    global map
    while True:
        New_Move=input("input the two points you want to connect, in the format of (0,0),(2,1) with no blank space:")
        if is_valid_input(New_Move) == False:
            print("Invalid points input! Please try again.")
            continue
        possible_move=get_possible_move(map)
        if not possible_move:
            print("AI wins!")
            break
        pointA, pointB=choose_move(possible_move)
        ai_move(pointA,pointB)
        possible_move=get_possible_move(map)
        if not possible_move:
            print("You wins!")
            break

