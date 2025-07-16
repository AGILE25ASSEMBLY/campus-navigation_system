import json
import logging
from typing import Dict, List, Tuple, Optional

class CampusNavigator:
    def __init__(self, data_file='campus_data.json'):
        """Initialize the campus navigator with location data"""
        self.campus_data = self._load_campus_data(data_file)
        self.locations_index = self._build_locations_index()
        
    def _load_campus_data(self, data_file: str) -> Dict:
        """Load campus data from JSON file"""
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Campus data file {data_file} not found")
            return {"floors": {}}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {data_file}")
            return {"floors": {}}
    
    def _build_locations_index(self) -> Dict[str, Dict]:
        """Build an index of all locations across floors"""
        index = {}
        for floor_key, floor_data in self.campus_data.get("floors", {}).items():
            for location_key, location_data in floor_data.get("locations", {}).items():
                index[location_key] = {
                    "floor": floor_key,
                    "data": location_data
                }
        return index
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations organized by floor"""
        locations = []
        for floor_key, floor_data in self.campus_data.get("floors", {}).items():
            floor_locations = []
            for location_key, location_data in floor_data.get("locations", {}).items():
                if not location_key.startswith("stairs"):
                    floor_locations.append({
                        "key": location_key,
                        "name": location_data.get("name", location_key.title())
                    })
            
            if floor_locations:
                locations.append({
                    "floor": floor_data.get("name", floor_key.title()),
                    "locations": floor_locations
                })
        
        return locations
    
    def search_locations(self, query: str) -> List[Dict]:
        """Search for locations matching the query"""
        results = []
        query_lower = query.lower()
        
        for location_key, location_info in self.locations_index.items():
            if query_lower in location_key or query_lower in location_info["data"].get("name", "").lower():
                if not location_key.startswith("stairs"):
                    results.append({
                        "key": location_key,
                        "name": location_info["data"].get("name", location_key.title()),
                        "floor": location_info["floor"]
                    })
        
        return results
    
    def find_location(self, location_name: str) -> Optional[Tuple[str, str]]:
        """Find a location by name and return (floor, location_key)"""
        location_lower = location_name.lower()
        
        # Direct match
        if location_lower in self.locations_index:
            return self.locations_index[location_lower]["floor"], location_lower
        
        # Partial match
        for location_key, location_info in self.locations_index.items():
            if location_lower in location_key or location_lower in location_info["data"].get("name", "").lower():
                return location_info["floor"], location_key
        
        return None
    
    def get_directions(self, start: str, destination: str) -> Dict:
        """Get step-by-step directions from start to destination"""
        # Find start and destination locations
        start_info = self.find_location(start)
        dest_info = self.find_location(destination)
        
        if not start_info:
            return {"success": False, "error": f"Starting location '{start}' not found"}
        
        if not dest_info:
            return {"success": False, "error": f"Destination '{destination}' not found"}
        
        start_floor, start_key = start_info
        dest_floor, dest_key = dest_info
        
        if start_key == dest_key:
            return {"success": False, "error": "You are already at your destination!"}
        
        # Generate directions
        directions = self._generate_directions(start_floor, start_key, dest_floor, dest_key)
        
        return {"success": True, "directions": directions}
    
    def _generate_directions(self, start_floor: str, start_key: str, dest_floor: str, dest_key: str) -> List[str]:
        """Generate step-by-step directions"""
        directions = []
        current_floor = start_floor
        current_location = start_key
        
        # Get location names for display
        start_name = self.locations_index[start_key]["data"].get("name", start_key.title())
        dest_name = self.locations_index[dest_key]["data"].get("name", dest_key.title())
        
        directions.append(f"From {start_name}")
        
        # If same floor, provide direct navigation
        if start_floor == dest_floor:
            directions.extend(self._get_same_floor_directions(start_floor, start_key, dest_key))
        else:
            # Navigate to different floor
            directions.extend(self._get_multi_floor_directions(start_floor, start_key, dest_floor, dest_key))
        
        directions.append(f"→ You have reached your destination: {dest_name}!")
        
        return directions
    
    def _get_same_floor_directions(self, floor: str, start_key: str, dest_key: str) -> List[str]:
        """Get directions within the same floor"""
        directions = []
        floor_data = self.campus_data["floors"][floor]
        
        # Simple pathfinding using BFS
        path = self._find_path(floor_data, start_key, dest_key)
        
        if len(path) <= 2:
            directions.append(f"→ Go directly to {self.locations_index[dest_key]['data'].get('name', dest_key.title())}")
        else:
            for i in range(1, len(path) - 1):
                location = path[i]
                location_name = floor_data["locations"][location].get("name", location.title())
                directions.append(f"→ Pass by {location_name}")
        
        return directions
    
    def _get_multi_floor_directions(self, start_floor: str, start_key: str, dest_floor: str, dest_key: str) -> List[str]:
        """Get directions across multiple floors"""
        directions = []
        
        # Define floor hierarchy
        floor_order = ["ground", "first", "second", "third"]
        start_level = floor_order.index(start_floor)
        dest_level = floor_order.index(dest_floor)
        
        current_floor = start_floor
        current_level = start_level
        
        # Navigate through floors
        while current_level != dest_level:
            if current_level < dest_level:
                # Going up
                next_floor = floor_order[current_level + 1]
                stair_location = self._find_stairs_to_floor(current_floor, next_floor)
                if stair_location:
                    directions.append(f"→ Take stairs and go up to {self.campus_data['floors'][next_floor]['name']}")
                    current_floor = next_floor
                    current_level += 1
                else:
                    directions.append(f"→ Find stairs to go up to {self.campus_data['floors'][next_floor]['name']}")
                    current_floor = next_floor
                    current_level += 1
            else:
                # Going down
                next_floor = floor_order[current_level - 1]
                stair_location = self._find_stairs_to_floor(current_floor, next_floor)
                if stair_location:
                    directions.append(f"→ Take stairs and go down to {self.campus_data['floors'][next_floor]['name']}")
                    current_floor = next_floor
                    current_level -= 1
                else:
                    directions.append(f"→ Find stairs to go down to {self.campus_data['floors'][next_floor]['name']}")
                    current_floor = next_floor
                    current_level -= 1
        
        # Now navigate on the destination floor
        if current_floor == dest_floor:
            # Add specific directions based on your campus layout
            if dest_floor == "first" and dest_key == "lh1":
                directions.append("→ In the centre, you will witness the Department of Computer Science and Engineering")
                directions.append("→ LH1 is next to the CSE Department")
            elif dest_floor == "third":
                directions.append("→ In the centre, you will witness the Centralised Lab")
                dest_name = self.locations_index[dest_key]["data"].get("name", dest_key.title())
                if "placement office" in dest_key:
                    directions.append(f"→ {dest_name} is next to Centralised Lab")
                else:
                    directions.append(f"→ Navigate to {dest_name}")
            else:
                dest_name = self.locations_index[dest_key]["data"].get("name", dest_key.title())
                directions.append(f"→ Navigate to {dest_name}")
        
        return directions
    
    def _find_stairs_to_floor(self, current_floor: str, target_floor: str) -> Optional[str]:
        """Find stairs connection to target floor"""
        floor_data = self.campus_data["floors"][current_floor]
        
        for location_key, location_data in floor_data["locations"].items():
            if location_key.startswith("stairs") and location_data.get("transition") == target_floor:
                return location_key
        
        return None
    
    def _find_path(self, floor_data: Dict, start: str, end: str) -> List[str]:
        """Find path between two locations on the same floor using BFS"""
        from collections import deque
        
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                return path
            
            current_data = floor_data["locations"].get(current, {})
            connections = current_data.get("connections", [])
            
            for connection in connections:
                if connection not in visited and connection in floor_data["locations"]:
                    visited.add(connection)
                    queue.append((connection, path + [connection]))
        
        return [start, end]  # Fallback direct path
