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

def generate_procedural_nodes(current_node, world, current_day):
    """
    Generate 1–2 notable nodes adjacent to the current node.
    These nodes are placed (if the location is empty) and flagged as persistent.
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    generated_count = 0
    for dx, dy in directions:
        if generated_count >= 2:
            break
        new_coords = (current_node.coords[0] + dx, current_node.coords[1] + dy)
        # Only create a node if there is no node at these coordinates.
        if any(node.coords == new_coords for node in world.nodes.values()):
            continue
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
            new_node.created_day = current_day
            new_node.persistent = True  # Mark notable nodes to persist.
            world.add_node(new_node)
            connection_info = {"path": "overgrown trail"}
            world.connect_nodes(current_node.node_id, new_node.node_id, connection_info, bidirectional=True)
            print(f"\n[Procedural Generation] A new location '{new_node.name}' has been revealed at {new_coords}!")
            generated_count += 1

def create_region():
    world = WorldMap()
    
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
    
    # Mark initial (notable) nodes as persistent.
    for node in [entrance, clearing, forest, riverbank, hilltop]:
        node.persistent = True
        world.add_node(node)
    
    world.connect_nodes("node.entrance", "node.clearing", connection_info={"path": "dirt road"})
    world.connect_nodes("node.clearing", "node.forest", connection_info={"path": "winding path"})
    world.connect_nodes("node.entrance", "node.riverbank", connection_info={"path": "forest trail"})
    world.connect_nodes("node.entrance", "node.hilltop", connection_info={"path": "steep slope"})
    
    return world, entrance

def main():
    world, starting_node = create_region()
    player = Player(starting_node)
    
    while True:
        print("\n" + "=" * 40)
        print(f"Day {player.current_day}:")
        print(f"You are at: {player.current_node.name}")
        print(player.current_node.description)
        print("\nPaths available:")
        
        # List neighbors. If the destination hasn't been discovered yet, hide its name.
        neighbors = list(player.current_node.neighbors.items())
        for idx, (neighbor_id, info) in enumerate(neighbors, 1):
            neighbor = world.get_node(neighbor_id)
            display_name = neighbor.name if neighbor.discovered else "???"
            print(f"{idx}. {display_name} via {info.get('path', 'an unknown path')}")
        print("m. Show Map")
        print("0. Exit game")
        
        choice = input("\nChoose your path (number/m): ")
        if choice == "0":
            print("Thanks for playing!")
            break
        if choice.lower() == "m":
            print("\n--- World Map ---")
            world.display_map(player)
            continue
        try:
            choice_index = int(choice) - 1
            if choice_index < 0 or choice_index >= len(neighbors):
                print("Invalid selection. Try again.")
                continue
            selected_neighbor_id, _ = neighbors[choice_index]
            next_node = world.get_node(selected_neighbor_id)
            
            if random.random() < 0.3:
                print("\n[Random Event] " + random_event())
            
            player.move_to(next_node)
            generate_procedural_nodes(player.current_node, world, player.current_day)
            # Remove any nodes that haven't been visited in over 5 in-game days.
            world.prune_old_nodes(player.current_day, decay_threshold=5)
        except ValueError:
            print("Please enter a valid number or 'm' for map.")
            
if __name__ == "__main__":
    main()