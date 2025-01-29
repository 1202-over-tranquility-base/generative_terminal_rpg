from managers import LLMEngine, InteractWithPlayer
from models import CharacterStats, Scene, Option, Act, Node, Path

class Game:
    def __init__(self):
        self.story_log = []
        self.character_stats = CharacterStats()
        self.llm_engine = LLMEngine()
        self.player_io = InteractWithPlayer()
        self.current_scene = None
        self.act = None

    def run(self):
        self.setup_act()
        self.story_log.append("You wake up in a strange place.")
        while self.act.has_more_nodes():
            node = self.act.get_current_node()
            if self.act.current_node_index == 0:
                self.play_path(None, node)
            else:
                prev_node = self.act.nodes[self.act.current_node_index - 1]
                self.play_path(prev_node, node)
            self.play_node(node)
            self.act.move_to_next_node()
        self.player_io.show_text("Your journey through the Act has ended.")

    def setup_act(self):
        nodes = [
            Node("Mysterious Hut", "A small hut in the forest rumored to hold secrets."),
            Node("Hermit Wizard", "An eccentric wizard who tests travelers' virtue."),
            Node("Ancient Ruins (Climax)", "A hidden ruin with magical artifacts.")
        ]
        self.act = Act("Forest Adventure", nodes)

    def play_path(self, origin_node, target_node):
        path = Path(origin_node, target_node)
        while True:
            if path.scenes_completed > 6:
                break
            origin_desc = origin_node.description if origin_node else "Starting Point"
            data = self.llm_engine.generate_path_scene(
                path_context=f"From {origin_desc}",
                story_so_far=" ".join(self.story_log),
                path_scene_count=path.scenes_completed,
                target_node_desc=target_node.description
            )
            scene = self.build_scene(data)
            if not scene.options:
                break
            self.display_scene(scene)
            choice_index = self.player_io.receive_option_selection(len(scene.options))
            chosen_option = scene.options[choice_index - 1]
            self.apply_option_effects(chosen_option)
            self.story_log.append(f"Player on path chose: {chosen_option.description}")
            path.scenes_completed += 1
            if "move on" in chosen_option.description.lower():
                break

    def play_node(self, node):
        node.discoveries = self.llm_engine.generate_node_discoveries(node.description)
        while True:
            if node.scenes_completed > 6:
                break
            data = self.llm_engine.generate_node_scene(
                node_context=node.description,
                story_so_far=" ".join(self.story_log),
                node_scene_count=node.scenes_completed,
                possible_discoveries=node.discoveries
            )
            scene = self.build_scene(data)
            if not scene.options:
                break
            self.display_scene(scene)
            choice_index = self.player_io.receive_option_selection(len(scene.options))
            chosen_option = scene.options[choice_index - 1]
            self.apply_option_effects(chosen_option)
            self.story_log.append(f"Player at node {node.name} chose: {chosen_option.description}")
            node.scenes_completed += 1
            if "leave" in chosen_option.description.lower():
                break

    def build_scene(self, data):
        options = []
        for opt in data.get("options", []):
            option = Option(
                description=opt["description"],
                inventory_mod=opt["inventory_modification"],
                health_mod=opt["health_modification"]
            )
            options.append(option)
        return Scene(data.get("setting_text", ""),
                     data.get("explanation_text", ""),
                     options)

    def display_scene(self, scene):
        self.player_io.show_text(f"Current health: {self.character_stats.health}")
        self.player_io.show_text(scene.setting_text)
        self.player_io.show_text(scene.explanation_text)
        scene.show_options()

    def apply_option_effects(self, option):
        self.character_stats.health += option.health_mod
        if self.character_stats.health <= 0:
            self.player_io.show_text("You have perished.")
            exit()

if __name__ == "__main__":
    game = Game()
    game.run()