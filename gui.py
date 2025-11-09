import tkinter as tk
import json
from tkinter import messagebox

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🧠 Python Quiz")
        self.master.geometry("750x600")
        self.master.resizable(False, False)

        self.question_index = 0
        self.score = 0

        self.load_questions()
        self.create_widgets()
        self.show_question()

    def load_questions(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        except Exception as e:
            messagebox.showerror("Fehler", f"Die Fragen konnten nicht geladen werden: {e}")
            self.master.quit()

    def create_widgets(self):
        self.question_label = tk.Label   (self.master, text="", height=2, wraplength=600, font=("Arial", 22), pady=30)
        self.question_label.pack()

        self.option_buttons = []
        for key in ["A", "B", "C", "D"]:
            btn = tk.Button(self.master, text="", width=40, bg="wheat1", font=("Arial", 18),
                            command=lambda k=key: self.check_answer(k))
            btn.pack(pady=10)
            self.option_buttons.append(btn)

        self.output_text = tk.StringVar()
        self.output_box = tk.Label(self.master, textvariable=self.output_text, font=("Arial", 18))
        self.output_box.pack(pady=30)

        self.ok_btn = tk.Button(self.master, text="OK", bg="lawn green", font=("Arial", 18), command=self.show_question)
        self.ok_btn.pack(pady=10)
        self.ok_btn["state"] = "disabled"

    def show_question(self):
        self.output_text.set("")      
        self.ok_btn["state"] = "disabled"

        if self.question_index < len(self.questions):
            q = self.questions[self.question_index]
            self.question_label.config(text=f"Q{self.question_index + 1}: {q['question']}")

            for i, key in enumerate(["A", "B", "C", "D"]):
                self.option_buttons[i].config(text=f"{key}. {q['options'][key]}")
                # enable answer
                self.option_buttons[i]["state"] = "normal"
        else:
            self.show_result()

    def check_answer(self, selected_option):
        # disable answer
        for i in range(len(["A", "B", "C", "D"])):
            self.option_buttons[i]["state"] = "disabled"
        correct = self.questions[self.question_index]["answer"]
        if selected_option == correct:
            self.output_text.set("✅ Deine Antwort: " + correct + " ist richtig!")
            self.score += 1
        else:
            self.output_text.set("❌ Falsch. Die richtige Antwort ist: " + correct)
        self.ok_btn["state"] = "normal"
        self.question_index += 1

    def show_result(self):
        percentage = (self.score / len(self.questions)) * 100
        msg = f"✅ Ergebnis: {self.score} / {len(self.questions)}\n🧮 Percentage: {percentage:.1f}%"

        if percentage == 100:
            msg += "\n🎉 Perfekt!"
        elif percentage >= 70:
            msg += "\n👍 Gut gemacht!"
        else:
            msg += "\n📘 Übe weiter!"

        messagebox.showinfo("Quiz beendet", msg)
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
