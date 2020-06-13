# -------------------------------------------------------
# Assignment (1)
# Written by (Mohamed Hefny, 40033382)
# For COMP 472 Section (ABIX) – Summer 2020
# --------------------------------------------------------
import geopandas as gp
import sys
import matplotlib.pyplot as plt
import numpy as np
import search

np.set_printoptions(threshold=sys.maxsize)

def get_data(file):
    """
    returns data of a file
    :parametar file: file to return the data from
    :return: data
    """

    data = gp.read_file(file)
    return data

def get_arr(x,x1,y,y1,gridsize):
    """
    generates longitude and latitude arrays from boundaries
    :parameter x: left most x
    :parameter x1: right most x
    :parameter y: bottom most y
    :parameter y1: top most y1
    """

    longitude_arr = np.arange(x, x1+gridsize*0.9,gridsize)
    latitude_arr = np.arange(y, y1+gridsize*0.9, gridsize)
    return longitude_arr,latitude_arr

#Generates a 2d array from a threshold
def get_map(bottomLeft, topRight, gridSize=0.002, dataPoints=None, threshold=0):
    """
    get histogram, mean and standard deviation
    parameterar bottomLeft: bottom left coordinate
    parameter topRight: top right coordinate
    parameter gridize: cell length, default 0.002
    parameter dataPoints: points representing the crime from shp file
    parameter threshold: threshold to cutoff for crime rates
    return: (hist, flat_hist, mean, standard_dev)
    """

    x, y= bottomLeft
    x1,y1= topRight

    #Create the grid
    long = np.arange(x, x1 + gridSize / 2, gridSize)
    lat = np.arange(y, y1 + gridSize / 2, gridSize)

    #x and y vector to create the histogram
    X = dataPoints.geometry.x
    Y = dataPoints.geometry.y
    hist, xedges, yedges = np.histogram2d(Y, X, bins=[lat, long])

    #convert percentage threshold to number
    crime_array= hist.flatten()
    crime_array= -np.sort(-crime_array)
    threshold_index = int(np.size(crime_array)-(np.size(crime_array)*threshold/100))
    threshold_value = crime_array.item(threshold_index)
    if threshold_value == 0:
        threshold_value = crime_array[crime_array > 0].min()
    
    #flatten histogram according to threshold to contain only 0 and 1s
    flat_hist = np.copy(hist)
    flat_hist[flat_hist <= threshold_value] = 0
    flat_hist[flat_hist > threshold_value] = 1

    #get mean and standard deviation
    mean = np.mean(hist)
    standard_dev=np.std(hist)
    print("Mean: {0:.4f}".format(mean))
    print("Standard deviation: {0:.4f}".format(standard_dev))
    print("Total number in each grid:")

    intial=np.array(hist[0])
    for x in hist[1:]:
        intial=np.vstack([x,intial])
    print(intial)
    #print(flat_hist)

    return hist, flat_hist, mean, standard_dev

def draw(histogram, bottomLeft, topRight,gridsize,mainhist, plot=None):
    """
    generates the grid with crime points
    :parameter histogram: histogram of crime rate on map
    :parameter bottomLeft: bottom left coordinate of the map
    :parameter topRight: top right coordinate of the map
    :parameter gridsize: cell size
    :parameter plot: points to draw on the map, defaul = none 
    """

    x, y = bottomLeft
    x1, y1 = topRight

    #boundaries of the map
    extent = [x, x1, y, y1]
    long = np.arange(x, x1 + gridsize / 2, gridsize)
    lat = np.arange(y, y1 + gridsize / 2, gridsize)

    #plots the graph into blocks
    plt.imshow(histogram, origin='lower',extent=extent, interpolation='nearest', aspect='auto')
    mainhist=mainhist.astype(np.int64)

    #adds the crime rates text on the graph
    for indx,val in enumerate(long[:-1]):
        for yindx,yval in enumerate(lat[:-1]):
            crimer_rate= mainhist[yindx][indx]
            plt.text(val+gridsize/2,yval+gridsize/2,crimer_rate,ha='center',va='center')

    #show the graph with or without the path
    if plot is None:
        plt.show()
    else:
        long_vec,lat_vec = plot.T
        plt.plot(long_vec,lat_vec)
        plt.show()

def get_row_col(user_longitude,user_latitiude,longitude_arr,latitude_arr):
    """
    gets the row and coloumn of user entered start and goal longitude and latitude
    parameter user_longitude: user entered longitdue
    parameter user_latitiude: user entered lontitude
    parameter longtiude_arr: array with longitude values divided from cell size
    parameter latitude_arr: array with latitude values divided from cell size
    return: row_index,coloumn_index
    """
    row_index = 0
    coloumn_index=0

    #find the coloumn index
    for i in longitude_arr:
        if user_longitude >= i:
            coloumn_index = np.where(longitude_arr==i)[0][0]

    #find the row index
    for i in latitude_arr:
        if user_latitiude >= i:
            row_index = np.where(latitude_arr==i)[0][0]
    return(row_index,coloumn_index)


def run(grid, threshold):
    """
    called to run program
    parameter grid: cell size user enters
    parameter threshold: threshold to cutoff crime rates
    """
    x =  -73.59
    y =  45.49
    x1 = -73.55
    y1 = 45.53
    gridsize= grid
    longitude_arr, latitude_arr = get_arr(x,x1,y,y1,gridsize)

    #map boundaries
    leftpoint=longitude_arr.min()
    rightpoint=longitude_arr.max()
    bottom=latitude_arr.min()
    top=latitude_arr.max()
    bottomLeft = (leftpoint,bottom)
    topRight =  (rightpoint,top)

    #data fetched
    data = get_data("crime_dt.shp")

    crime_histo, crime_threshold, mean, std_dev = get_map(bottomLeft=bottomLeft,topRight=topRight,gridSize=gridsize,dataPoints=data,threshold=threshold)
    
    #draw the inital grid
    xs  = np.arange(x, x1+gridsize*0.9,gridsize)
    ys = np.arange(y, y1+gridsize*0.9, gridsize)
    for x in xs:
        plt.plot([x, x], [ys[0], ys[-1]])
    for y in ys:
        plt.plot([xs[0], xs[-1]], [y, y])
    plt.show()

    #draw the crime rate grid
    draw(crime_threshold, bottomLeft=bottomLeft, topRight=topRight,mainhist=crime_histo, gridsize=gridsize)
    
    height, width = crime_threshold.shape

    points_in_grid = []

    #let the user specify the start and end coordinates
    start_long,start_lat = input("Enter start longitude & latitude comma seprated:").split(",")
    start_long = float(start_long)
    start_lat = float(start_lat)
    end_long,end_lat = input("Enter goal longitude & latitude comma seprated:").split(",")
    end_long = float(end_long)
    end_lat = float(end_lat)

    #transform the latitude and longitude coordinates to row and column indexes
    startRow_index, startCol_index = get_row_col(start_long,start_lat,longitude_arr,latitude_arr)
    endRow_index, endCol_index = get_row_col(end_long,end_lat,longitude_arr,latitude_arr)
    

    points_on_grid = search.search(crime_threshold, (startRow_index, startCol_index), (endRow_index, endCol_index))
    #checks if there are points generated to draw a path
    if len(points_on_grid)==0:
        draw(crime_threshold, bottomLeft=bottomLeft, topRight=topRight, mainhist=crime_histo, gridsize=gridsize)
    else:
        try:
            route = np.column_stack((longitude_arr[points_on_grid[:, 1]], latitude_arr[points_on_grid[:, 0]]))
            draw(crime_threshold, bottomLeft=bottomLeft, topRight=topRight, plot=route, gridsize=gridsize,mainhist=crime_histo)
        except:
            pass

#let the user enter the grid and threshold
grid,threshold = input("Enter grid size and threshold seprated by a comma: ").split(",")
grid = float(grid)
threshold = float(threshold)
run(grid,threshold)

print('Thank for using my program!')

#credits for helping: dung hoang