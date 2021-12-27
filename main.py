from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# -------------------------Pandas csv reading------------------------
try:
    words_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_data = pandas.read_csv("data/english_words.csv")
finally:
    to_learn = words_data.to_dict(orient="records")


# ---------------------------Card selection--------------------------
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_img, image=front_img)
    canvas.itemconfig(language_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=current_card["English"], fill="black")

    flip_timer = window.after(5000, flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(canvas_img, image=back_img)
    canvas.itemconfig(language_text, text="Spanish", fill="white")
    canvas.itemconfig(word_text, text=current_card["Spanish"], fill="white")


# -------------------------Saving know words--------------------------
def is_known():
    global current_card, to_learn
    to_learn.remove(current_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# --------------------------------GUI--------------------------------
# Window config
window = Tk()
window.config(bg=BACKGROUND_COLOR)
window.title("Flash Cards")
window.minsize(width=880, height=700)
window.maxsize(width=880, height=700)

flip_timer = window.after(5000, flip_card)

# Canvas config
canvas = Canvas(width=800, height=538, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 276)
canvas.grid(row=0, column=0, columnspan=2, padx=(50, 0), pady=10)

# Canvas text
language_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))

# Button config
x_img = PhotoImage(file="images/wrong.png")
start_button = Button(image=x_img, bg=BACKGROUND_COLOR, border=0, activebackground=BACKGROUND_COLOR, command=next_card)
start_button.grid(row=1, column=0)

v_img = PhotoImage(file="images/right.png")
start_button = Button(image=v_img, bg=BACKGROUND_COLOR, border=0, activebackground=BACKGROUND_COLOR, command=is_known)
start_button.grid(row=1, column=1)

next_card()

window.mainloop()
