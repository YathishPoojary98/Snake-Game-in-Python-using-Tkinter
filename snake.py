import tkinter as tk
import random


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.score = 0

        # Create a frame for the top bar
        self.top_frame = tk.Frame(master, bg="gray", height=30)
        self.top_frame.pack(fill="x")

        # Score label (centered)
        self.score_label = tk.Label(self.top_frame, text=f"Score: {self.score}", bg="gray", font=("Arial", 12), fg="white")
        self.score_label.pack(side="left", padx=(10, 0))

        # Pause button (top-right)
        self.pause_button = tk.Button(self.top_frame, text="Pause", command=self.pause_game, font=("Arial", 10))
        self.pause_button.pack(side="right", padx=(0, 10))

        # Create canvas for the game
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.snake = [(280, 200), (300, 200), (320, 200)]
        self.food = self.create_food()
        self.direction = "Left"
        self.running = True
        self.paused = False

        self.master.bind("<KeyPress>", self.change_direction)

        self.update_game()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in self.snake:
                return x, y

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"] and not self.paused:
            self.direction = event.keysym

    def pause_game(self):
        self.paused = True
        self.display_pause_message()

    def resume_game(self):
        """ Resumes the game and removes Pause pop-up buttons """
        self.paused = False
        self.canvas.delete("pause_message")

        # Remove the buttons after resuming
        self.resume_button.destroy()
        self.exit_button.destroy()

        self.update_game()

    def exit_game(self):
        """ Exits the game and removes buttons if they exist """
        try:
            self.resume_button.destroy()
            self.exit_button.destroy()
        except AttributeError:
            pass  # Handles case where buttons do not exist
        self.master.destroy()

    def update_game(self):
        if self.running and not self.paused:
            self.move_snake()
            self.check_collisions()
            self.draw()
            self.update_score()
            self.master.after(100, self.update_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= self.cell_size
        elif self.direction == "Right":
            head_x += self.cell_size
        elif self.direction == "Up":
            head_y -= self.cell_size
        elif self.direction == "Down":
            head_y += self.cell_size
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 1

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or self.snake[0] in self.snake[1:]:
            self.running = False
            self.display_game_over_message()

    def draw(self):
        self.canvas.delete("snake")
        self.canvas.delete("food")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="green", tags="snake")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + self.cell_size, self.food[1] + self.cell_size, fill="red", tags="food")

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def display_pause_message(self):
        """ Displays pause message with Resume & Exit buttons """
        self.canvas.delete("pause_message")
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            fill="yellow",
            font=("Arial", 20),
            tags="pause_message",
        )
        self.resume_button = tk.Button(self.master, text="Resume", command=self.resume_game, font=("Arial", 12))
        self.resume_button.place(x=self.width // 2 - 70, y=self.height // 2 + 30)
        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_game, font=("Arial", 12))
        self.exit_button.place(x=self.width // 2 + 20, y=self.height // 2 + 30)

    def display_game_over_message(self):
        """ Displays 'Game Over' message and hides pause button """
        self.pause_button.pack_forget()  # Hide pause button

        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            fill="red",
            font=("Arial", 20),
            tags="game_over_message",
        )
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, font=("Arial", 12))
        self.new_game_button.place(x=self.width // 2 - 90, y=self.height // 2 + 30)
        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_game, font=("Arial", 12))
        self.exit_button.place(x=self.width // 2 + 20, y=self.height // 2 + 30)

    def new_game(self):
        """ Resets the game and brings back pause button """
        self.score = 0
        self.snake = [(280, 200), (300, 200), (320, 200)]
        self.food = self.create_food()
        self.direction = "Left"
        self.running = True
        self.paused = False
        self.canvas.delete("game_over_message")

        # Remove game-over buttons
        self.new_game_button.destroy()
        self.exit_button.destroy()

        # Restore pause button
        self.pause_button.pack(side="right", padx=(0, 10))

        self.update_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
