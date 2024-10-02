import numpy as np

class Vector:
    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], int):  # Если передана длина
            self.n = values[0]  # длина вектора
            self.v = np.zeros(self.n)  # создаем массив длины n
        else:  # Если передан список значений
            self.n = len(values)
            self.v = np.array(values)

    # Обращение по индексу
    def __getitem__(self, i):
        return self.v[i]

    def __setitem__(self, i, value):
        self.v[i] = value


class Matrix:
    def __init__(self, n, m):
        self.n = n  # количество строк
        self.m = m  # количество столбцов
        self.v = np.random.uniform(-0.5, 0.5, (n, m))  # матрица весов со случайными значениями

    # Обращение по индексу
    def __getitem__(self, idx):
        i, j = idx  # распаковка индексов
        return self.v[i, j]

    def __setitem__(self, idx, value):
        i, j = idx  # распаковка индексов
        self.v[i, j] = value


class Network:
    class LayerT:
        def __init__(self, input_size, output_size):
            self.x = Vector(input_size)  # вход слоя
            self.z = Vector(output_size)  # активированный выход слоя
            self.df = Vector(output_size)  # производная активации слоя

    def __init__(self, sizes):
        self.layersN = len(sizes) - 1  # количество слоёв
        self.weights = [Matrix(sizes[k], sizes[k - 1]) for k in range(1, len(sizes))]  # матрицы весов
        self.L = [self.LayerT(sizes[k - 1], sizes[k]) for k in range(1, len(sizes))]  # инициализация слоёв
        self.deltas = [Vector(sizes[k]) for k in range(1, len(sizes))]  # вектора дельт

    # Прямое распространение
    def forward(self, input):
        for k in range(self.layersN):
            if k == 0:
                for i in range(input.n):
                    self.L[k].x[i] = input[i]  # копируем вход на первый слой
            else:
                for i in range(self.L[k - 1].z.n):
                    self.L[k].x[i] = self.L[k - 1].z[i]  # передаем выход с предыдущего слоя как вход текущего

            for i in range(self.weights[k].n):
                y = 0
                for j in range(self.weights[k].m):
                    y += self.weights[k][i, j] * self.L[k].x[j]

                # Активация с помощью ReLU
                self.L[k].z[i] = max(0, y)  # ReLU
                self.L[k].df[i] = 1 if y > 0 else 0  # производная ReLU

        return self.L[self.layersN - 1].z  # возвращаем результат
    
    def backward(self, output, error):
        last = self.layersN - 1
        error[0] = 0  # обнуляем ошибку (передается как список для изменения)

        # Находим дельту для последнего слоя
        for i in range(output.n):
            e = self.L[last].z[i] - output[i]  # разность значений
            self.deltas[last][i] = e * self.L[last].df[i]  # вычисляем дельту
            error[0] += e ** 2 / 2  # прибавляем к ошибке половину квадрата разности

        # Вычисляем дельты для предыдущих слоёв
        for k in range(last, 0, -1):
            for i in range(self.weights[k].m):
                self.deltas[k - 1][i] = 0

                # Умножаем на транспонированную матрицу весов и вычисляем новую дельту
                for j in range(self.weights[k].n):
                    self.deltas[k - 1][i] += self.weights[k][j, i] * self.deltas[k][j]

                # Умножаем на производную активационной функции
                self.deltas[k - 1][i] *= self.L[k - 1].df[i]
        
    def update_weights(self, alpha):
        for k in range(self.layersN):
            for i in range(self.weights[k].n):
                for j in range(self.weights[k].m):
                    # Обновляем весовой коэффициент с учётом скорости обучения
                    self.weights[k][i, j] -= alpha * self.deltas[k][i] * self.L[k].x[j]

    def train(self, X, Y, alpha, eps, epochs):
        epoch = 1  # номер эпохи

        while epoch <= epochs:
            error = [0]  # обнуляем ошибку (список для передачи по ссылке)

            # Проходим по всем элементам обучающего набора
            for i in range(len(X)):
                self.forward(X[i])  # прямое распространение
                self.backward(Y[i], error)  # обратное распространение ошибки
                self.update_weights(alpha)  # обновление весовых коэффициентов

            # Выводим текущий номер эпохи и ошибку
            print(f"epoch: {epoch}, error: {error[0]}")

            # Прерываем, если ошибка меньше заданного порога
            if error[0] <= eps:
                break

            epoch += 1  # увеличиваем номер эпохи

# массив входных обучающих векторов
X = [
    np.array([0, 0]),
    np.array([0, 1]),
    np.array([1, 0]),
    np.array([1, 1])
]

# массив выходных обучающих векторов
Y = [
    np.array([0.0]),  # 0 ^ 0 = 0
    np.array([1.0]),  # 0 ^ 1 = 1
    np.array([1.0]),  # 1 ^ 0 = 1
    np.array([0.0])   # 1 ^ 1 = 0
]

# создаём сеть с двумя входами, тремя нейронами в скрытом слое и одним выходом
network = Network([2, 3, 1])

# Запускаем обучение сети с заданными параметрами
network.train(X, Y, alpha=0.5, eps=1e-7, epochs=100000)

# Проверяем выходные данные сети для каждого входного вектора
for i in range(4):
    output = network.forward(X[i])  # Прямое распространение
    print(f"X: {X[i][0]} {X[i][1]}, Y: {Y[i][0]}, output: {output[0]}")
