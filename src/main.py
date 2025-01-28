from models import Scene, Option, CharacterStats
from managers import LLMEngine, InteractWithPlayer

class Game:
    def __init__(self):
        self.story_log = []
        self.character_stats = CharacterStats()
        self.llm_engine = LLMEngine()
        self.player_interaction = InteractWithPlayer()
        self.current_scene = None

    def build_scene_from_json(self, data):
        options = []
        for opt in data["options"]:
            option = Option(
                description=opt["description"],
                inventory_mod=opt["inventory_modification"],
                health_mod=opt["health_modification"]
            )
            options.append(option)
        return Scene(data["setting_text"], data["explanation_text"], options)

    def run(self):
        self.story_log.append("You wake up in a strange place.")
        self.load_next_scene("Dark fantasy in a forest clearing", "")

        while True:
            self.display_scene()
            if self.character_stats.health <= 0 or not self.current_scene.options:
                print("Your journey ends here.")
                break
            chosen_option_index = self.player_interaction.receive_option_selection(len(self.current_scene.options))
            chosen_option = self.current_scene.options[chosen_option_index - 1]
            self.apply_option_effects(chosen_option)
            self.story_log.append(f"Player chose: {chosen_option.description}")
            if "go to sleep" in chosen_option.description.lower():
                print("You drift off, ending your adventure.")
                break
            self.load_next_scene("Dark fantasy continuing the story", chosen_option.description)

    def display_scene(self):
        self.player_interaction.show_text(self.current_scene.setting_text)
        self.player_interaction.show_text(self.current_scene.explanation_text)
        self.current_scene.show_options()

    def apply_option_effects(self, option):
        self.character_stats.health += option.health_mod

    def load_next_scene(self, broad_context, last_choice):
        data = self.llm_engine.generate_scene(broad_context, " ".join(self.story_log), last_choice)
        self.current_scene = self.build_scene_from_json(data)

if __name__ == "__main__":
    game = Game()
    game.run()
