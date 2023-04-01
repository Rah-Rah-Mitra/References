import tkinter as tk
from PredWeight_Model import Predict_Value


def say_hello():
    Height = Height_entry.get()
    hello_label.config(text="Predicted Weight: " + Predict_Value(int(Height)) + "Kg")

root = tk.Tk()
root.title("ML Weight Model")

Height_label = tk.Label(root, text="Enter your Height (cm):",font=("Arial",15),bg="light blue")
Height_label.pack()

Height_entry = tk.Entry(root)
Height_entry.pack()

hello_button = tk.Button(root, text="Generate", command=say_hello)
hello_button.pack()

hello_label = tk.Label(root, text="")
hello_label.pack()

root.mainloop()
