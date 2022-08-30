# Required modules
import json
import math
from cmath import pi
import matplotlib.pyplot as plt # In terminal: python -m pip install matplotlib
import sys
import os.path

#______________________________________________________________________________#
class Road:
    '''
    A Road has the following attributes:
        properties (dict): A dictionary with properties.
        coordinates (list): A list of lists with x and y coordinates for the 
            points of a road.
        distance (float): The distance in kilometers of the road.
        road_type (str): The type of road (road/bicycle).
        color (str): The color of the road (black/red).
    '''
    def __init__(self, feature):
        self.properties = feature['properties']
        self.coordinates = feature['geometry']['coordinates']
        self.distance = self._calculate_distance()
        self.road_type = self._classify_road_type() 
        self.color = self._determine_color()

    def _calculate_distance(self):
        '''
        Method to calculate the distance in kilometers of a road.
        '''
        distance = 0

        for i in range(len(self.coordinates) - 1):
            # Index i is used to access two (x,y)-points at the time. 
            x1 = self.coordinates[i][0]
            x2 = self.coordinates[i+1][0]
            y1 = self.coordinates[i][1]
            y2 = self.coordinates[i+1][1]
            # Calculating the distance between two points.
            d_x = 111 * (x1 - x2) * math.cos(y1 * pi / 180)
            d_y = 111 * (y1 - y2)
            distance += math.sqrt(d_x ** 2 + d_y ** 2)
        return distance

    def _classify_road_type(self):
        '''
        Method to determine if a road is bicycle friendly. Returns 'bicycle' if 
        bicycle friendly and 'road' otherwise.
        '''
        bicycle_road = False
        
        cond1 = 'bicycle' in self.properties.keys()
        cond2 = self.properties.get('highway') == 'cycleway'
        if cond1 or cond2:
            bicycle_road = True
        
        # Executes only if bicycle_road has not already been determined.
        if not bicycle_road:
            for key in ['cycleway', 'cycleway:left', 
            'cycleway:right', 'cycleway:both']:
                # If key does not exist, .get() returns 'no'. If the value 
                # associated with the key is not 'no', it is bicycle friendly.
                if self.properties.get(key, 'no') != 'no':
                    bicycle_road = True
        
        if bicycle_road:
            return 'bicycle'
        else:
            return 'road'

    def _determine_color(self):
        '''
        Method to determine the color of a road. Returns 'red' if bicycle 
        friendly and 'black' otherwise.
        '''
        if self.road_type == 'bicycle':
            return 'red'
        else:
            return 'black' 

#______________________________________________________________________________#
class Location:
    '''
    A Location has the following attributes:
        file_name (str): A name of a JSON-file, including .json extension.
        features (list): A list of features.
        roads (list): A list of Road-objects.
    '''
    def __init__(self, specific_input=None):
        # Specific_input overrides _get_user_input. The purpose of specific_input
        # is to allow filenames to be specified without user input when running
        # unittests.
        if specific_input:
            self.file_name = specific_input
        else:
            self.file_name = self._get_user_input()
        self.features = self._read_file()
        self.list_of_roads = self._classify_features_as_roads()
        self.distances = self._total_distances()

    def _get_user_input(self):
        '''
        Method to get a file name through user input. If the file does not exist,
        the user can try again. 
        '''
        while True:
            file_name = input("Enter a file name (including .json extension): ")
            if not os.path.exists(os.path.join(sys.path[0], file_name)):
                print("File does not exist. Try another file.")
            else:
                return file_name

    def _read_file(self):
        '''
        Method to read a Location.file_name attribute and return a dictionary.
        Assumes that the file has extension .json and that 
        '''
        try:
            with open(os.path.join(sys.path[0], self.file_name), 'r') as handle:
                return json.load(handle)['features']
        except KeyError:
            raise Exception("File does not have 'feature' parameter.")
    
    def _classify_features_as_roads(self):
        '''
        Method to determine if features are roads. If the feature meets the 
        requirements for a road, a Road-object is instantiated. Returns a list 
        of Road-objects.
        '''
        self.list_of_roads = []

        for feature in self.features:
            cond1 = feature['geometry']['type'] == 'LineString'
            cond2 = 'highway' in feature['properties']
            if cond1 and cond2:
                # If feature is a road, the constructor in Road() is called and 
                # the Road-object is added to roads.
                self.list_of_roads.append(Road(feature))
       
        # If the file does not contain any roads, an Exception is raised and 
        # the user is made aware that there are no roads.
        if len(self.list_of_roads) == 0:
            raise Exception("File does not contain any roads.")

        return self.list_of_roads
    
    def _total_distances(self):
        '''
        Method to calculate the sum the distance of Location.roads, from 
        Roads.coordinates. Returns the distances in kilometers of all roads and 
        all bicycle roads, respectively, rounded to two decimal places.
        '''
        distances = {}
        distances['total'] = sum(road.distance for road in self.list_of_roads)
        distances['bicycle'] = sum(road.distance for road in self.list_of_roads 
        if road.road_type == 'bicycle')

        # Using format() instead of round() as 0.9 should be displayed as 0.90.
        return {key : format(distances[key], '.2f') for key in distances}

#______________________________________________________________________________#
class Map(Location):
    '''
    A Map inherits from Location. When called through Map(), it asks for a file
    by user input, creates a file with a map of the roads in the Location and
    prints the distances of total street length and bicycle friendly length. 
    '''
    def __init__(self, specific_input=None):
        if specific_input:
            super().__init__(specific_input)
        else:
            super().__init__()
        self._create_map()
        self._print_results() 
    
    def _create_map(self):
        '''
        Method to plot the Location.lift_of_roads attributes. Roads are black,
        and bicycle roads are red. The map is saved as a pdf with the same name 
        as the .json file which is supplied through user input.
        '''
        for road in self.list_of_roads:
            x = [coord[0] for coord in road.coordinates]
            y = [coord[1] for coord in road.coordinates]
            plt.plot(x, y, color = road.color, linewidth = 0.7)
        plt.axis('off')
        # Using file_name to save the map with the correct name.
        plt.savefig(self.file_name[:-5] + '.pdf', format = 'pdf')
    
    def _print_results(self):
        '''
        Method to print the distances in kilometers of roads and bicycle roads.
        '''
        print("Total street/road/path length:", str(self.distances['total']), "km")
        print("Bicycle friendly length:", str(self.distances['bicycle']), "km")

if __name__ == '__main__': 
    Map()
