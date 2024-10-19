import random
import tkinter as tk
from tkinter import messagebox

# Initialize the deck of cards (2-10, J, Q, K, A; suits: hearts, diamonds, spades, clubs)
suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
deck = [(str(rank) + ' of ' + suit) for rank in ranks for suit in suits]

# Shuffle the deck
random.shuffle(deck)

# Define additional patterns
def is_even(card):
    rank = card.split()[0]
    return rank.isdigit() and int(rank) % 2 == 0

def is_face_card(card):
    rank = card.split()[0]
    return rank in ['J', 'Q', 'K']

# Existing patterns
# Existing patterns (updated to handle the full set of cards correctly)
def is_prime(card):
    prime_ranks = [2, 3, 5, 7]
    rank = card.split()[0]
    if rank.isdigit() and int(rank) in prime_ranks:
        return True
    return False




def sum_to_9(cards):
    total = 0
    for card in cards:
        rank = card.split()[0]
        if rank.isdigit():
            total += int(rank)
        elif rank == 'A':  # Treat Ace as 1
            total += 1
    return total == 9

def ace_and_black_jack(cards):
    # Check if there is an Ace and a black Jack (spades or clubs)
    has_ace = any(card.split()[0] == 'A' for card in cards)
    has_black_jack = any(card.split()[0] == 'J' and card.split()[2] in ['spades', 'clubs'])
    return has_ace and has_black_jack


# Dealer patterns (including additional ones)
patterns = {
    "All prime numbers": lambda cards: all(is_prime(card) for card in cards),
    "Cards sum to 9": sum_to_9,
    "Ace and a black Jack": ace_and_black_jack,
    "All even numbers": lambda cards: all(is_even(card) for card in cards),
    "All face cards": lambda cards: all(is_face_card(card) for card in cards)
}

# Hints system
hints = {
    "All prime numbers": "Check if the numbers are prime!",
    "Cards sum to 9": "Maybe the numbers add up to something.",
    "Ace and a black Jack": "Look for an Ace and a black card.",
    "All even numbers": "Are all the numbers divisible by 2?",
    "All face cards": "Look for face cards: J, Q, K."
}

# Game history to store last 5 game results
game_history = []

# Function to add game result to history
def add_to_history(pattern, guesses, rounds):
    game_history.append({
        "pattern": pattern,
        "guesses": guesses,
        "rounds": rounds
    })
    if len(game_history) > 5:
        game_history.pop(0)

# Main GUI window
root = tk.Tk()
root.title("Art Dealer Game")
root.geometry("600x400")
root.configure(bg="#e0f7fa")  # Set background color

# Game state variables
picked_cards = []
round_count = 1
chosen_pattern_name, chosen_pattern_func = random.choice(list(patterns.items()))
hint_given = False
guessed_patterns = []

# Helper function to update feedback
def update_feedback(text):
    feedback_label.config(text=text)

# Helper function to reset the game state
def reset_game():
    global picked_cards, round_count, chosen_pattern_name, chosen_pattern_func, guessed_patterns
    picked_cards = []
    round_count = 1
    random.shuffle(deck)  # Reshuffle the deck
    chosen_pattern_name, chosen_pattern_func = random.choice(list(patterns.items()))  # Choose a new pattern
    guessed_patterns = []
    update_feedback("Game reset. Pick your cards.")
    picked_cards_label.config(text="")
    pick_button.config(state="normal")
    guess_button.config(state="disabled")

# Helper function to pick a card from the deck
def pick_card():
    if len(picked_cards) < 4:
        card = deck.pop()
        picked_cards.append(card)
        picked_cards_label.config(text=", ".join(picked_cards))
        if len(picked_cards) == 4:
            pick_button.config(state="disabled")
            guess_button.config(state="normal")
            check_cards()

# Function to check cards and dealer’s buying decision
# Function to check cards and dealer’s buying decision
# Function to check cards and dealer’s buying decision
def check_cards():
    # Check how many individual cards match the dealer's hidden pattern
    bought_cards = [card for card in picked_cards if chosen_pattern_func([card])]  # Check each card individually
    bought_cards_text = ", ".join(bought_cards) if bought_cards else "none"
    
    # Provide feedback on how many cards were bought
    update_feedback(f"The dealer bought {len(bought_cards)} out of 4 cards: {bought_cards_text}.")



# Add this function to create the celebration effect with balloons
def celebration_animation():
    # Create a new window for the celebration
    celebration_window = tk.Toplevel(root)
    celebration_window.geometry("400x400")
    celebration_window.title("Congratulations!")

    # Create a canvas to draw the balloons on
    canvas = tk.Canvas(celebration_window, bg="skyblue", width=400, height=400)
    canvas.pack()

    # Balloon colors and starting positions
    balloons = [
        {"color": "red", "x": 50, "y": 400},
        {"color": "green", "x": 150, "y": 400},
        {"color": "blue", "x": 250, "y": 400},
        {"color": "yellow", "x": 350, "y": 400}
    ]

    # Create balloon shapes on the canvas
    balloon_objects = []
    for balloon in balloons:
        balloon_obj = canvas.create_oval(
            balloon["x"], balloon["y"], balloon["x"] + 50, balloon["y"] + 70,
            fill=balloon["color"], outline=balloon["color"]
        )
        balloon_objects.append(balloon_obj)

    # Animate the balloons moving upwards
    def move_balloons():
        for i, balloon in enumerate(balloons):
            # Move each balloon upwards
            canvas.move(balloon_objects[i], 0, -5)
            balloon["y"] -= 5

        # Repeat the animation until the balloons go off-screen
        if all(balloon["y"] < -70 for balloon in balloons):
            celebration_window.destroy()  # Close window after the celebration ends
        else:
            celebration_window.after(50, move_balloons)  # Continue moving balloons

    # Start the balloon movement
    move_balloons()

#### Add the celebration function to be called when the student wins:
def guess_pattern():
    global round_count
    pattern_choice = pattern_var.get()
    guessed_patterns.append(pattern_choice)

    # Check if the player's guess matches the dealer's hidden pattern
    if pattern_choice == chosen_pattern_name:
        add_to_history(chosen_pattern_name, guessed_patterns, round_count)
        messagebox.showinfo("You Win!", f"Correct! The dealer's pattern was {chosen_pattern_name}.")
        celebration_animation()  # Show celebration animation when the student wins
        reset_game()  # Reset game after correct guess
    else:
        round_count += 1
        if round_count > 3:
            # End game after 3 wrong guesses
            messagebox.showinfo("Game Over", f"Game Over! The dealer's pattern was {chosen_pattern_name}.")
            reset_game()
        else:
            update_feedback(f"Wrong guess. Try again! This is round {round_count}.")

# The rest of the game code remains the same.



# Function to show hints
def show_hint():
    hint = hints[chosen_pattern_name]
    messagebox.showinfo("Hint", hint)

# Function to show game history
def show_history():
    if not game_history:
        messagebox.showinfo("History", "No games played yet!")
        return
    history_message = "\n".join([f"Game {i+1}: Dealer Pattern - {game['pattern']}, Rounds - {game['rounds']}" for i, game in enumerate(game_history)])
    messagebox.showinfo("Game History", history_message)

# Main menu screen
def main_menu():
    menu_frame = tk.Frame(root, bg="#e0f7fa")
    menu_frame.pack(fill="both", expand=True)

    title_label = tk.Label(menu_frame, text="Art Dealer Game", font=("Arial", 24), bg="#e0f7fa")
    title_label.pack(pady=20)

    play_button = tk.Button(menu_frame, text="Play Game", font=("Arial", 16), command=lambda: start_game(menu_frame), bg="#00796b", fg="white", width=15, height=2)
    play_button.pack(pady=10)

    history_button = tk.Button(menu_frame, text="History", font=("Arial", 16), command=show_history, bg="#00796b", fg="white", width=15, height=2)
    history_button.pack(pady=10)

    exit_button = tk.Button(menu_frame, text="Exit Game", font=("Arial", 16), command=root.quit, bg="#d32f2f", fg="white", width=15, height=2)
    exit_button.pack(pady=10)

# Function to start game
def start_game(menu_frame):
    menu_frame.destroy()
    
    # GUI for the actual game
    game_frame = tk.Frame(root, bg="#e0f7fa")
    game_frame.pack(fill="both", expand=True)

    title_label = tk.Label(game_frame, text="Pick 4 Cards", font=("Arial", 18), bg="#e0f7fa")
    title_label.pack(pady=10)

    global picked_cards_label, feedback_label, pattern_var, pick_button, guess_button

    picked_cards_label = tk.Label(game_frame, text="", font=("Arial", 14), bg="#e0f7fa")
    picked_cards_label.pack(pady=10)

    feedback_label = tk.Label(game_frame, text="Pick 4 cards to begin.", font=("Arial", 12), bg="#e0f7fa")
    feedback_label.pack(pady=10)

    pick_button = tk.Button(game_frame, text="Pick a Card", font=("Arial", 14), command=pick_card, bg="#00796b", fg="white")
    pick_button.pack(pady=10)

    pattern_var = tk.StringVar(game_frame)
    pattern_var.set("Select a pattern")

    pattern_menu = tk.OptionMenu(game_frame, pattern_var, *patterns.keys())
    pattern_menu.config(font=("Arial", 14))
    pattern_menu.pack(pady=10)

    guess_button = tk.Button(game_frame, text="Guess Pattern", font=("Arial", 14), command=guess_pattern, bg="#00796b", fg="white")
    guess_button.pack(pady=10)
    guess_button.config(state="disabled")

    hint_button = tk.Button(game_frame, text="Get a Hint", font=("Arial", 14), command=show_hint, bg="#fbc02d", fg="white")
    hint_button.pack(pady=10)

    # Back to main menu button
    main_menu_button = tk.Button(game_frame, text="Go Back to Main Menu", font=("Arial", 14), command=lambda: [game_frame.destroy(), main_menu()], bg="#8e24aa", fg="white")
    main_menu_button.pack(pady=10)

    # Reset game button
    reset_button = tk.Button(game_frame, text="Reset Game", font=("Arial", 14), command=reset_game, bg="#d32f2f", fg="white")
    reset_button.pack(pady=10)

# Initialize the game with the main menu
main_menu()

# Run the Tkinter event loop
root.mainloop()
