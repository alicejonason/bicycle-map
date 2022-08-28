import unittest
import json
from bicycle_and_map import *

# Test cases for class Roads
finska_kyrkogrand = Road({"type":"Feature","geometry":
        {"type":"LineString","coordinates":[[18.0726066,59.3258778],
        [18.0726261,59.3257445],[18.0726178,59.3255238]]},"properties":
        {"bicycle":"yes","highway":"pedestrian", "name":"Finska Kyrkogränd"}})

marten_trotzigs_grand = Road({"type":"Feature", "geometry":
        {"type":"LineString","coordinates":[[18.0728411,59.3231371],
        [18.0727421,59.3229742]]},"properties":{"handrail":"no",
        "highway":"steps","incline":"down","lit":"yes",
        "name":"Mårten Trotzigs Gränd","old_name":"Trånga Trappgränden",
        "ramp":"no", "step_count":"36","surface":"unhewn_cobblestone",
        "tourism":"yes","width":"0.9","wikidata":"Q2575880",
        "wikipedia":"sv:Mårten Trotzigs gränd"}})

class TestRoad(unittest.TestCase):
    # Tests for Finska Kyrkogrand
    def test_properties_finska_kyrkogrand(self):
        self.assertTrue(finska_kyrkogrand.properties, 
        {"bicycle":"yes","highway":"pedestrian", "name":"Finska Kyrkogränd"})
    
    def test_coordinates_finska_kyrkogrand(self):
        self.assertTrue(finska_kyrkogrand.coordinates, 
        [[18.0726066,59.3258778],[18.0726261,59.3257445],[18.0726178,59.3255238]])

    def test_distance_finska_kyrkogrand(self):
        self.assertTrue(finska_kyrkogrand.distance, 0.039339654732537505)
    
    def test_road_type_finska_kyrkogrand(self):
        self.assertTrue(finska_kyrkogrand.road_type, 'bicycle')

    def test_color_finska_kyrkogrand(self):
        self.assertTrue(finska_kyrkogrand.color, 'red')
    
    # Tests for Marten Trotzig Grand
    def test_properties_marten_trotzig_grand(self):
        self.assertTrue(marten_trotzigs_grand.properties, 
        {"handrail":"no","highway":"steps","incline":"down","lit":"yes","name":
        "Mårten Trotzigs Gränd","old_name":"Trånga Trappgränden","ramp":"no", 
        "step_count":"36","surface":"unhewn_cobblestone","tourism":"yes","width":
        "0.9","wikidata":"Q2575880","wikipedia":"sv:Mårten Trotzigs gränd"})
    
    def test_coordinates_marten_trotzigs_grand(self):
        self.assertTrue(marten_trotzigs_grand.coordinates, 
        [[18.0728411,59.3231371],[18.0727421,59.3229742]])

    def test_distance_marten_trotzigs_grand(self):
        self.assertTrue(marten_trotzigs_grand.distance, 0.018931148898046705)
    
    def test_road_type_marten_trotzigs_grand(self):
        self.assertTrue(marten_trotzigs_grand.road_type, 'road')

    def test_color_marten_trotzigs_grand(self):
        self.assertTrue(marten_trotzigs_grand.color, 'black')

# Test cases for class Location
e18_500m = Location("e18_500m.json")
helgeandsholmen = Location("helgeandsholmen.json")
gamla_stan = Location("gamla_stan.json")
# Creating a corrupt file where the parameter 'features' is called 'Features'
json_dictionary = {"type":"FeatureCollection","Features":[{"type":"Feature",
"geometry":{"type":"LineString","coordinates":[[18.2245592,59.5477028],
[18.2226495,59.5465337]]},"properties":{"landuse":"forest"}}]}
json_object = json.dumps(json_dictionary)
with open("corrupt.json", "w") as handle:
    handle.write(json_object)

class TestLocation(unittest.TestCase):
    def test_corrupt(self):
        with self.assertRaises(Exception):
            Location("corrupt.json")

    def test_e18_500m(self):
        self.assertEqual(len(e18_500m.list_of_roads), 2)
        self.assertEqual(e18_500m.distances, {'total': '0.90', 'bicycle': '0.00'})
    
    def test_helgeandsholmen(self):
        self.assertEqual(helgeandsholmen.distances, {'total': '1.81', 'bicycle': '0.12'})

    def test_gamla_stan(self):  
        self.assertEqual(gamla_stan.distances, {'total': '27.16', 'bicycle': '11.32'})
    
    def test_t1(self):
        with self.assertRaises(Exception):
            Location("t1.json")

if __name__ == '__main__': 
    unittest.main()
