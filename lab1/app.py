import tkinter as tk
from tkinter import messagebox
from kanren import Relation, facts, run, var
from sympy import symbols

# Определяем отношения для птиц
bird = Relation()

# Добавляем факты о птицах
facts(bird,
      ('воробей', 'маленький', 'коричневый', 'город'),
      ('сокол', 'средний', 'серый', 'горные'),
      ('страус', 'большой', 'черный', 'пустыня'))

# Функция для классификации птиц
def classify_bird(size, color, habitat):
    x = var()
    return run(1, x, bird(x, size, color, habitat))

# Функция для обработки нажатия кнопки
def on_classify():
    size_input = size_entry.get()
    color_input = color_entry.get()
    habitat_input = habitat_entry.get()

    if size_input not in ['маленький', 'средний', 'большой']:
        messagebox.showerror("Ошибка ввода", "Некорректный ввод размера! Введите маленький, средний или большой.")
        return
    if not color_input:
        messagebox.showerror("Ошибка ввода", "Введите окрас птицы!")
        return
    if not habitat_input:
        messagebox.showerror("Ошибка ввода", "Введите среду обитания птицы!")
        return

    result = classify_bird(size_input, color_input, habitat_input)
    if result:
        result_label.config(text=f"Это может быть: {result[0]}", fg="green")
    else:
        result_label.config(text="Не удалось классифицировать птицу", fg="red")

# Создание красивого интерфейса с помощью tkinter
root = tk.Tk()
root.title("Классификация птиц")
root.geometry("400x300")
root.config(bg="#f0f8ff")

# Заголовок
title_label = tk.Label(root, text="Классификация птиц", font=("Helvetica", 16, "bold"), bg="#f0f8ff")
title_label.pack(pady=10)

# Поля для ввода характеристик
tk.Label(root, text="Размер (маленький, средний, большой):", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
size_entry = tk.Entry(root, font=("Helvetica", 12))
size_entry.pack()

tk.Label(root, text="Окрас:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
color_entry = tk.Entry(root, font=("Helvetica", 12))
color_entry.pack()

tk.Label(root, text="Среда обитания:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
habitat_entry = tk.Entry(root, font=("Helvetica", 12))
habitat_entry.pack()

# Кнопка для запуска классификации
classify_button = tk.Button(root, text="Классифицировать", font=("Helvetica", 12, "bold"), bg="#87cefa", fg="white", 
                            activebackground="#4682b4", activeforeground="white", command=on_classify)
classify_button.pack(pady=20)

# Поле для отображения результата
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f8ff")
result_label.pack()

# Запуск основного цикла tkinter
root.mainloop()
