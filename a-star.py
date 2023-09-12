import sys
from math import asin, cos, radians, sin, sqrt
from queue import PriorityQueue
from typing import List
import copy


# Data class Route that store route information from map.txt file
class Route:
    city_name: str
    distance: float

    def __init__(self, name, dist) -> None:
        self.city_name = name
        self.distance = dist


# create_coord_dict function to read through the coordinates.txt file
def create_coord_dict(city1: str, city2: str, coord_dict):
    # Create two flags to detect if we can find both city
    city1_found, city2_found = False, False
    # Opening coordinates file to create coordinate dictionary
    with open("coordinates.txt", "r") as coord_file:
        for coordinate_line in coord_file:
            city_name, coordinate = coordinate_line.split(":")
            coord_dict[city_name] = tuple(
                float(value)
                for value in coordinate.replace("\n", "").strip("()").split(",")
            )
            # Change flag to true if we found demanded city in the file
            if city_name == city1:
                city1_found = True
            if city_name == city2:
                city2_found = True
    # Returning result
    if city1_found and city2_found:
        return True
    elif city1_found:
        return city2
    elif city2_found:
        return city1
    else:
        return False


# convert_coord_to_distance function to convert coordinates to distance to the destination
def convert_coord_to_distance(destination: str, coord_distance_dict):
    lat2, lon2 = coord_distance_dict[destination]
    lat2, lon2 = radians(lat2), radians(lon2)
    for city, coords in coord_distance_dict.items():
        lat1, lon1 = coords
        lat1, lon1 = radians(lat1), radians(lon1)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        r = 3958.8
        d = 2 * r * asin(sqrt(a))
        coord_distance_dict[city] = d


# read_map function to read map.txt and return list of Routes that is available for current city
def read_map(search_city: str) -> List[Route]:
    # Initialize empty list of tuples to hold city names and distances
    path_list = []
    with open("map.txt", "r") as map_file:
        for map_line in map_file:
            # Find available routes from departure city
            start_city_name, paths_str = map_line.split("-")
            if start_city_name == search_city:
                # Read routes information and store it in list
                paths = paths_str.replace("\n", "").split(",")
                for path in paths:
                    end_city_name, distance = path.strip("()").split("(")
                    path_list.append(Route(end_city_name, float(distance)))
    return path_list


# A* algorithm to find optimal route from departure to arrival
def a_star(departure: str, arrival: str, distance_dict) -> [str, float]:
    # Initial state from departure city
    city_queue = PriorityQueue()
    city_queue.put((0, departure))
    last_stop = {}
    cost_so_far = {}
    last_stop[departure] = None
    cost_so_far[departure] = 0
    # Starting route search
    while not city_queue.empty():
        # A* search on the city with lowest cost
        current_city = city_queue.get()[1]
        # If we found arrival, stop algorithm
        if current_city == arrival:
            break
        # Iterate through available routes
        for neighbor in read_map(current_city):
            # Compute the potential cost for that city
            new_cost = cost_so_far[current_city] + neighbor.distance
            # If the cost is not recorded or lower cost is found,
            # update the queue, cost record, and route record
            if (
                neighbor.city_name not in cost_so_far
                or new_cost < cost_so_far[neighbor.city_name]
            ):
                cost_so_far[neighbor.city_name] = new_cost
                # Update the priority queue with new cost and distance
                city_queue.put(
                    (new_cost + distance_dict[neighbor.city_name], neighbor.city_name)
                )
                last_stop[neighbor.city_name] = current_city
    # Finalizing desired information
    best_route = ""
    best_route_iterator = arrival
    # Create best route by combining route record
    while best_route_iterator != None:
        best_route = " - " + best_route_iterator + best_route
        best_route_iterator = last_stop[best_route_iterator]
    # Returning the best route and route cost
    return best_route.strip(" - "), cost_so_far[arrival]


def main():
    # End the program if arguments are invalid
    if len(sys.argv) != 3:
        print("Invalid number of arguments, please try again.")
        print(
            'Remember there should be no space in a city name, for example, "San Jose" should be "SanJose"'
        )
        return None
    else:
        departure, arrival = sys.argv[1:3]
        coord_distance_dict = {}
        if departure == arrival:
            print(f"You entered the same city for departure and arrival: {departure}")
            print("Please try again.")
            return
        result = create_coord_dict(departure, arrival, coord_distance_dict)
        # If both city is found, then start A* search
        # Otherwise, tell the user to input command again
        if result == True:
            convert_coord_to_distance(arrival, coord_distance_dict)
            best_route, cost = a_star(departure, arrival, coord_distance_dict)
            # Printing results
            print(f"From city: {departure}")
            print(f"To city: {arrival}")
            print(f"Best route: {best_route}")
            print(f"Total distance: {cost:.2f} mi")
        # Warns user if the input cannot be found in the database
        elif result == False:
            print("Neither city can be located in the database.")
        else:
            print(f'"{result}" is not found in the database, please try again.')


if __name__ == "__main__":
    main()
