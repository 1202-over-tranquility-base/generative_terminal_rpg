import networkx as nx
from models import Scene, Option, GameObject

class NodeManager:
    def __init__(self):
        # Create a directed graph to represent the world.
        self.graph = nx.DiGraph()
        # A global registry of movable objects (e.g., the boat).
        self.objects = {}
        self._load_sample_nodes()

    def _load_sample_nodes(self):
        # Define options for each node
        cabin_interior_options = [
            Option("Step outside to start the day", "cabin_exterior")
        ]
        cabin_exterior_options = [
            Option("Travel north along the path", "river_side_0"),
            Option("Travel south along the path", "cabin_interior")
        ]
        river_side_0_options = [
            Option("Turn back towards the house", "cabin_exterior"),
            Option("Use the boat to cross the river", "river_side_1")
        ]
        river_side_1_options = [
            Option("Turn back towards the boat", "river_side_0"),
            Option("Return home", "cabin_exterior")
        ]
        
        # Create Scenes with narrative text and options
        cabin_interior_scene = Scene(
            "You wake up in a small, creaking cabin deep in the woods.",
            "Morning light streams through the window, heralding the start of your adventure.",
            cabin_interior_options
        )
        cabin_exterior_scene = Scene(
            "You step outside and are greeted by the wild.",
            "A narrow path stretches out before you, inviting exploration.",
            cabin_exterior_options
        )
        river_side_0_scene = Scene(
            "You arrive at the edge of a gently flowing river.",
            "A small boat is tied here, its paint peeling and waiting for use.",
            river_side_0_options
        )
        river_side_1_scene = Scene(
            "You stand on the opposite bank of the river.",
            "The current rushes behind you, and familiar landmarks hint at home.",
            river_side_1_options
        )

        # Add nodes to the graph with attributes:
        # Each node gets a unique id, a scene, coordinates (x, y), and an empty objects dict.
        self.graph.add_node("cabin_interior", scene=cabin_interior_scene, coords=(0, 0), objects={})
        self.graph.add_node("cabin_exterior", scene=cabin_exterior_scene, coords=(1, 0), objects={})
        self.graph.add_node("river_side_0", scene=river_side_0_scene, coords=(2, 0), objects={})
        self.graph.add_node("river_side_1", scene=river_side_1_scene, coords=(2, -1), objects={})
        
        # Optionally add directed edges from each node to its target nodes.
        for node in self.graph.nodes:
            scene = self.graph.nodes[node]["scene"]
            for option in scene.options:
                self.graph.add_edge(node, option.target_node, description=option.description)
        
        # Create and place a boat object at the river_side_0 node.
        boat = GameObject("boat", "A small, creaky boat.", "river_side_0")
        self.objects[boat.object_id] = boat
        self.graph.nodes["river_side_0"]["objects"][boat.object_id] = boat

    def get_node(self, node_id):
        return self.graph.nodes.get(node_id)

    def move_object(self, object_id, target_node_id):
        obj = self.objects.get(object_id)
        if not obj:
            return
        current_node_id = obj.current_node
        # Remove the object from its current node
        if object_id in self.graph.nodes[current_node_id]["objects"]:
            del self.graph.nodes[current_node_id]["objects"][object_id]
        # Update the object's current node and add it to the target node.
        obj.current_node = target_node_id
        self.graph.nodes[target_node_id]["objects"][object_id] = obj