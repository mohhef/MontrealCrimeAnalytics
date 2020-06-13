# -------------------------------------------------------
# Assignment (1)
# Written by (Mohamed Hefny, 40033382)
# For COMP 472 Section (ABIX) – Summer 2020
# --------------------------------------------------------
import time
import sys
import math
import validgoal
import numpy as np

class Node:
    """Node class"""
    def __init__(self, prev=None,row=None,col=None):
        self.prev=prev
        self.row=row
        self.col=col
        self.g=0
        self.h=0
        self.f=0

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.col, self.row))

    def __str__(self):
        return "({0}, {1})".format(self.row, self.col)


def search(map, start, end):
    """
    Search for optimal path using the A* algorithm, uses the costs and heuristic values
    parameter map: 2d array on where a path will be searched on
    parameter start: starting possition on the 2d array, represented in (row,column)
    parameter end: ending position on the 2d array, represented in (row,column)
    parameter: numpy array of the coordinates of the path found
    """
    start_time = time.time()
    open_list=[]
    closed_list=set()
    start_row, start_col=start
    start_node = Node(None,start_row,start_col)

    end_row,end_col=end
    end_node=Node(None,end_row,end_col)

    #to check if the goal node is a valid node, makes the algorithm slightly faster
    if not validgoal.valid_goal(map, end):
        print("Due to blocks, no path is found. Please change the map and try again.")
        return []
    
    open_list.append(start_node)
    
    #check open list values
    while len(open_list)>0:
        isTimeUp(start_time)
        current_node = open_list.pop(0)
        closed_list.add(current_node)
        #if the goal node has been found
        if current_node == end_node:
            end_time = time.time()
            print("Path found in {0:.4f} seconds".format(end_time - start_time))
            print("Cost: {0:.1f}".format(current_node.g))
            return get_path(current_node)

        #find the neighbours of the current node   
        neighbours = findNeighbours(map,current_node,end_node,closed_list)

        #assign the cost for each neighbour
        for child, cost in neighbours:
            child.g = current_node.g+cost
            child.h = diag_distance(map,(child.row,child.col),end)
            child.f = child.g + child.h
            open_list.insert(0, child)
      
        open_list.sort(key=lambda item: item.f)

    #if there is no path found
    print("Due to blocks, no path is found.Please change the map and try again")
    return []

def isTimeUp(start_time):
    end_time = time.time()
    time_diff = end_time-start_time
    if(time_diff>10):
        print('Time is up. The optimal path is not found.')
        sys.exit()

def movecost(map, current_node, target_node, end_node):
    """
    calculates the cost for traversing the map, format(row,col)
    If there is no possible path to node then return cost as infinity
    
    parameter map: map that will be traversed, 2d array
    parameter current_node: origin node to calculate costs from
    parameter target_node: target node to calculate costs from origin
    parameter end_node: goal node of the whole map
    return: cost of traversing from orgin to destination node
    """
 
    row_cur = current_node.row
    col_cur = current_node.col

    row_tar = target_node.row
    col_tar = target_node.col

    row_end = end_node.row
    col_end = end_node.col

    shape_width , shape_height = map.shape

    #if not inside the map
    if col_cur < 0 or col_tar < 0 or col_cur > shape_width or col_tar > shape_width:
        return sys.maxsize
    if row_cur < 0 or row_tar < 0 or row_cur > shape_height or row_tar > shape_height:
        return sys.maxsize

    horizontal_step = col_tar - col_cur
    vertical_step = row_tar - row_cur

    # if the distance is longer than 1, return infinity
    if math.fabs(horizontal_step) > 1 or math.fabs(vertical_step) > 1:
        return sys.maxsize

    if target_node != end_node :
        if row_tar==0 or col_tar==0 or col_tar == shape_width or row_tar == shape_height:
            return sys.maxsize

    #very edge case, if you choose two adjcent blocks verticall or horizontally, it makes sure that it doesnt traverse the edges
    if movecost.counter == 1 and target_node==end_node:
        if horizontal_step!=0 and vertical_step!=0:
            pass
        else:
            return sys.maxsize
    #To check diagonally
    if horizontal_step!=0 and vertical_step!=0:
        col_check= col_cur if horizontal_step>0 else col_cur-1
        row_check = row_cur if vertical_step>0 else row_cur-1
        return 1.5 if map[row_check, col_check]==0 else sys.maxsize
    
    #To check vertical
    if horizontal_step==0:
        check_row = row_cur
        #move down
        if vertical_step < 0:
            check_row = row_cur-1
        #move up
        if vertical_step > 0:
            check_row = row_cur
        #Not blocked on both sides
        if map[check_row,col_cur-1]==0 and map[check_row,col_cur]==0:
            return 1
        #Blocked on one side
        if map[check_row,col_cur-1]==0 or map[check_row,col_cur]==0:
            return 1.3
        #Both sides are blocked
        return sys.maxsize

    #To check horizontally
    if vertical_step==0:
        check_col = col_cur

        #left movement
        if horizontal_step<0:
            check_col = col_cur -1
        #right movement
        if horizontal_step>0:
            check_col = col_cur 

        #not blocked on both sides
        if map[row_cur-1, check_col]==0 and map[row_cur, check_col] == 0:
            return 1
        #one side blocked
        if map[row_cur-1, check_col]==0 or map[row_cur, check_col] == 0:
            return 1.3
        #blocked from both sides
        return sys.maxsize


def get_path(from_node):
    """
    reconstructs the path found from intial to goal node, keep pointer of parent node
    parameter from_node: goal node to find the parent of
    return: path in a numpy array format, each row is a coordinate point (row,col)
    """
    path = np.array([from_node.row, from_node.col])

    current = Node(from_node.prev, from_node.row, from_node.col)
    while current.prev is not None:
        prev = current.prev
        current = Node(prev.prev, prev.row, prev.col)
        path = np.vstack((np.array([prev.row, prev.col]), path))
    return path



def findNeighbours(map,current_node,end_node,closed_list):

    """
    Find all moves from current node to destination node, position format: (row,col)
    Find the neighbours and the costs of move to these numbers
    Choose neighbour if cost is not infinity(i.e. valid move)
    parameter map: the map on which we will find the path on
    parameter current_node: current node to find neighbours of
    parameter end_node: end node which is the goal
    parameter closed_list: the visited nodes on the map
    return: moves and costs of neighbours nodes
    """
    
    movecost.counter+=1

    result=[]
    row_cur=current_node.row
    col_cur=current_node.col

    #create node and check cost
    left_node = Node(current_node, row_cur, col_cur-1)
    left_cost = movecost(map,current_node,left_node, end_node)
    right_node = Node(current_node,row_cur,col_cur+1)
    right_cost = movecost(map,current_node,right_node, end_node)

    top_node = Node(current_node,row_cur+1, col_cur)
    top_cost = movecost(map,current_node,top_node, end_node)
    bot_node = Node(current_node,row_cur-1,col_cur)
    bot_cost = movecost(map,current_node,bot_node, end_node)

    top_left= Node(current_node,row_cur+1, col_cur-1)
    tl_cost = movecost(map,current_node,top_left, end_node)
    top_right=Node(current_node,row_cur+1, col_cur+1)
    tr_cost = movecost(map,current_node,top_right, end_node)

    bottom_left=Node(current_node, row_cur - 1, col_cur - 1)
    bl_cost = movecost(map,current_node,bottom_left, end_node)
    bottom_right=Node(current_node,row_cur-1, col_cur+1 )
    br_cost = movecost(map,current_node,bottom_right, end_node)
  
    if left_node not in closed_list and left_cost<sys.maxsize:
        result.append((left_node,left_cost))
    if right_node not in closed_list and right_cost<sys.maxsize:
        result.append((right_node,right_cost))

    if top_node not in closed_list and top_cost<sys.maxsize:
        result.append((top_node,top_cost))
    if bot_node not in closed_list and bot_cost<sys.maxsize:
        result.append((bot_node,bot_cost))

    if top_left not in closed_list and tl_cost<sys.maxsize:
        result.append((top_left,tl_cost))
    if top_right not in closed_list and tr_cost<sys.maxsize:
        result.append((top_right,tr_cost))  

    if bottom_left not in closed_list and bl_cost<sys.maxsize:
        result.append((bottom_left,bl_cost))
    if bottom_right not in closed_list and br_cost < sys.maxsize:
        result.append((bottom_right,br_cost))

    return result
movecost.counter=0

def diag_distance(city_map, current, goal):
    """
    This heurstic is like manhattan distance but we can also go diagonally
    If there is a diagonal path itll consider it
    Considering only vertical and horizontal paths will not gaurntee admissbility and thus diagonal is considered
    parameter city_map: the graph with the crimes
    parameter current: current node to be evaluated, (row,column)
    parameter goal: the end goal coordinate, (row,column)
    """
    height_, width_ = city_map.shape

    row_cur, col_cur = current
    row_goal, col_goal = goal

    if col_cur < 0 or col_goal < 0 or col_cur > width_ or col_goal > width_:
        return sys.maxsize
    if row_cur < 0 or row_goal < 0 or row_cur > height_ or row_goal > height_:
        return sys.maxsize

    horizontal_step = math.fabs(col_goal - col_cur)
    vertical_step = math.fabs(row_goal - row_cur)

    if vertical_step > horizontal_step:
        temp = vertical_step
        vertical_step = horizontal_step
        horizontal_step = temp

    return vertical_step * 1.5 + (horizontal_step - vertical_step)

#credits for helping: dung hoang
