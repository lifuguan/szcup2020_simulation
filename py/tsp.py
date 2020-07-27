'''
@Author: lifuguan
@Date: 2020-07-23 10:10:22
@LastEditTime: 2020-07-27 10:55:00
@LastEditors: Please set LastEditors
@Description: The solution of Shen Zhen Cup 2020 Problem C
@FilePath: \szcup2020_simulation\py\tsp.py
'''
#%% import necessary library
from __future__ import print_function
import xlrd
import ortools
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
import matplotlib.pyplot as plt
import numpy as np
#%% read the data from xlsx
def read_data_model():
    data = xlrd.open_workbook("../data/C1.xlsx")
    table = data.sheet_by_name("Sheet1")
    rowNum = table.nrows
    colNum = table.ncols

    data = {}
    # Formation: (longtitude(m), latitude(m)) 
    data['locations'] = []
    for i in range(1, rowNum):
        data['locations'].append([(table.cell_value(i,1) - 120)*708883, (table.cell_value(i,2) - 36)*111194])
    dcLocation = [(table.cell_value(1,1) - 120)*708883, (table.cell_value(1,2) - 36)*111194]
    # For TSP : indicate num_vehicles = 1
    data['num_vehicles'] = 1
    # depot : the start and end location for the route.
    data['depot'] = 0
    return data
#%% Compute Euclidean distance between nodes
def compute_euclidean_distance_matrix(locations):
    distances = {}
    for fromCounter, fromNode in enumerate(locations):
        distances[fromCounter] = {}
        for toCounter, toNode in enumerate(locations):
            if fromCounter == toCounter:
                distances[fromCounter][toCounter] = 0
            else:
                distances[fromCounter][toCounter] = math.hypot(fromNode[0] - toNode[0], fromNode[1] - toNode[1])
    return distances

#%%
def print_solution(manager, routing, solution, locationsList):
    """Prints solution on console."""
    # print('Objective: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))

        # visualize the routes between nodes
        if index == 30:
            plt.plot([locationsList[previous_index][0],locationsList[0][0]], [locationsList[previous_index][1],locationsList[0][1]])
        else:
            plt.plot([locationsList[previous_index][0],locationsList[index][0]], [locationsList[previous_index][1],locationsList[index][1]])
                
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Distance: {}m\n'.format(route_distance)
    print(plan_output)

# %% main function
if __name__ == '__main__':

    # create a plot
    plt.title("TSP using OR-Tools") 
    plt.xlabel("longitude caption") 
    plt.ylabel("latitude caption") 
    # choose search strategy : 1 for computationally intractable; 2 for optimal
    option = 2
    options={'computational':1, 'optimal':2}

    data = read_data_model()
    # plot on the screen
    locationsList = np.array(data['locations'])

    # visualize the nodes
    plt.plot(locationsList[:,0],locationsList[:,1],'o')

    distances = compute_euclidean_distance_matrix(data['locations'])

    # create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['locations']), data['num_vehicles'], data['depot'])

    #create routing model
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(fromIndex, toIndex):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        fromNode = manager.IndexToNode(fromIndex)
        toNode = manager.IndexToNode(toIndex)
        return distances[fromNode][toNode]

    transitCallbackIndex = routing.RegisterTransitCallback(distance_callback)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex)

    # Setting first solution heuristic.
    if option == options['computational']:
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
 
    elif option == options['optimal']:
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = 30
        search_parameters.log_search = True
    else:
        print("WARN:No strategy!!")
        sys.exit(0)
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution, locationsList)
