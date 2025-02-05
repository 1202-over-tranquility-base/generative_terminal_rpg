class SceneNode:
    def __init__(self, node_id, name, coords, description, data=None):
        self.node_id = node_id
        self.name = name
        self.coords = coords
        self.description = description
        self.neighbors = {}  # neighbor_node_id -> connection info
        self.data = data or {}
        self.discovered = False
        self.last_visited = None
        self.created_day = None
        self.persistent = False

    def add_neighbor(self, neighbor_id, connection_info=None):
        self.neighbors[neighbor_id] = connection_info or {}

    def __repr__(self):
        return f"<SceneNode {self.node_id} at {self.coords}>"


class WorldMap:
    def __init__(self):
        self.nodes = {}  # node_id -> SceneNode

    def add_node(self, scene_node):
        self.nodes[scene_node.node_id] = scene_node

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def connect_nodes(self, node_id_a, node_id_b, connection_info=None, bidirectional=True):
        node_a = self.get_node(node_id_a)
        node_b = self.get_node(node_id_b)
        if node_a and node_b:
            node_a.add_neighbor(node_b.node_id, connection_info)
            if bidirectional:
                node_b.add_neighbor(node_a.node_id, connection_info)

    def prune_old_nodes(self, current_day, decay_threshold):
        # Remove nodes that haven't been visited in decay_threshold days (if not persistent)
        to_remove = []
        for node_id, node in list(self.nodes.items()):
            # Use the last interaction time (visited or creation)
            last_time = node.last_visited if node.last_visited is not None else node.created_day
            if (not node.persistent and last_time is not None 
                    and (current_day - last_time > decay_threshold)):
                to_remove.append(node_id)
        for node_id in to_remove:
            # Remove connections pointing to this node
            for node in self.nodes.values():
                if node_id in node.neighbors:
                    del node.neighbors[node_id]
            del self.nodes[node_id]

    def display_map(self, player):
        # Show only discovered nodes in a simple grid.
        discovered_nodes = [node for node in self.nodes.values() if node.discovered]
        if not discovered_nodes:
            print("Map is empty.")
            return
        xs = [node.coords[0] for node in discovered_nodes]
        ys = [node.coords[1] for node in discovered_nodes]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        for y in range(max_y, min_y - 1, -1):
            row = ""
            for x in range(min_x, max_x + 1):
                node_here = next((node for node in discovered_nodes if node.coords == (x, y)), None)
                if node_here:
                    if node_here.node_id == player.current_node.node_id:
                        row += " P "  # P for Player’s current location
                    else:
                        row += " X "  # X marks a discovered node
                else:
                    row += " . "  # Dot means no discovered node here
            print(row)

    def __repr__(self):
        return f"<WorldMap with {len(self.nodes)} nodes>"


class Player:
    def __init__(self, starting_node, health=10):
        self.current_node = starting_node
        self.health = health
        self.inventory = []
        self.discovered_nodes = {starting_node.node_id}
        self.current_day = 0
        starting_node.discovered = True
        starting_node.last_visited = self.current_day
        if starting_node.created_day is None:
            starting_node.created_day = self.current_day

    def move_to(self, new_node):
        self.current_node = new_node
        self.discovered_nodes.add(new_node.node_id)
        new_node.discovered = True
        self.current_day += 1
        new_node.last_visited = self.current_day
        if new_node.created_day is None:
            new_node.created_day = self.current_day

    def __repr__(self):
        return f"<Player at {self.current_node.node_id} with health {self.health}>"


# --- Example Usage (for quick testing) ---
if __name__ == "__main__":
    world = WorldMap()
    
    cabin_interior = SceneNode(
        node_id="cabin.interior",
        name="Cabin Interior",
        coords=(0, 0),
        description="You are inside a small, creaking cabin in the woods."
    )
    
    cabin_exterior = SceneNode(
        node_id="cabin.exterior",
        name="Cabin Exterior",
        coords=(1, 0),
        description="Stepping outside, you see the wilds beckoning."
    )
    
    river_side = SceneNode(
        node_id="river.side",
        name="River Side",
        coords=(2, 0),
        description="A gentle river flows nearby, its banks inviting exploration."
    )
    
    world.add_node(cabin_interior)
    world.add_node(cabin_exterior)
    world.add_node(river_side)
    
    world.connect_nodes("cabin.interior", "cabin.exterior", connection_info={"path": "wooden door"})
    world.connect_nodes("cabin.exterior", "river.side", connection_info={"path": "narrow dirt trail"})
    
    player = Player(starting_node=cabin_interior)
    
    print(player)
    print("Available paths from current location:")
    for neighbor_id, info in player.current_node.neighbors.items():
        neighbor = world.get_node(neighbor_id)
        print(f" - {neighbor.name} via {info.get('path', 'an unknown path')}")