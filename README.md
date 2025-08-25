# Riddle_game
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Riddles, answers, and hints
riddles = [
    {"question": "What’s always hard to keep in your pants when you’re excited?", "answer": "phone", "hint": "It’s something you check often."},
    {"question": "What grows bigger the more you play with it?", "answer": "ego", "hint": "It’s inflated by compliments."},
    {"question": "What’s slippery when wet and hard to hold onto?", "answer": "soap", "hint": "It’s used in the shower."},
    {"question": "What’s long, gets hot, and you grip it tightly?", "answer": "candle", "hint": "It’s lit during a romantic evening."},
    {"question": "What’s something you blow to make it quick?", "answer": "fuse", "hint": "It’s part of an explosive."},
    {"question": "What’s firm, juicy, and best when squeezed?", "answer": "peach", "hint": "It’s a fruit you eat."},
    {"question": "What’s soft, gets wet, and you rub it in circles?", "answer": "towel", "hint": "It’s used after a shower."},
    {"question": "What’s stiff, stands up, and you adjust it in the morning?", "answer": "collar", "hint": "It’s part of a dress shirt."},
    {"question": "What’s something you stroke to make it purr?", "answer": "cat", "hint": "It’s a pet that loves attention."},
    {"question": "What’s round, bouncy, and fun to chase?", "answer": "ball", "hint": "It’s used in sports."},
    {"question": "What’s sticky, sweet, and drips when warm?", "answer": "honey", "hint": "It’s made by bees."},
    {"question": "What’s hard, gets pounded, and you do it on a table?", "answer": "nail", "hint": "It’s used in carpentry."},
    {"question": "What’s something you lick before you stick?", "answer": "stamp", "hint": "It’s used for mailing letters."},
    {"question": "What’s long, curved, and you peel it before use?", "answer": "banana", "hint": "It’s a fruit you eat."},
    {"question": "What’s tight, stretchy, and you slip into it?", "answer": "glove", "hint": "It protects your hands."},
    {"question": "What’s hot, steamy, and you do it in a bath?", "answer": "tea", "hint": "It’s a beverage you steep."},
    {"question": "What’s something you pump to make it quick?", "answer": "tire", "hint": "It’s part of a car."},
    {"question": "What’s smooth, gets wet, and you slide it in?", "answer": "card", "hint": "It’s used for payments."},
    {"question": "What’s something you whip to make it quick and creamy?", "answer": "cream", "hint": "It’s used in desserts."},
    {"question": "What’s hard to pull out once it’s in deep?", "answer": "cork", "hint": "It’s used to seal a bottle."}
]

class RiddleGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Riddle Zone")
        self.geometry("800x600")
        self.resizable(False, False)

        # Background Image
        self.bg_image = Image.open("pooltable.png").resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Overlay Frame
        self.frame = tk.Frame(self, bg="#000000")  # No transparency
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.username = ""
        self.age = 0
        self.score = 0
        self.riddle_index = 0

        self.build_start_screen()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def build_start_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Riddle Zone", font=("Helvetica", 20), fg="white", bg="#000000").pack(pady=10)
        tk.Label(self.frame, text="Must be 21 to play", font=("Helvetica", 14), fg="white", bg="#000000").pack(pady=5)

        tk.Label(self.frame, text="Enter Username:", fg="white", bg="#000000").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        tk.Label(self.frame, text="Enter Age:", fg="white", bg="#000000").pack()
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.pack()

        tk.Button(self.frame, text="Start Game", command=self.validate_start).pack(pady=10)

    def validate_start(self):
        name = self.name_entry.get().strip()
        age_text = self.age_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Username cannot be empty!")
            return
        try:
            age = int(age_text)
            if age < 21:
                messagebox.showwarning("Too Young", "Too Young to Play!")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a number!")
            return

        self.username = name
        self.age = age
        self.score = 0
        self.riddle_index = 0
        self.load_riddle()

    def load_riddle(self):
        self.clear_frame()
        if self.riddle_index >= len(riddles):
            self.show_final_score()
            return

        r = riddles[self.riddle_index]
        tk.Label(self.frame, text=f"Riddle {self.riddle_index + 1}:", font=("Helvetica", 16), fg="white", bg="#000000").pack(pady=5)
        tk.Label(self.frame, text=r["question"], wraplength=600, fg="white", bg="#000000").pack(pady=5)

        self.answer_entry = tk.Entry(self.frame)
        self.answer_entry.pack()

        self.feedback_label = tk.Label(self.frame, text="", fg="yellow", bg="#000000")
        self.feedback_label.pack(pady=5)

        tk.Button(self.frame, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = riddles[self.riddle_index]["answer"]
        hint = riddles[self.riddle_index]["hint"]

        if user_answer == correct_answer:
            self.score += 1
            self.riddle_index += 1
            self.load_riddle()
        else:
            self.feedback_label.config(text=f"Incorrect! Hint: {hint}")

    def show_final_score(self):
        self.clear_frame()
        tk.Label(self.frame, text=f"Game Over, {self.username}!", font=("Helvetica", 18), fg="white", bg="#000000").pack(pady=10)
        tk.Label(self.frame, text=f"You got {self.score} out of 20 correct!", font=("Helvetica", 16), fg="white", bg="#000000").pack(pady=10)

        tk.Button(self.frame, text="Play Again", command=self.build_start_screen).pack(pady=5)
        tk.Button(self.frame, text="Exit", command=self.destroy).pack(pady=5)

if __name__ == "__main__":
    RiddleGame().mainloop()

