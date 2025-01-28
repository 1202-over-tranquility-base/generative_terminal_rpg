import json
# If you have an LLM library (e.g., openai), import it here

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
        )
        # Placeholder logic. Replace with actual LLM API call
        # response = openai.Completion.create(...)  # etc.
        # For now, pretend we got a JSON string back:
        fake_json_response = """
        {
            "setting_text": "You step into a dimly lit hut.",
            "explanation_text": "It smells musty. You notice a simple table with a few items.",
            "options": [
                {
                    "description": "Look around the hut.",
                    "inventory_modification": [],
                    "health_modification": 0
                },
                {
                    "description": "Leave the hut quietly.",
                    "inventory_modification": [],
                    "health_modification": 0
                }
            ]
        }
        """
        return json.loads(fake_json_response)

class InteractWithPlayer:
    def show_text(self, text):
        print(text)

    def receive_option_selection(self, num_options):
        choice = input("Choose an option: ")
        while not choice.isdigit() or not (1 <= int(choice) <= num_options):
            choice = input("Please enter a valid option number: ")
        return int(choice)
