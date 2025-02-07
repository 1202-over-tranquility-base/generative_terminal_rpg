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
    Some nodes are now flagged as hidden, and their names/descriptions
    are chosen based on a randomly selected terrain.
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
            # Choose terrain and adjust naming/description accordingly
            terrain_roll = random.random()
            if terrain_roll < 0.3:
                terrain = "forest"
                names = ["Enchanted Grove", "Ancient Oak", "Forest Clearing"]
                desc = "hidden among dense trees"
            elif terrain_roll < 0.6:
                terrain = "mountain"
                names = ["Rocky Outcrop", "Hidden Cave", "Mountain Pass"]
                desc = "nestled in rugged terrain"
            else:
                terrain = "plains"
                names = ["Abandoned Cabin", "Mystic Ruins", "Forgotten Shrine"]
                desc = "standing quietly on the open plains"
            name = random.choice(names)
            description = f"You discover a {name.lower()} {desc}."
            node_id = f"node.generated.{len(world.nodes)}"
            new_node = SceneNode(node_id=node_id, name=name, coords=new_coords, description=description)
            new_node.created_day = current_day
            new_node.persistent = True
            new_node.terrain = terrain
            # With a 30% chance, mark the node as hidden (it will not be listed until found)
            is_hidden = random.random() < 0.3
            new_node.hidden = is_hidden
            world.add_node(new_node)
            world.connect_nodes(current_node.node_id, new_node.node_id, connection_info={"path": "overgrown trail"}, bidirectional=True)
            if not is_hidden:
                print(f"\n[Procedural Generation] A new location '{new_node.name}' has been revealed at {new_coords}!")
            generated_count += 1

def generate_path_between_nodes(node_a, node_b, world, path_type="road"):
    # Create a few intermediate nodes between node_a and node_b
    steps = 3
    ax, ay = node_a.coords
    bx, by = node_b.coords
    dx = (bx - ax) / (steps + 1)
    dy = (by - ay) / (steps + 1)
    previous_node = node_a
    for i in range(1, steps + 1):
        new_x = round(ax + i * dx)
        new_y = round(ay + i * dy)
        new_coords = (new_x, new_y)
        # If a node already exists at these coordinates, link to it.
        existing = next((node for node in world.nodes.values() if node.coords == new_coords), None)
        if existing:
            if existing.node_id not in previous_node.neighbors:
                world.connect_nodes(previous_node.node_id, existing.node_id, connection_info={"path": path_type}, bidirectional=True)
            previous_node = existing
            continue
        node_id = f"node.secondary.{len(world.nodes)}"
        names = ["Road Outpost", "Small Village", "Watchtower", "Rest Stop"]
        name = random.choice(names)
        description = f"A {name.lower()} along the {path_type} connecting {node_a.name} and {node_b.name}."
        new_node = SceneNode(node_id=node_id, name=name, coords=new_coords, description=description)
        new_node.created_day = 0
        new_node.persistent = True
        world.add_node(new_node)
        world.connect_nodes(previous_node.node_id, new_node.node_id, connection_info={"path": path_type}, bidirectional=True)
        previous_node = new_node
    world.connect_nodes(previous_node.node_id, node_b.node_id, connection_info={"path": path_type}, bidirectional=True)

def create_macro_world():
    world = WorldMap()
    # Define a few regions with centers and boundaries.
    regions = [
        {"name": "Northern Realm", "center": (10, 10), "bounds": ((5, 5), (15, 15))},
        {"name": "Southern Lands", "center": (-10, -10), "bounds": ((-15, -15), (-5, -5))},
        {"name": "Eastern Expanse", "center": (20, -10), "bounds": ((15, -15), (25, -5))}
    ]
    major_nodes = []
    for region in regions:
        region_name = region["name"]
        (min_bound, max_bound) = region["bounds"]
        min_x, min_y = min_bound
        max_x, max_y = max_bound
        # Create two major nodes per region.
        for i in range(2):
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            node_id = f"node.major.{len(world.nodes)}"
            name = f"{region_name} City {i+1}"
            description = f"A bustling city in the {region_name.lower()}."
            node = SceneNode(node_id=node_id, name=name, coords=(x, y), description=description)
            node.created_day = 0
            node.persistent = True
            world.add_node(node)
            major_nodes.append(node)
    # Connect the two nodes in each region with a major road and scatter secondary nodes along the way.
    for i in range(0, len(major_nodes), 2):
        node_a = major_nodes[i]
        node_b = major_nodes[i+1]
        world.connect_nodes(node_a.node_id, node_b.node_id, connection_info={"path": "major road"}, bidirectional=True)
        generate_path_between_nodes(node_a, node_b, world, path_type="major road")
    # Connect regions by linking the first major node of each region.
    if len(major_nodes) >= 3:
        world.connect_nodes(major_nodes[0].node_id, major_nodes[2].node_id, connection_info={"path": "inter-region highway"}, bidirectional=True)
        generate_path_between_nodes(major_nodes[0], major_nodes[2], world, path_type="inter-region highway")
        world.connect_nodes(major_nodes[2].node_id, major_nodes[4].node_id, connection_info={"path": "inter-region highway"}, bidirectional=True)
        generate_path_between_nodes(major_nodes[2], major_nodes[4], world, path_type="inter-region highway")
    # Start at the first major node.
    starting_node = major_nodes[0]
    return world, starting_node

def search_for_hidden_nodes(current_node, world):
    """
    Look for any hidden nodes in the 8 adjacent coordinates.
    If found, reveal (set hidden=False and discovered=True) and announce them.
    """
    found = False
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            adjacent = (current_node.coords[0] + dx, current_node.coords[1] + dy)
            node = next((n for n in world.nodes.values() if n.coords == adjacent and n.hidden and not n.discovered), None)
            if node:
                node.hidden = False
                node.discovered = True
                print(f"\n[Search] You have discovered a hidden location: {node.name} at {node.coords}!")
                found = True
    if not found:
         print("\n[Search] You search the area but find nothing hidden.")

def update_factions(current_day, world):
    """
    Placeholder for faction or event updates.
    Currently, every 5 days a message is printed.
    """
    if current_day % 5 == 0 and current_day != 0:
        print("\n[Faction Update] Rumors spread that mysterious forces are shifting in the land...")

def main():
    world, starting_node = create_macro_world()
    player = Player(starting_node)
    while True:
        print("\n" + "=" * 40)
        print(f"Day {player.current_day}:")
        print(f"You are at: {player.current_node.name}")
        print(player.current_node.description)
        update_factions(player.current_day, world)
        # Only list neighbors that are either not hidden or have been discovered
        visible_neighbors = []
        for neighbor_id, info in player.current_node.neighbors.items():
            neighbor = world.get_node(neighbor_id)
            if neighbor.hidden and not neighbor.discovered:
                continue
            visible_neighbors.append((neighbor_id, info, neighbor))
        print("\nPaths available:")
        for idx, (neighbor_id, info, neighbor) in enumerate(visible_neighbors, 1):
            display_name = neighbor.name if neighbor.discovered else "???"
            print(f"{idx}. {display_name} via {info.get('path', 'an unknown path')}")
        print("m. Show Map")
        print("s. Search for hidden paths")
        print("0. Exit game")
        
        choice = input("\nChoose your action (number/m/s): ")
        if choice == "0":
            print("Thanks for playing!")
            break
        if choice.lower() == "m":
            print("\n--- World Map ---")
            world.display_map(player)
            continue
        if choice.lower() == "s":
            search_for_hidden_nodes(player.current_node, world)
            player.current_day += 1
            player.current_node.last_visited = player.current_day
            continue
        try:
            choice_index = int(choice) - 1
            if choice_index < 0 or choice_index >= len(visible_neighbors):
                print("Invalid selection. Try again.")
                continue
            selected_neighbor_id, _, next_node = visible_neighbors[choice_index]
            if random.random() < 0.3:
                print("\n[Random Event] " + random_event())
            player.move_to(next_node)
            generate_procedural_nodes(player.current_node, world, player.current_day)
            world.prune_old_nodes(player.current_day, decay_threshold=5)
        except ValueError:
            print("Please enter a valid number, 'm' for map, or 's' to search.")

if __name__ == "__main__":
    main()