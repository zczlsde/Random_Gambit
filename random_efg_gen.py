import pygambit as gbt
import random
import numpy as np

def generate_random_probabilities(n):
    """Generate n random probabilities that sum to 1."""
    probabilities = np.random.randint(1,20,n)
    # print(probabilities)
    total = sum(probabilities)
    return [gbt.Rational(p,total) for p in probabilities]

def generate_random_efg(max_depth):
    # Initialize the game and players
    g = gbt.Game.new_tree()
    p1 = g.add_player("P1")
    p2 = g.add_player("P2")

    # Keep track of nodes for potential information sets
    p1_nodes_by_depth = [[] for _ in range(max_depth)]
    p2_nodes_by_depth = [[] for _ in range(max_depth)]

    # Helper function to add random moves and outcomes
    def add_random_moves(node, depth):
        if depth == max_depth:
            # Base case: add random outcomes
            outcome = g.add_outcome([random.randint(-10, 10), random.randint(-10, 10)])
            # print("======")
            g.set_outcome(node, outcome)
            return

        # Randomly decide the type of event
        if depth == (max_depth-1):
            event_type = random.randint(0, 1)
        else:
            event_type = random.randint(0, 2)

        if event_type == 0:  # P1 move
            # g.append_move(node, p1, [f"P1 choice {i}" for i in range(random.randint(2, 3))])
            g.append_move(node, p1, [f"P1 choice {i}" for i in range(2)])
            if depth<max_depth-1:
                for child in node.children:
                    
                    p1_nodes_by_depth[depth].append(child)

        elif event_type == 1:  # P2 move
            # g.append_move(node, p2, [f"P2 choice {i}" for i in range(random.randint(2, 3))])
            g.append_move(node, p2, [f"P2 choice {i}" for i in range(2)])
            if depth<max_depth-1:
                for child in node.children:
                    
                    p2_nodes_by_depth[depth].append(child)

        else:  # Chance move
            num_choices = random.randint(2, 3)
            probabilities = generate_random_probabilities(2)
            # g.append_move(node, g.players.chance, [f"Chance {i}" for i in range(num_choices)])
            g.append_move(node, g.players.chance, [f"Chance {i}" for i in range(2)])
            g.set_chance_probs(node.infoset, probabilities)
            

        # Recursively add moves to the children
        for child in node.children:
            add_random_moves(child, depth + 1)

    # Start the recursive move addition
    add_random_moves(g.root, 0)
    
    print(g.write(format='native'))
    def add_random_imperfect_information(nodes_by_depth):
        # print(nodes_by_depth)
        # print(len(nodes_by_depth))
        for depth_nodes in nodes_by_depth:
            if len(depth_nodes) < 2:
                continue
            for _ in range(len(depth_nodes) // 2):
                node1, node2 = random.sample(depth_nodes, 2)
                # print(node1)
                # print(node2.infoset)
                g.set_infoset(node1, node2.infoset)

    # Add imperfect information for both players
    add_random_imperfect_information(p1_nodes_by_depth)
    add_random_imperfect_information(p2_nodes_by_depth)

    # Write the game to an EFG file
    # print(g.is_perfect_recall)
    efg = g.write(format='native')
    # print("=========")
    # print(efg)
    
    return efg, g

# Example usage
total_games = 0
while total_games<1500:
    print("Generating: ", total_games)
    max_depth = random.randint(2, 4)
    efg_content, game = generate_random_efg(max_depth)
    print(game.is_perfect_recall)
    # Save the EFG content to a file
    fix = total_games + 1500
    if game.is_perfect_recall:
        name = "imperfect_info_game/random_game_" + str(fix) + ".efg"
        with open(name, "w") as file:
            file.write(efg_content)
        
        total_games += 1

        print("Random EFG file generated with max depth:", max_depth)