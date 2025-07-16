import json
import logging
from collections import deque

class CampusPathfinder:
    def __init__(self, data_file='campus_data.json'):
        """Initialize the pathfinder with campus data"""
        self.campus_data = self.load_campus_data(data_file)
        self.floors = self.campus_data['floors']
        self.floor_connections = self.campus_data['floor_connections']
        
    def load_campus_data(self, data_file):
        """Load campus data from JSON file"""
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Campus data file {data_file} not found")
            return {"floors": {}, "floor_connections": {}}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {data_file}")
            return {"floors": {}, "floor_connections": {}}
    
    def get_all_locations(self):
        """Get all available locations grouped by floor"""
        locations = {}
        for floor_id, floor_data in self.floors.items():
            locations[floor_id] = {
                'name': floor_data['name'],
                'locations': []
            }
            for loc_id, loc_data in floor_data['locations'].items():
                if loc_id != 'stairs':  # Don't include stairs in location list
                    locations[floor_id]['locations'].append({
                        'id': loc_id,
                        'name': loc_data['name'],
                        'description': loc_data['description']
                    })
        return locations
    
    def find_location_floor(self, location_name):
        """Find which floor a location is on"""
        location_name = location_name.lower().strip()
        for floor_id, floor_data in self.floors.items():
            if location_name in floor_data['locations']:
                return floor_id
        return None
    
    def find_path(self, start, destination):
        """Find path between two locations using BFS"""
        start = start.lower().strip()
        destination = destination.lower().strip()
        
        # Check if locations exist
        start_floor = self.find_location_floor(start)
        dest_floor = self.find_location_floor(destination)
        
        if not start_floor or not dest_floor:
            return None
        
        # If same location
        if start == destination:
            return [f"You are already at {self.floors[start_floor]['locations'][start]['name']}!"]
        
        # BFS to find path
        queue = deque([(start_floor, start, [])])
        visited = set()
        
        while queue:
            current_floor, current_location, path = queue.popleft()
            
            if (current_floor, current_location) in visited:
                continue
            
            visited.add((current_floor, current_location))
            
            # If we reached destination
            if current_location == destination:
                return self.generate_directions(path + [(current_floor, current_location)])
            
            # Get current location data
            current_data = self.floors[current_floor]['locations'][current_location]
            
            # Explore connections on same floor
            for connection in current_data['connections']:
                if connection in self.floors[current_floor]['locations']:
                    if (current_floor, connection) not in visited:
                        queue.append((current_floor, connection, path + [(current_floor, current_location)]))
            
            # If current location has floor connection (stairs), explore next floor
            if 'floor_connection' in current_data:
                next_floor = current_data['floor_connection']
                if next_floor in self.floors:
                    # Add stairs to path and continue from stairs on next floor
                    stairs_path = path + [(current_floor, current_location), (current_floor, 'stairs')]
                    queue.append((next_floor, 'stairs', stairs_path))
            
            # Also check if we can go to previous floor via stairs
            if current_location == 'stairs':
                for floor_id, floor_data in self.floors.items():
                    if floor_id != current_floor and 'stairs' in floor_data['locations']:
                        stairs_data = floor_data['locations']['stairs']
                        if 'floor_connection' in stairs_data and stairs_data['floor_connection'] == current_floor:
                            queue.append((floor_id, 'stairs', path + [(current_floor, current_location)]))
        
        return None
    
    def generate_directions(self, path):
        """Generate human-readable directions from path"""
        if not path:
            return []
        
        directions = []
        current_floor = None
        
        for i, (floor, location) in enumerate(path):
            location_name = self.floors[floor]['locations'][location]['name']
            
            if i == 0:
                directions.append(f"Starting from {location_name}")
                current_floor = floor
            elif location == 'stairs' and floor != current_floor:
                # Going up or down stairs
                if self.get_floor_number(floor) > self.get_floor_number(current_floor):
                    directions.append(f"→ Take stairs up to {self.floors[floor]['name']}")
                else:
                    directions.append(f"→ Take stairs down to {self.floors[floor]['name']}")
                current_floor = floor
            elif location != 'stairs':
                if i == len(path) - 1:
                    directions.append(f"→ {location_name} is your destination")
                    directions.append("→ You have reached your destination!!")
                else:
                    # Check if this is a landmark or intermediate location
                    next_floor, next_location = path[i + 1]
                    if next_location == 'stairs':
                        directions.append(f"→ Pass by {location_name}")
                    else:
                        directions.append(f"→ Head towards {location_name}")
        
        return directions
    
    def get_floor_number(self, floor_id):
        """Get numeric floor number for comparison"""
        floor_order = {'ground': 0, 'first': 1, 'second': 2, 'third': 3}
        return floor_order.get(floor_id, 0)
