# File: src/core.py

class SceneNode:
    def __init__(self, node_id, name, coords, description, data=None):
        """
        :param node_id: A unique identifier (e.g., "cabin.interior")
        :param name: Human-readable name of the location.
        :param coords: Tuple representing physical coordinates (e.g., (0, 0)).
        :param description: Narrative description of the scene.
        :param data: Optional dictionary for additional properties.
        """
        self.node_id = node_id
        self.name = name
        self.coords = coords
        self.description = description
        self.neighbors = {}  # Mapping: neighbor_node_id -> connection details (if any)
        self.data = data or {}

    def add_neighbor(self, neighbor_id, connection_info=None):
        """Link this node to a neighbor. For now, connection_info can be any metadata."""
        self.neighbors[neighbor_id] = connection_info or {}

    def __repr__(self):
        return f"<SceneNode {self.node_id} at {self.coords}>"


class WorldMap:
    def __init__(self):
        self.nodes = {}  # Mapping: node_id -> SceneNode

    def add_node(self, scene_node):
        """Add a new node to the world."""
        self.nodes[scene_node.node_id] = scene_node

    def get_node(self, node_id):
        """Retrieve a node by its unique id."""
        return self.nodes.get(node_id)

    def connect_nodes(self, node_id_a, node_id_b, connection_info=None, bidirectional=True):
        """
        Create a connection between two nodes.
        
        :param node_id_a: ID of the first node.
        :param node_id_b: ID of the second node.
        :param connection_info: Optional dictionary describing the link (e.g., "path": "dirt road").
        :param bidirectional: If True, link both ways.
        """
        node_a = self.get_node(node_id_a)
        node_b = self.get_node(node_id_b)
        if node_a and node_b:
            node_a.add_neighbor(node_b.node_id, connection_info)
            if bidirectional:
                node_b.add_neighbor(node_a.node_id, connection_info)

    def __repr__(self):
        return f"<WorldMap with {len(self.nodes)} nodes>"


class Player:
    def __init__(self, starting_node, health=10):
        """
        :param starting_node: A SceneNode where the player begins.
        :param health: The player’s starting health.
        """
        self.current_node = starting_node
        self.health = health
        self.inventory = []
        self.discovered_nodes = {starting_node.node_id}  # For fog-of-war tracking.

    def move_to(self, new_node):
        """Move the player to a new node and mark it as discovered."""
        self.current_node = new_node
        self.discovered_nodes.add(new_node.node_id)

    def __repr__(self):
        return f"<Player at {self.current_node.node_id} with health {self.health}>"


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the world map and a few scene nodes.
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
    
    # Add nodes to the world.
    world.add_node(cabin_interior)
    world.add_node(cabin_exterior)
    world.add_node(river_side)
    
    # Connect the nodes (here, using simple connection info to describe the link).
    world.connect_nodes("cabin.interior", "cabin.exterior", connection_info={"path": "wooden door"})
    world.connect_nodes("cabin.exterior", "river.side", connection_info={"path": "narrow dirt trail"})
    
    # Create a player starting inside the cabin.
    player = Player(starting_node=cabin_interior)
    
    # Display starting information.
    print(player)
    print("Available paths from current location:")
    for neighbor_id, info in player.current_node.neighbors.items():
        neighbor = world.get_node(neighbor_id)
        print(f" - {neighbor.name} via {info.get('path', 'an unknown path')}")