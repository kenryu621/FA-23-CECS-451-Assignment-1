import sys
from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple


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


def convert_coord_to_distance(destination: str, coord_distance_dict):
    lat2, lon2 = coord_distance_dict[destination]
    lat2, lon2 = radians(lat2), radians(lon2)
    for city, coords in coord_distance_dict.items():
        print(f"Converting {city}'s coordinate...")
        lat1, lon1 = coords
        lat1, lon1 = radians(lat1), radians(lon1)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        r = 3958.8
        d = 2 * r * asin(sqrt(a))
        coord_distance_dict[city] = d


def read_coord(search_city: str, coord_dict):
    if search_city not in coord_dict:
        with open("coordinates.txt", "r") as coord_file:
            for coordinate_line in coord_file:
                city_name, coordinate = coordinate_line.split(":")
                if city_name is not search_city:
                    continue
                else:
                    coord_dict[city_name] = coordinate
                    return coordinate
        return False
    else:
        return coord_dict[search_city]


def read_map(search_city: str) -> List[Tuple[str, float]]:
    print(f"\nReading paths from {search_city}...")
    path_tuples = []
    with open("map.txt", "r") as map_file:
        for map_line in map_file:
            start_city_name, paths_str = map_line.split("-")
            if start_city_name == search_city:
                paths = paths_str.replace("\n", "").split(",")
                for path in paths:
                    end_city_name, distance = path.strip("()").split("(")
                    path_tuples.append((end_city_name, float(distance)))
    print(f"    {path_tuples}")
    return path_tuples


def a_star(departure: str, arrival: str, distance_dict):
    print(f"Running A* search from {departure} to {arrival}...")
    read_map(departure)


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
        result = create_coord_dict(departure, arrival, coord_distance_dict)
        # If both city is found, then start A* search
        # Otherwise, tell the user to input command again
        if result == True:
            print("Located both cities in the database.")
            print("Converting coordinates to distance...\n")
            convert_coord_to_distance(arrival, coord_distance_dict)
            print(coord_distance_dict)
            print("\nConversion complete, running A* search...")
            a_star(departure, arrival, coord_distance_dict)
        elif result == False:
            print("Neither city can be located in the database.")
        else:
            print(f'"{result}" is not found in the database, please try again.')


if __name__ == "__main__":
    main()
