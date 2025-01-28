class CharacterStats:
    def __init__(self, health=5):
        self.health = health

class Option:
    def __init__(self, description, inventory_mod=(), health_mod=0):
        self.description = description
        self.inventory_mod = inventory_mod
        self.health_mod = health_mod
        self.next_scene = None

class Scene:
    def __init__(self, setting_text, explanation_text, options):
        self.setting_text = setting_text
        self.explanation_text = explanation_text
        self.options = options

    def show_options(self):
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option.description}")
