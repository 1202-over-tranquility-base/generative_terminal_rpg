class CharacterStats:
    def __init__(self, health=5):
        self.health = health

class Option:
    def __init__(self, description, inventory_mod=(), health_mod=0):
        self.description = description
        self.inventory_mod = inventory_mod
        self.health_mod = health_mod

class Scene:
    def __init__(self, setting_text, explanation_text, options):
        self.setting_text = setting_text
        self.explanation_text = explanation_text
        self.options = options

    def show_options(self):
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option.description}")

class Path:
    def __init__(self, origin_node, target_node):
        self.origin_node = origin_node
        self.target_node = target_node
        self.scenes_completed = 0

class Node:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.scenes_completed = 0
        self.discoveries = []

class Act:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
        self.current_node_index = 0

    def has_more_nodes(self):
        return self.current_node_index < len(self.nodes)

    def get_current_node(self):
        if self.has_more_nodes():
            return self.nodes[self.current_node_index]
        return None

    def move_to_next_node(self):
        self.current_node_index += 1