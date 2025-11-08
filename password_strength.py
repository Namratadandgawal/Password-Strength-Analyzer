import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk   # make sure Pillow is installed (pip install pillow)
import math
import string
import os

# Common weak passwords list (basic local dictionary)
weak_passwords = ["password", "123456", "qwerty", "admin", "letmein", "welcome"]

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
    if charset == 0:
        return 0
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def analyze_password():
    password = entry.get()
    feedback = []
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password too short (min 8 chars).")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters (!@# etc).")

    if password.lower() in weak_passwords:
        feedback.append("This is a common password!")
        score = 1

    entropy = calculate_entropy(password)
    if entropy < 30:
        level = "Weak"
        color = "red"
    elif entropy < 50:
        level = "Moderate"
        color = "orange"
    else:
        level = "Strong"
        color = "green"

    progress['value'] = (score / 5) * 100
    progress_style.configure("TProgressbar", troughcolor='white', background=color)

    result_label.config(text=f"Strength: {level} | Entropy: {entropy} bits", fg=color)
    feedback_label.config(text="\n".join(feedback) if feedback else "Good password!")
    suggest_strong_password(password)

def suggest_strong_password(pwd):
    suggestion = pwd
    if len(pwd) < 8:
        suggestion += "@" + "123"
    if not any(c.isupper() for c in pwd):
        suggestion = "A" + suggestion
    if not any(c.isdigit() for c in pwd):
        suggestion += "7"
    suggestion_label.config(text=f"Suggested Stronger Password: {suggestion}")

# Tkinter UI
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("500x450")
root.config(bg="#f0f0f0")

# ✅ Load and display demo image from screenshots folder
image_path = os.path.join("screenshots", "demo.png")
try:
    img = Image.open(image_path)
    img = img.resize((200, 120))  # adjust as needed
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo, bg="#f0f0f0")
    img_label.pack(pady=10)
except Exception as e:
    print(f"Image not found or cannot be loaded: {e}")

tk.Label(root, text="Enter Password:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
entry = tk.Entry(root, show="*", width=40, font=("Arial", 12))
entry.pack()

ttk.Style().theme_use('default')
progress_style = ttk.Style()
progress_style.configure("TProgressbar", thickness=20, background="red")

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
progress.pack(pady=15)

tk.Button(root, text="Check Strength", command=analyze_password, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
result_label.pack()

feedback_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f0f0", fg="red")
feedback_label.pack(pady=5)

suggestion_label = tk.Label(root, text="", font=("Arial", 10, "italic"), bg="#f0f0f0", fg="blue")
suggestion_label.pack(pady=5)

root.mainloop()
