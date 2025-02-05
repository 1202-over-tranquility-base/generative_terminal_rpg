import random
from core import SceneNode, WorldMap, Player

def random_event():
    events = [
        "A sudden gust of wind rustles the leaves.",
        "You hear a distant howl echoing through the trees.",
        "A bird swoops by, startling you for a moment.",
        "The ground trembles slightly beneath your feet."
    ]
    return random.choice(events)

def generate_procedural_nodes(current_node, world):
    """
    Procedurally generate 1–2 notable nodes adjacent to the current node.
    The nodes are placed in one of the four cardinal directions if that location is empty.
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    generated_count = 0
    for dx, dy in directions:
        if generated_count >= 2:
            break
        new_coords = (current_node.coords[0] + dx, current_node.coords[1] + dy)
        # Check if any node already occupies these coordinates.
        if any(node.coords == new_coords for node in world.nodes.values()):
            continue
        # With 50% chance, generate a new notable node.
        if random.random() < 0.5:
            notable_names = ["Abandoned Cabin", "Hidden Grove", "Mystic Ruins", "Forgotten Shrine"]
            name = random.choice(notable_names)
            description = f"You discover a {name.lower()} off the beaten path."
            node_id = f"node.generated.{len(world.nodes)}"
            new_node = SceneNode(
                node_id=node_id,
                name=name,
                coords=new_coords,
                description=description
            )
            world.add_node(new_node)
            connection_info = {"path": "overgrown trail"}
            world.connect_nodes(current_node.node_id, new_node.node_id, connection_info, bidirectional=True)
            print(f"\n[Procedural Generation] A new location '{new_node.name}' has been revealed at {new_coords}!")
            generated_count += 1

def create_region():
    world = WorldMap()
    
    # Create a small region of 5 nodes.
    entrance = SceneNode(
        node_id="node.entrance",
        name="Entrance",
        coords=(0, 0),
        description="You stand at the entrance of a mysterious realm."
    )
    clearing = SceneNode(
        node_id="node.clearing",
        name="Clearing",
        coords=(1, 0),
        description="A quiet clearing with soft grass and gentle sunlight."
    )
    forest = SceneNode(
        node_id="node.forest",
        name="Forest",
        coords=(1, 1),
        description="Dense trees and winding paths create an eerie ambiance."
    )
    riverbank = SceneNode(
        node_id="node.riverbank",
        name="Riverbank",
        coords=(0, 1),
        description="The sound of trickling water fills the air along the riverbank."
    )
    hilltop = SceneNode(
        node_id="node.hilltop",
        name="Hilltop",
        coords=(-1, 0),
        description="From this elevated spot, the landscape unfolds before you."
    )
    
    # Add nodes to the world.
    for node in [entrance, clearing, forest, riverbank, hilltop]:
        world.add_node(node)
    
    # Connect the nodes.
    world.connect_nodes("node.entrance", "node.clearing", connection_info={"path": "dirt road"})
    world.connect_nodes("node.clearing", "node.forest", connection_info={"path": "winding path"})
    world.connect_nodes("node.entrance", "node.riverbank", connection_info={"path": "forest trail"})
    world.connect_nodes("node.entrance", "node.hilltop", connection_info={"path": "steep slope"})
    
    return world, entrance

def main():
    world, starting_node = create_region()
    player = Player(starting_node)
    
    while True:
        # Display current location and description.
        print("\n" + "=" * 40)
        print(f"You are at: {player.current_node.name}")
        print(player.current_node.description)
        print("\nPaths available:")
        
        # List the available neighbors.
        neighbors = list(player.current_node.neighbors.items())
        for idx, (neighbor_id, info) in enumerate(neighbors, 1):
            neighbor = world.get_node(neighbor_id)
            print(f"{idx}. {neighbor.name} via {info.get('path', 'an unknown path')}")
        print("0. Exit game")
        
        choice = input("\nChoose your path (number): ")
        if choice == "0":
            print("Thanks for playing!")
            break
        try:
            choice_index = int(choice) - 1
            if choice_index < 0 or choice_index >= len(neighbors):
                print("Invalid selection. Try again.")
                continue
            selected_neighbor_id, _ = neighbors[choice_index]
            next_node = world.get_node(selected_neighbor_id)
            
            # Occasionally trigger a random event.
            if random.random() < 0.3:  # 30% chance
                print("\n[Random Event] " + random_event())
            
            player.move_to(next_node)
            # After moving, attempt to generate new nearby nodes.
            generate_procedural_nodes(player.current_node, world)
        except ValueError:
            print("Please enter a valid number.")
            
if __name__ == "__main__":
    main()