from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random

revealed_cards = []
score = 0
balls = 0
wickets = 0
full =[0,1,2,3,4,6,"NoBall","Wicket","Wide"]
weights =[0.2,0.15,0.15,0.15,0.1,0.1,0.05,0.05,0.05]
overs=1

def create_number_image(number):
    card_image = Image.open("image.png")
    bg_color = (random.randint(00, 255), random.randint(0, 255), random.randint(00, 255))
    image = Image.new("RGB", card_image.size, bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 60)
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (card_image.width - text_width) // 2
    y = (card_image.height - text_height) // 2
    draw.text((x, y), text, fill="black", font=font)
    return image


def on_card_click(card_index):
    global score, balls, wickets
    card_number = f[card_index]
    image = create_number_image(card_number)
    photo = ImageTk.PhotoImage(image)
    labels[card_index].configure(image=photo)
    labels[card_index].image = photo
    if card_number not in revealed_cards:
        message_label.config(text="Shuffle the cards")
        revealed_cards.append(card_number)
        record(card_number)
        balls += 1
        score_label["text"] = f"Score: {score}"
        balls_label["text"] = f"Balls: {balls}"
        wickets_label["text"] = f"Wickets: {wickets}"
    print(score)
    for label in labels:
        label.unbind("<Button-1>")
    shuffle_button.config(state=NORMAL)

def reset_game():
    global score, balls, wickets, revealed_cards
    score = 0
    balls = 0
    wickets = 0
    revealed_cards = []
    score_label["text"] = f"Score: {score}"
    balls_label["text"] = f"Balls: {balls}"
    wickets_label["text"] = f"Wickets: {wickets}"
    for label in labels:
        photo=PhotoImage(file="image.png")
        label.configure(image=photo)
    for i,label in enumerate(labels):
        label.bind("<Button-1>", lambda e,i=i: on_card_click(i))
        label.image = photo

def shuffle_cards():
    global f, balls, score, wickets,revealed_cards
    revealed_cards=[]

    f=gen(full, weights,5)
    print(f)
    for i in range(5):
        photo=PhotoImage(file="image.png")
        labels[i].configure(image=photo)
        labels[i].image = photo
    for i,label in enumerate(labels):
        if balls ==overs*6:
            end_game()
        else:
            label.bind("<Button-1>", lambda e,i=i: on_card_click(i))
    

def gen(numbers, weights, length):
    weighted_numbers = list(zip(numbers, weights))
    random.shuffle(weighted_numbers)
    random_list = [num for num, _ in weighted_numbers[:length]]
    return random_list


def record(s):
    global score, wickets, balls
    if isinstance(s, int):
        score += s
    elif s == "NoBall":
        score += 1
        balls += -1
    elif s == "Wide":
        score += 1
        balls += -1
    elif s == "Wicket":
        wickets += 1

def end_game():
    for label in labels:
        label.unbind("<Button-1>")
    message_label.config(text="Game Over")
    print("Game Over")

def start():
    global f, balls, score, wickets,revealed_cards , labels ,message_label ,wickets_label ,score_label , balls_label ,shuffle_button ,reset_button
    root = Tk()
    root.title("Cricket Game")
    root.configure(bg="black")
    message_label = Label(root,text="Play the Game", font=("Helvetica", 16), bg="lightblue")
    message_label.pack()
    score_label = Label(root,text=f" Score:  {score}", font=("Helvetica", 16),bg="black",fg="white")
    score_label.pack()
    balls_label = Label(root,text=f" Balls:  {balls}", font=("Helvetica", 16), bg="black",fg="white")
    balls_label.pack()
    wickets_label = Label(root,text=f"Wickets: {wickets}", font=("Helvetica", 16), bg="black",fg="white")
    wickets_label.pack()
    f = random.choices(full, weights, k=5)
    labels = []
    photos=[]



    for i in range(5):
        photo = PhotoImage(file="image.png")
        label = Label(root,image=photo)
        label.pack(side=LEFT)
        label.bind("<Button-1>", lambda e,i=i: on_card_click(i))
        labels.append(label)
        photos.append(photo)



    shuffle_button=Button(root,text="Shuffle ",command=shuffle_cards, font=("Helvetica", 16), bg="white", fg="black", activebackground="green", activeforeground="white")
    shuffle_button.pack()
    shuffle_button.config(state=DISABLED)

    reset_button=Button(root,text=" Reset ",command=reset_game, font=("Helvetica", 16), bg="white", fg="black", activebackground="green", activeforeground="white")
    reset_button.pack()
    reset_game
    root.mainloop()
