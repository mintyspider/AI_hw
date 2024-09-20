from kanren import Relation, facts, run, var

# Определяем отношения для птиц
bird = Relation()

# Добавляем факты о птицах
facts(bird,
      ('воробей', 'маленький', 'коричневый', 'город'),
      ('сокол', 'средний', 'серый', 'горные'),
      ('страус', 'большой', 'черный', 'пустыня'))

# Функция для классификации птиц по одному, двум или трём критериям
def classify_bird(size=None, color=None, habitat=None):
    x = var()
    conditions = []

    if size:
        conditions.append(bird(x, size, var(), var()))
    if color:
        conditions.append(bird(x, var(), color, var()))
    if habitat:
        conditions.append(bird(x, var(), var(), habitat))

    if not conditions:
        return []

    result = run(0, x, *conditions)
    return result
