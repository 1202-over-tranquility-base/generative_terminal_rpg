import networkx as nx
import json
import os
from models import Scene, Option, GameObject

class NodeManager:
    def __init__(self, world_file="world.json"):
        self.graph = nx.DiGraph()
        self.objects = {}
        self._load_world(world_file)

    def _load_world(self, world_file):
        # Load the JSON world file.
        world_path = os.path.join(os.path.dirname(__file__), world_file)
        with open(world_path, "r") as f:
            data = json.load(f)

        scenes_data = data["scenes"]

        # Create nodes using the hierarchical ID provided.
        for scene_data in scenes_data:
            scene_id = scene_data["id"]  # e.g., "cabin.interior", "cabin.exterior", etc.
            options = []
            for opt_data in scene_data.get("options", []):
                options.append(Option(
                    description=opt_data["description"],
                    target_node=opt_data["target"]  # Expecting a fully qualified target id.
                ))
            scene = Scene(
                setting_text=scene_data["setting_text"],
                explanation_text=scene_data["explanation_text"],
                options=options
            )
            coords = tuple(scene_data.get("coords", [0, 0]))
            self.graph.add_node(scene_id, scene=scene, coords=coords, objects={})

        # Add directed edges from each scene to its option targets.
        for node in self.graph.nodes:
            scene = self.graph.nodes[node]["scene"]
            for option in scene.options:
                target_id = option.target_node
                if target_id not in self.graph:
                    raise ValueError(f"Target scene id '{target_id}' not found for option '{option.description}'.")
                self.graph.add_edge(node, target_id, description=option.description)

        # Place objects in their starting scenes.
        for obj_data in data.get("objects", []):
            starting_scene = obj_data["starting_scene"]
            if starting_scene not in self.graph:
                raise ValueError(f"Starting scene '{starting_scene}' for object '{obj_data['object_id']}' not found.")
            obj = GameObject(
                object_id=obj_data["object_id"],
                description=obj_data["description"],
                current_node=starting_scene
            )
            self.objects[obj.object_id] = obj
            self.graph.nodes[starting_scene]["objects"][obj.object_id] = obj

    def get_node(self, node_id):
        return self.graph.nodes.get(node_id)

    def get_node_id_by_alias(self, alias):
        # In this namespaced system, the alias is the fully qualified id.
        return alias if alias in self.graph else None

    def move_object(self, object_id, target_node_id):
        obj = self.objects.get(object_id)
        if not obj:
            return
        current_node_id = obj.current_node
        if object_id in self.graph.nodes[current_node_id]["objects"]:
            del self.graph.nodes[current_node_id]["objects"][object_id]
        obj.current_node = target_node_id
        self.graph.nodes[target_node_id]["objects"][object_id] = obj