import json
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from submodules.query_llm.src.query_llm import LLMRequest, call_openai_llm

class LLMEngine:
    def __init__(self, model_name="gpt-4o-mini"):
        self.model_name = model_name

    def generate_path_scene(self, path_context, story_so_far, path_scene_count, target_node_desc):
        prompt = (
            f"You are generating a relaxed transition scene in a branching RPG.\n"
            f"You are trying to gently lead the player to a more interesting node, which will happen over the course of a few scenes.\n"
            f"Very minor events will occur along the way. Your job is to make it feel like the character is naturally travelling between the origin and target.\n"
            f"Path context: {path_context}\n"
            f"Story so far: {story_so_far}\n"
            f"Number of path scenes so far: {path_scene_count} (aim for around 4-7 total, but this can go longer if the character is in the middle of something)\n"
            f"Target node description: {target_node_desc}\n"
            f"Provide a scene in JSON with:\n"
            f"- setting_text\n"
            f"- explanation_text\n"
            f"- options (list of objects with 'description', 'inventory_modification', 'health_modification').\n"
            f"Ensure the JSON is properly formatted without any trailing commas or invalid characters.\n"
            f"Return **only** JSON text; no extra text (such as code blocks)."
        )
        req = LLMRequest(input_text=prompt, log_input_file="/home/user/Desktop/path_input.md",
                         log_output_file="/home/user/Desktop/path_output.md", model=self.model_name)
        resp = call_openai_llm(req)
        return json.loads(resp)

    def generate_node_discoveries(self, node_description):
        prompt = (
            f"Given the node description:\n"
            f"{node_description}\n"
            f"Generate a short list (in JSON) of interesting discoveries.\n"
            f"Each item should be a concise string.\n"
            f"Ensure the JSON is properly formatted without any trailing commas or invalid characters.\n"
            f"Return **only** JSON text; no extra text (such as code blocks)."
        )
        req = LLMRequest(input_text=prompt, log_input_file="/home/user/Desktop/node_disc_input.md",
                         log_output_file="/home/user/Desktop/node_disc_output.md", model=self.model_name)
        resp = call_openai_llm(req)
        return json.loads(resp)

    def generate_node_scene(self, node_context, story_so_far, node_scene_count, possible_discoveries):
        prompt = (
            f"You are generating a more engaging scene in a branching RPG.\n"
            f"Node context: {node_context}\n"
            f"Story so far: {story_so_far}\n"
            f"Number of node scenes so far: {node_scene_count} (somewhere around 4-7 total)\n"
            f"Possible discoveries: {possible_discoveries}\n"
            f"Return a scene in JSON with:\n"
            f"- setting_text\n"
            f"- explanation_text (hint at the possible discoveries)\n"
            f"- options (objects with 'description', 'inventory_modification', 'health_modification').\n"
            f"Ensure the JSON is properly formatted without any trailing commas or invalid characters.\n"
            f"Return **only** JSON text; no extra text (such as code blocks)."
        )
        req = LLMRequest(input_text=prompt, log_input_file="/home/user/Desktop/node_scene_input.md",
                         log_output_file="/home/user/Desktop/node_scene_output.md", model=self.model_name)
        resp = call_openai_llm(req)
        return json.loads(resp)

class InteractWithPlayer:
    def show_text(self, text):
        print(text)

    def receive_option_selection(self, num_options):
        choice = input("Choose an option: ")
        while not choice.isdigit() or not (1 <= int(choice) <= num_options):
            choice = input("Please enter a valid option number: ")
        return int(choice)