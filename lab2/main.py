import random
from deap import base, creator, tools, algorithms

# Целевая функция
def func(individual):
    x, y = individual
    return -x**2 - y**2 + 4,

# Задаем максимизацию как цель
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Регистрация необходимых компонентов
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -10, 10)  # диапазон поиска
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", func)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)

    # Инициализация популяции
    pop = toolbox.population(n=100)

    # Настройки генетического алгоритма
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # Настройки статистики
    stats.register("avg", lambda x: sum(val[0] for val in x) / len(x))
    stats.register("min", lambda x: min(val[0] for val in x))
    stats.register("max", lambda x: max(val[0] for val in x))

    # Запуск алгоритма
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)

    # Лучший результат
    best_individual = hof[0]
    print(f"Лучшее решение: {best_individual}, максимальная функция: {best_individual.fitness.values[0]}")

if __name__ == "__main__":
    main()
