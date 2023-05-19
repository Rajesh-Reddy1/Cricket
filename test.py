from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random

revealed_cards = []
score = 0
balls = 0
wickets = 0
full = [0, 1, 2, 3, 4, 6, "NoBall", "Wicket", "Wide"]
weights = [0.2, 0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
overs = 2
players = ["Player 1", "Player 2"]
game_scores = {player: 0 for player in players}


class CricketGame:
    def __init__(self):
        self.revealed_cards = []
        self.score = 0
        self.balls = 0
        self.wickets = 0
        self.full = full
        self.weights = weights
        self.overs = overs
        self.players = players
        self.game_scores = game_scores

        self.card_image = Image.open("image.png")
        self.font = ImageFont.truetype("arial.ttf", 60)

        self.root = Tk()
        self.root.title("Cricket Game")
        self.root.configure(bg="black")

        self.message_label = Label(self.root, text="Play the Game", font=("Helvetica", 16), bg="lightblue")
        self.message_label.pack()
        self.score_label = Label(self.root, text=f" Score:  {self.score}", font=("Helvetica", 16), bg="black",
                                fg="white")
        self.score_label.pack()
        self.balls_label = Label(self.root, text=f" Balls:  {self.balls}", font=("Helvetica", 16), bg="black",
                            fg="white")
        self.balls_label.pack()
        self.wickets_label = Label(self.root, text=f"Wickets: {self.wickets}", font=("Helvetica", 16), bg="black",
                                fg="white")
        self.wickets_label.pack()

        self.labels = []
        self.photos = []
        for i in range(5):
            photo = ImageTk.PhotoImage(self.card_image)
            label = Label(self.root, image=photo)
            label.pack(side="left")
            label.bind("<Button-1>", lambda e, i=i: self.on_card_click(i))
            self.labels.append(label)
            self.photos.append(photo)

        self.shuffle_button = Button(self.root, text="Shuffle", command=self.shuffle_cards, font=("Helvetica", 16),
                                    bg="white", fg="black", activebackground="green", activeforeground="white")
        self.shuffle_button.pack()
        self.shuffle_button.config(state="disabled")

        self.reset_button = Button(self.root, text="Reset", command=self.reset_game, font=("Helvetica", 16),
                                bg="white", fg="black", activebackground="green", activeforeground="white")
        self.reset_button.pack()

    def create_number_image(self, number):
        bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image = Image.new("RGBA", self.card_image.size, bg_color)
        draw = ImageDraw.Draw(image)
        text = str(number)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.card_image.width - text_width) // 2
        y = (self.card_image.height - text_height) // 2
        draw.text((x, y), text, fill="black", font=self.font)
        return image

    def on_card_click(self, card_index):
        card_number = self.full[card_index]
        image = self.create_number_image(card_number)
        photo = ImageTk.PhotoImage(image)
        self.labels[card_index].configure(image=photo)
        self.labels[card_index].image = photo
        if card_number not in self.revealed_cards:
            self.message_label.config(text="Shuffle the cards")
            self.revealed_cards.append(card_number)
            self.record(card_number)
            self.balls += 1
            self.score_label["text"] = f"Score: {self.score}"
            self.balls_label["text"] = f"Balls: {self.balls}"
            self.wickets_label["text"] = f"Wickets: {self.wickets}"
        for label in self.labels:
            label.unbind("<Button-1>")
        self.shuffle_button.config(state="normal")

    def reset_game(self):
        self.score = 0
        self.balls = 0
        self.wickets = 0
        self.revealed_cards = []
        self.score_label["text"] = f"Score: {self.score}"
        self.balls_label["text"] = f"Balls: {self.balls}"
        self.wickets_label["text"] = f"Wickets: {self.wickets}"
        for label, photo in zip(self.labels, self.photos):
            label.configure(image=photo)
        for i, label in enumerate(self.labels):
            label.bind("<Button-1>", lambda e, i=i: self.on_card_click(i))
            label.image = self.photos[i]

    def shuffle_cards(self):
        self.revealed_cards = []
        self.full = self.gen(self.full, self.weights, 5)
        print(self.full)
        for label, photo in zip(self.labels, self.photos):
            label.configure(image=photo)
            label.image = photo
        for i, label in enumerate(self.labels):
            if self.balls == self.overs * 6:
                self.end_game()
            else:
                label.bind("<Button-1>", lambda e, i=i: self.on_card_click(i))

    @staticmethod
    def gen(numbers, weights, length):
        weighted_numbers = list(zip(numbers, weights))
        random.shuffle(weighted_numbers)
        random_list = [num for num, _ in weighted_numbers[:length]]
        return random_list

    def record(self, s):
        player = self.players[self.balls // 6]
        if isinstance(s, int):
            self.score += s
            self.game_scores[player] += s
        else:
            if s == "NoBall" or s == "Wide":
                self.score += 1
                self.game_scores[player] += 1
                self.balls -= 1
            elif s == "Wicket":
                self.wickets += 1
                self.game_scores[player] -= 5

    def end_game(self):
        for label in self.labels:
            label.unbind("<Button-1>")
        self.message_label.config(text="Game Over")
        print("Game Over")
        max_score = max(self.game_scores.values())
        winners = [player for player, score in self.game_scores.items() if score == max_score]
        if len(winners) == 1:
            print(f"The winner is {winners[0]}!")
        else:
            print("It's a tie! The winners are:")
            for winner in winners:
                print(winner)
        print("Final scores:")
        for player, score in self.game_scores.items():
            print(f"{player}: {score}")

    def start(self):
        for i, label in enumerate(self.labels):
            label.bind("<Button-1>", lambda e, i=i: self.on_card_click(i))
        self.root.mainloop()


if __name__ == "__main__":
    game = CricketGame()
    game.start()
