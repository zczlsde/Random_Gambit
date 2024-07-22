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
    p1 = g.add_player("Alice")
    p2 = g.add_player("Bob")

    # Helper function to add random moves and outcomes
    def add_random_moves(node, depth):
        if depth == max_depth:
            # Base case: add random outcomes
            outcome = g.add_outcome([random.randint(-10, 10), random.randint(-10, 10)])
            g.set_outcome(node, outcome)
            return

        # Randomly decide the type of event
        if depth == (max_depth-1):
            event_type = random.randint(0, 1)
        else:
            event_type = random.randint(0, 2)

        if event_type == 0:  # P1 move
            g.append_move(node, p1, [f"P1 choice {i}" for i in range(random.randint(2, 3))])
        elif event_type == 1:  # P2 move
            g.append_move(node, p2, [f"P2 choice {i}" for i in range(random.randint(2, 3))])
        else:  # Chance move
            num_choices = random.randint(2, 3)
            probabilities = generate_random_probabilities(num_choices)
            g.append_move(node, g.players.chance, [f"Chance {i}" for i in range(num_choices)])
            # print(probabilities)

            g.set_chance_probs(node.infoset, probabilities)
            
            # for i, prob in enumerate(probabilities):
            #     move.probabilities[i] = prob

        # Recursively add moves to the children
        for child in node.children:
            add_random_moves(child, depth + 1)

    # Start the recursive move addition
    add_random_moves(g.root, 0)

    # Write the game to an EFG file
    efg = g.write(format='native')
    return efg, g

# Example usage
total_games = 0
while total_games<3000:
    print("Generating: ", total_games)
    max_depth = random.randint(2, 4)
    efg_content, game = generate_random_efg(max_depth)
    print(game.is_perfect_recall)
    # Save the EFG content to a file
    if game.is_perfect_recall:
        
        name = "perfect_info_game/random_game_" + str(total_games) + ".efg"
        with open(name, "w") as file:
            file.write(efg_content)
        
        total_games += 1

        print("Random EFG file generated with max depth:", max_depth)