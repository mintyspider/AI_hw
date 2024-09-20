import tkinter as tk
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
    """
    Классифицирует птицу по ее размеру, окрасу и среде обитания.
    """
    x = var() # переменная для поиска
    return run(1, x, bird(x, size, color, habitat)) # ищем птицу

# Функция для обработки нажатия кнопки
def on_classify():
    """
    Обработка нажатия кнопки "Классифицировать"
    """
    size_input = size_entry.get()
    color_input = color_entry.get()
    habitat_input = habitat_entry.get()

    # Проверка корректности ввода
    if size_input not in ['маленький', 'средний', 'большой']:
        result_label.config(text="Некорректный ввод размера!")
        return
    if not color_input:
        result_label.config(text="Введите окрас птицы!")
        return
    if not habitat_input:
        result_label.config(text="Введите среду обитания птицы!")
        return

    # Классификация птицы
    result = classify_bird(size_input, color_input, habitat_input)
    if result:
        result_label.config(text=f"Это может быть: {result[0]}")
    else:
        result_label.config(text="Не удалось классифицировать птицу")

# Создание интерфейса с помощью tkinter
root = tk.Tk()
root.title("Классификация птиц")

# Поля для ввода характеристик
tk.Label(root, text="Размер (маленький, средний, большой):").pack()
size_entry = tk.Entry(root)
size_entry.pack()

tk.Label(root, text="Окрас:").pack()
color_entry = tk.Entry(root)
color_entry.pack()

tk.Label(root, text="Среда обитания:").pack()
habitat_entry = tk.Entry(root)
habitat_entry.pack()

# Кнопка для запуска классификации
classify_button = tk.Button(root, text="Классифицировать", command=on_classify)
classify_button.pack()

# Поле для отображения результата
result_label = tk.Label(root, text="")
result_label.pack()

# Запуск основного цикла tkinter
root.mainloop()
