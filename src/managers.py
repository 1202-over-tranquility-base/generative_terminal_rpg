import json
# If you have an LLM library (e.g., openai), import it here

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)
from submodules.query_llm.src.query_llm import LLMRequest, call_openai_llm

class LLMEngine:
    def __init__(self, model_name="some-llm-model"):
        self.model_name = model_name

    def generate_scene(self, broad_context, story_log, last_choice):
        prompt = (
            f"You are designing a scene in a branching RPG.\n"
            f"Context: {broad_context}\n"
            f"Story so far: {story_log}\n"
            f"The player just chose: {last_choice}\n"
            f"Provide the next scene in JSON with:\n"
            f"- setting_text\n"
            f"- explanation_text\n"
            f"- options (each option has 'description', 'inventory_modification', 'health_modification')\n"
            f"Return **only** JSON text; no extra text (such as code blocks)"
        )
        request = LLMRequest(
            input_text=prompt,
            log_input_file="/home/user/Desktop/input.md",
            log_output_file="/home/user/Desktop/output.md",
            model="gpt-4o-mini"
        )
        response = call_openai_llm(request)
        return json.loads(response)

class InteractWithPlayer:
    def show_text(self, text):
        print(text)

    def receive_option_selection(self, num_options):
        choice = input("Choose an option: ")
        while not choice.isdigit() or not (1 <= int(choice) <= num_options):
            choice = input("Please enter a valid option number: ")
        return int(choice)
