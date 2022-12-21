import utility as utility
import loader as loader
import numpy as np


def main():
    # Paths to the data and solution files.
    vrp_file = "n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "n32-k5.sol"  # "data/n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution: VRP Distance = {}".format(best_distance))

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(nnh_solution, px, py, depot,
    "Nearest Neighbour Heuristic: VRP Distance = {}".format(nnh_distance))

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!

    # sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    # sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    # print("Saving VRP Heuristic Distance:", sh_distance)
    # utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


def get_nearest_neighbour(current, dist_matrix, current_capacity, demand):
    nearest = current
    for i in range(len(dist_matrix[current])):
        if (dist_matrix[current][i] < dist_matrix[current][nearest]) and (current_capacity - demand[i] >= 0):
            nearest = i
    if nearest == current:
        return -1
    else:
        return nearest


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Nearest Neighbour Heuristic to generate VRP solutions.

    current_capacity = capacity
    routes = []

    dist_matrix = []
    for i in range(len(px)):
        dist_i = []
        for j in range(len(px)):
            dist_i.append(utility.calculate_euclidean_distance(px, py, i, j))
            if i == j or j == depot:
                dist_i[j] = float('inf')
        dist_matrix.append(dist_i)

    visited_nodes = [depot]
    current = depot
    route = []

    while len(visited_nodes) < len(px):
        nearest = get_nearest_neighbour(current, dist_matrix, current_capacity, demand)
        if nearest == -1:
            routes.append(route)
            route = []
            current = depot
            current_capacity = capacity
        else:
            current = nearest
            route.append(current)
            current_capacity -= demand[current]
            visited_nodes.append(current)
            for row in dist_matrix:
                row[current] = float('inf')

    routes.append(route)

    return routes


def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Saving Heuristic to generate VRP solutions.

    routes = []

    for i in range(len(px)):
        if i == depot:
            continue
        routes.append([i])

    savings = {}

    for node_i in range(len(routes)):
        for node_j in range(len(routes)):
            if node_i != node_j and node_i != depot and node_j != depot:
                savings[(node_i, node_j)] = utility.calculate_euclidean_distance(px, py, routes[node_i], depot) + \
                                            utility.calculate_euclidean_distance(px, py, routes[node_j], depot) - \
                                            utility.calculate_euclidean_distance(px, py, routes[node_i], routes[node_j])

    savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    while savings:
        feasible_savings = savings
        while feasible_savings:
            merge = feasible_savings[0][0]

            route_1 = None
            route_2 = None

            for route in routes:
                if route[-1] == merge[0]:
                    route_1 = route

            for route in routes:
                if route[0] == merge[1]:
                    route_2 = route

            if route_1 is not None and route_2 is not None:

                merged_route = route_1 + route_2

                current_capacity = 0

                for n in merged_route:
                    current_capacity += demand[n]

                if current_capacity <= capacity:
                    routes.append(merged_route)
                    routes.remove(route_1)
                    routes.remove(route_2)

                    for s in savings:
                        if s[0][0] == merge[0]:
                            savings.remove(s)

                    for s in savings:
                        if merge[0] in s[0] and merge[1] in s[0]:
                            savings.remove(s)

                    if len(merged_route) > 2:
                        savings_to_remove = []
                        for s in savings:
                            if all(item in merged_route for item in list(s[0])):
                                savings_to_remove.append(s)
                        for s in savings_to_remove:
                            savings.remove(s)
                else:
                    feasible_savings.remove(feasible_savings[0])
            else:
                feasible_savings.remove(feasible_savings[0])

        savings_to_remove = []
        for s in savings:
            if any(item in routes[-1] for item in list(s[0])):
                savings_to_remove.append(s)
        for s in savings_to_remove:
            savings.remove(s)

    return routes


if __name__ == '__main__':
    main()
