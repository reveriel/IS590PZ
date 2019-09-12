map=[]

class Point:
    def __init__(self, idx_x, idx_y, value, other_end):
        self.idx_x=idx_x
        self.idx_y=idx_y
        self.value=value
        self.other_end=other_end
    

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
            map_sub.append(Point(i,j,"*",None))
        map.append(map_sub)

    return height,width


def is_valid_input(str):
    bo1=(str[0]=="(")
    bo2=(str[1].isdigit() & )

if __name__ == "__main__":
    height,width=init_map()
    while True
        New_Move=input("input the two points you want to connect, in the format of (0,0),(2,1) with no blank space:")
        if is_valid_input(New_Move) == False:
            print("Invalid points input! Please try again.")
            continue
