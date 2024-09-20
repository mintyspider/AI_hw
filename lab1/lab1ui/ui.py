import tkinter as tk
from tkinter import messagebox
from classification import classify_bird

# Функция для обработки нажатия кнопки классификации
def on_classify(size_input, color_entry, habitat_entry, result_label):
    color_input = color_entry.get()
    habitat_input = habitat_entry.get()

    result = classify_bird(size=size_input.get(), color=color_input, habitat=habitat_input)
    if result:
        result_label.config(text=f"Это может быть: {', '.join(result)}", fg="green")
    else:
        result_label.config(text="Не удалось классифицировать птицу", fg="red")

# Функция для создания основного интерфейса
def create_window():
    root = tk.Tk()
    root.title("Классификация птиц")
    root.geometry("400x300")
    root.config(bg="#f0f8ff")

    # Заголовок
    title_label = tk.Label(root, text="Классификация птиц", font=("Helvetica", 16, "bold"), bg="#f0f8ff")
    title_label.pack(pady=10)

    # Выбор размера с кнопками
    size_input = tk.StringVar()
    size_frame = tk.Frame(root, bg="#f0f8ff")
    tk.Label(size_frame, text="Размер:", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
    tk.Radiobutton(size_frame, text="Маленький", variable=size_input, value="маленький", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
    tk.Radiobutton(size_frame, text="Средний", variable=size_input, value="средний", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
    tk.Radiobutton(size_frame, text="Большой", variable=size_input, value="большой", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT)
    size_frame.pack(pady=5)

    # Поля для ввода цвета и среды обитания
    tk.Label(root, text="Окрас:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
    color_entry = tk.Entry(root, font=("Helvetica", 12))
    color_entry.pack()

    tk.Label(root, text="Среда обитания:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
    habitat_entry = tk.Entry(root, font=("Helvetica", 12))
    habitat_entry.pack()

    # Поле для результата
    result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f8ff")
    result_label.pack()

    # Кнопка для запуска классификации
    classify_button = tk.Button(root, text="Классифицировать", font=("Helvetica", 12, "bold"), bg="#87cefa", fg="white",
                                activebackground="#4682b4", activeforeground="white",
                                command=lambda: on_classify(size_input, color_entry, habitat_entry, result_label))
    classify_button.pack(pady=20)

    return root
