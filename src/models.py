class CharacterStats:
    def __init__(self, health=5):
        self.health = health

class Option:
    def __init__(self, description, target_node, health_mod=0, inventory_mod=None):
        self.description = description
        self.target_node = target_node
        self.health_mod = health_mod
        self.inventory_mod = inventory_mod if inventory_mod is not None else []

class Scene:
    def __init__(self, setting_text, explanation_text, options):
        self.setting_text = setting_text
        self.explanation_text = explanation_text
        self.options = options

class GameObject:
    def __init__(self, object_id, description, current_node):
        self.object_id = object_id
        self.description = description
        self.current_node = current_node