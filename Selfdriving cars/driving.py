from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import argparse
from timeit import default_timer as timer

def create_data_model(distance, time, v):
  """Stores the data for the problem."""
  data = {}
  data['time_matrix'] = distance
  data['time_windows'] = time
  data['num_vehicles'] = v
  data['depot'] = 0
  return data

def print_solution(data, manager, routing, assignment, o):
    """Prints assignment on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        aux = []
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), assignment.Min(time_var),
                assignment.Max(time_var))
            index = assignment.Value(routing.NextVar(index))
            if not routing.IsEnd(index):
                aux.append(str(index - 1))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(
            manager.IndexToNode(index), assignment.Min(time_var),
            assignment.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            assignment.Min(time_var))
        #print(plan_output)
        total_time += assignment.Min(time_var)
        o.write(str(len(aux)))
        for element in aux:
            o.write(" ")
            o.write(str(element))
        o.write('\n')
    print('Total time of all routes: {}min'.format(total_time))

def main():
    parser = argparse.ArgumentParser(description='Spreading vehicles fleet arounde the city.')
    
    """
    parser.add_argument("-f", "--file", default='C:\\Users\\jose.gariburo\\Documents\\Google\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\a_example.in',
                        type=argparse.FileType('r'), help='Filename with input data.')                        
    parser.add_argument("-f", "--file", default='C:\\Users\\jose.gariburo\\Documents\\Google\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\b_should_be_easy.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    parser.add_argument("-f", "--file", default='C:\\Users\\jose.gariburo\\Documents\\Google\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\c_no_hurry.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    parser.add_argument("-f", "--file", default='C:\\Users\\jose.gariburo\\Documents\\Google\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\d_metropolis.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    parser.add_argument("-f", "--file", default='C:\\Users\\jose.gariburo\\Documents\\Google\\Google Hash Code 2018\\HashCode2018_Pastutatis\\Selfdriving cars\\e_high_bonus.in',
                        type=argparse.FileType('r'), help='Filename with input data.')
    """
    
    args = parser.parse_args()
    outFile = open(args.file.name.split(".in")[0] + ".out", "w")
    lines = args.file.readlines()
    args.file.close()
    v = int(lines[0].split()[2])
    distance = []
    time = []
    ttl = 0
    for i in range(len(lines)):
        l = lines[i].split()
        if i == 0:
            time.insert(i, (i, int(l[5]) - 1))
            ttl = int(l[5]) - 1
        else:
            time.insert(i, (int(l[4]), int(l[5])))
            ttl = max(ttl, int(l[5]) - int(l[4]))
    ttl = int(ttl / int(lines[0].split()[3]))

    startix = 0
    startiy = 0
    endix = 0
    endiy = 0
    for i in range(len(lines)):
        inter = []        
        if i != 0:       
            li = lines[i].split()
            startix = int(li[0])
            startiy = int(li[1])
            endix = int(li[2])
            endiy = int(li[3])
        startjx = 0
        startjy = 0
        endjx = 0
        endjy = 0
        for j in range(len(lines)):            
            if j != 0:
                lj = lines[j].split()
                startjx = int(lj[0])
                startjy = int(lj[1])
                endjx = int(lj[2])
                endjy = int(lj[3])
            if i == j:
                inter.append(0)
            else:
                # Add distance
                inter.append(abs(endix - startjx) + abs(endiy - startjy) + abs(endjx - startjx) + abs(endjy - startjy))
        #distance.insert(i, inter)
        distance = distance + [inter]

    data = create_data_model(distance, time, v)
    manager = pywrapcp.RoutingIndexManager(
        len(data['time_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        0,  # allow waiting time
        ttl,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        print_solution(data, manager, routing, assignment, outFile)
    outFile.close()

if __name__ == '__main__':
  main()