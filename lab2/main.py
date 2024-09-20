import random
from deap import base, creator, tools, algorithms

# Целевая функция
def func(individual):
    # Получаем x и y из списка "индивида"
    x, y = individual
    # Возвращаем значение целевой функции x^2 + y^2 - 4
    # Важно возвращать в виде кортежа, т.к. DEAP ожидает, что фитнес будет кортежем
    return x**2 + y**2 - 4,

# Создаем цель для минимизации
# FitnessMin говорит DEAP, что мы хотим минимизировать функцию
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# Определяем тип "индивида" как список с фитнесом для минимизации
creator.create("Individual", list, fitness=creator.FitnessMin)

# Инициализируем инструментарий для генетического алгоритма
toolbox = base.Toolbox()

# Генерируем случайные значения для x и y в диапазоне [-10, 10]
toolbox.register("attr_float", random.uniform, -10, 10)

# Создаем "индивида" как список из двух атрибутов (x и y)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)

# Создаем популяцию как список индивидов
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Регистрируем целевую функцию для оценки индивидов
toolbox.register("evaluate", func)

# Регистрируем операцию кроссовера с методом cxBlend (смешивание генов двух родителей)
toolbox.register("mate", tools.cxBlend, alpha=0.5)

# Регистрируем мутацию с использованием гауссовского шума
# mu=0 - среднее распределения мутации, sigma=1 - стандартное отклонение
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)

# Регистрируем селекцию с методом турнира (случайное соревнование между индивидами)
toolbox.register("select", tools.selTournament, tournsize=3)

# Главная функция алгоритма
def main():
    # Инициализируем генератор случайных чисел для воспроизводимости эксперимента
    random.seed(42)

    # Создаем начальную популяцию из 100 индивидов
    pop = toolbox.population(n=100)

    # HallOfFame сохраняет лучший индивид по ходу эволюции
    hof = tools.HallOfFame(1)

    # Создаем объект для сбора статистики
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    
    # Регистрируем статистику для среднего значения фитнеса в популяции
    stats.register("avg", lambda x: sum(val[0] for val in x) / len(x))
    
    # Регистрируем статистику для минимального значения фитнеса
    stats.register("min", lambda x: min(val[0] for val in x))
    
    # Регистрируем статистику для максимального значения фитнеса
    stats.register("max", lambda x: max(val[0] for val in x))

    # Запуск генетического алгоритма с параметрами:
    # популяция, инструменты, вероятность кроссовера (cxpb=0.5),
    # вероятность мутации (mutpb=0.2), количество поколений (ngen=50)
    # сбор статистики и сохранение лучшего решения
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)

    # Выводим лучшее найденное решение и значение целевой функции в этой точке
    best_individual = hof[0]
    print(f"Лучшее решение: {best_individual}, минимум функции: {best_individual.fitness.values[0]}")

# Если этот файл запущен как основной, то вызываем функцию main
if __name__ == "__main__":
    main()
