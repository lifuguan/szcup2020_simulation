
#%% import necessary library
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import xlrd, math
import sys
import matplotlib.pyplot as plt
import numpy as np

#%% read data from xlsx
def read_data_model():
    """Stores the data for the problem."""
    data = xlrd.open_workbook("../data/C2.xlsx")
    table = data.sheet_by_name("Sheet1")
    rowNum = table.nrows
    colNum = table.ncols
    data = {}
    data['velocity'] = 100

    # time windows : An array of time windows for the locations.
    data['timeWindows'] = []
    for i in range(1, rowNum):
        if i == 1:
            data['timeWindows'].append((0, 0))
        else:
            data['timeWindows'].append((0, int((39305) / 100 / 2)))
    
    data['locations'] = []
    for i in range(1, rowNum):
        data['locations'].append([(table.cell_value(i,1) - 120)*708883, (table.cell_value(i,2) - 36)*111194])

    # time matrix : An array of travel times between locations.
    data['timeMatrix'] = {}
    for fromCounter, fromNode in enumerate(data['locations']):
        data['timeMatrix'][fromCounter] = {}
        for toCounter, toNode in enumerate(data['locations']):
            if fromCounter == toCounter:
                data['timeMatrix'][fromCounter][toCounter] = 0
            else:
                # data['timeMatrix']  = distance / velocity
                data['timeMatrix'][fromCounter][toCounter] = int(math.hypot(fromNode[0] - toNode[0], fromNode[1] - toNode[1]) / data['velocity'])

    # the number of vehicles of the fleet.
    data['numVehicles'] = 4

    # the index of the depot.
    data['depot'] = 0
    return data

#%%
def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0

    colors = {0:'coral',1:'r',2:'g',3:'b'}
    # create a plot
    plt.title("VRPTW using OR-Tools") 
    plt.xlabel("longitude caption") 
    plt.ylabel("latitude caption") 

    # plot on the screen
    locationsList = np.array(data['locations'])

    # commit on the plot
    plt.annotate(r'$depot$',
            xy=(locationsList[0]), xycoords='data',
            xytext=(+10, +30), textcoords='offset points', fontsize=16,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    # visualize the nodes
    plt.plot(locationsList[:,0],locationsList[:,1],'o')

    for vehicle_id in range(data['numVehicles']):

        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            previous_index = index
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
            
            # line
            plt.plot([locationsList[previous_index if previous_index < 30 else 0][0],locationsList[index if index < 30 else 0][0]], 
                [locationsList[previous_index if previous_index < 30 else 0][1],locationsList[index if index < 30 else 0][1]], color = colors[vehicle_id])
        time_var = time_dimension.CumulVar(index)

        plt.plot([locationsList[index if index < 30 else 0][0],locationsList[0][0]], [locationsList[index if index < 30 else 0][1],locationsList[0][1]], color = colors[vehicle_id])

        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {} seconds\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))


#%%



"""Solve the VRP with time windows."""
# Instantiate the data problem.
data = read_data_model()

#%%
# Create the routing index manager.
manager = pywrapcp.RoutingIndexManager(len(data['timeMatrix']),
                                        data['numVehicles'], data['depot'])

# Create Routing Model.
routing = pywrapcp.RoutingModel(manager)


# Create and register a transit callback.
def time_callback(from_index, to_index):
    """Returns the travel time between the two nodes."""
    # Convert from routing variable Index to time matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['timeMatrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(time_callback)

# Define cost of each arc.
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Add Time Windows constraint.
time = 'Time'
routing.AddDimension(
    transit_callback_index,
    10,  # allow waiting time
    180,  # maximum time per vehicle
    False,  # Don't force start cumul to zero.
    time)
time_dimension = routing.GetDimensionOrDie(time)
# Add time window constraints for each location except depot.
for location_idx, time_window in enumerate(data['timeWindows']):
    if location_idx == 0:
        continue
    index = manager.NodeToIndex(location_idx)
    time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])


# Add time window constraints for each vehicle start node.
for vehicle_id in range(data['numVehicles']):
    index = routing.Start(vehicle_id)
    time_dimension.CumulVar(index).SetRange(data['timeWindows'][0][0],
                                            data['timeWindows'][0][1])

# Instantiate route start and end times to produce feasible times.
for i in range(data['numVehicles']):
    routing.AddVariableMinimizedByFinalizer(
        time_dimension.CumulVar(routing.Start(i)))
    routing.AddVariableMinimizedByFinalizer(
        time_dimension.CumulVar(routing.End(i)))

# Setting first solution heuristic.
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.seconds = 30
search_parameters.log_search = True

# Solve the problem.
solution = routing.SolveWithParameters(search_parameters)

# Print solution on console.
if solution:
    print_solution(data, manager, routing, solution)
