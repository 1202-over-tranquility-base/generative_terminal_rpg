import json
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from submodules.query_llm.src.query_llm import LLMRequest, call_openai_llm

class LLMEngine:
    def __init__(self, model_name="gpt-4o"):
        self.model_name = model_name

    def generate_path_scene(self, path_context, story_so_far, path_scene_count, target_node_desc):
        prompt = (
            f"You are generating a scene in a branching RPG as the character travels from one area of interest to another, which will happen over the course of a number of scenes.\n"
            f"Your job is to make it feel like the character is naturally travelling between the origin and target, and should therefore be a bit on the dull side.\n"
            f"Consider the following overview of the context and story so far:\n"
            f"Node context: {path_context}\n"
            f"Story so far: {story_so_far}\n"
            f"There have been {path_scene_count} scenes generated on this path so far. The goal for the character to arrive at the target within a total of roughly 2-3 scenes.\n"
            f"When you feel like it's a good time, have the character discover the Node and edit the transition_flag accordingly.\n"
            f"Target node description: {target_node_desc}\n"
            f"Provide a scene in JSON with:\n"
            f"- setting_text\n"
            f"- explanation_text\n"
            f"- options: list of objects, each with:\n"
            f"  - description: string\n"
            f"  - inventory_modification: list of strings\n"
            f"  - health_modification: integer (use negative numbers for reductions, positive without a plus sign)\n"
            f"  - transition_flag: string ('continue_path' or 'path-node_transition')\n"  # Added instruction for transition_flag
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
            f"You are generating a scene in a branching RPG, in the middle of an ongoing situation.\n"
            f"Consider the following overview of the context and story so far:\n"
            f"Node context: {node_context}\n"
            f"Story so far: {story_so_far}\n"
            f"You can have the player meander through this situation, and vaguely hint at a number of possible discoveries:\n"
            f"Possible discoveries: {possible_discoveries}\n"
            f"There have been {node_scene_count} scenes generated in this Node so far. The goal for the character to arrive at the target within a total of roughly 5-8 scenes.\n"
            f"When you feel like it's a good time, have the character exit the situation and edit the transition_flag accordingly.\n"
            f"Return a scene in JSON with:\n"
            f"- setting_text\n"
            f"- explanation_text (hint at the possible discoveries)\n"
            f"- options: list of objects, each with:\n"
            f"  - description: string\n"
            f"  - inventory_modification: list of strings\n"
            f"  - health_modification: integer (use negative numbers for reductions, positive without a plus sign)\n"
            f"  - transition_flag: string ('continue_node' or 'path-node_transition')\n"  # Added instruction for transition_flag
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