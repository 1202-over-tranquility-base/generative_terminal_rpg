from models import CharacterStats
from node_manager import NodeManager

def main():
    # Initialize the player's stats and the world (graph) of nodes.
    player_stats = CharacterStats(health=5)
    node_manager = NodeManager()
    current_node_id = "cabin_interior"

    while True:
        # Retrieve current node's attributes
        node_data = node_manager.get_node(current_node_id)
        if node_data is None:
            print(f"Error: Node '{current_node_id}' does not exist.")
            break

        scene = node_data["scene"]
        coords = node_data["coords"]
        objects = node_data["objects"]

        # Display location, player health, and narrative text
        print("\n" + "=" * 50)
        print(f"Location: {current_node_id}  |  Coordinates: {coords}")
        print(f"Health: {player_stats.health}\n")
        print(scene.setting_text)
        print(scene.explanation_text)

        # List any objects present in the node
        if objects:
            print("\nYou notice the following objects:")
            for obj in objects.values():
                print(f" - {obj.description}")

        # List available options
        print("\nAvailable actions:")
        for idx, option in enumerate(scene.options):
            print(f" {idx + 1}. {option.description}")

        # Get player's choice (or quit)
        choice = input("\nChoose an option (or type 'q' to quit): ").strip()
        if choice.lower() == "q":
            print("Exiting game. Goodbye!")
            break

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number corresponding to an option.")
            continue

        if not (1 <= choice <= len(scene.options)):
            print("Choice out of range. Try again.")
            continue

        selected_option = scene.options[choice - 1]

        # Apply any health modification from the option.
        player_stats.health += selected_option.health_mod
        if player_stats.health <= 0:
            print("Your health has reached 0. Game over!")
            break

        # Process special interactions: for instance, using the boat.
        if "boat" in selected_option.description.lower():
            if "boat" in objects:
                node_manager.move_object("boat", selected_option.target_node)
                print("You use the boat to cross the river. The boat is now on the other side.")
            else:
                print("The boat is not here!")
                continue

        # Transition to the target node.
        current_node_id = selected_option.target_node

if __name__ == "__main__":
    main()