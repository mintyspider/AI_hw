import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score

# Функции активации и их производные
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x))  # для стабильности численных вычислений
    return exps / np.sum(exps, axis=1, keepdims=True)

# Функция потерь (кросс-энтропия)
def cross_entropy_loss(y_true, y_pred):
    return -np.mean(np.sum(y_true * np.log(y_pred + 1e-10), axis=1))

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Инициализация весов
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))

    # Прямое распространение
    def forward(self, X):
        self.z1 = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.a1 = relu(self.z1)  # ReLU на скрытом слое
        self.z2 = np.dot(self.a1, self.weights_hidden_output) + self.bias_output
        self.a2 = softmax(self.z2)  # Softmax на выходном слое
        return self.a2

    # Обратное распространение
    def backward(self, X, y_true, y_pred, learning_rate):
        m = X.shape[0]  # количество примеров

        # Вычисляем градиенты для весов и смещений
        dz2 = y_pred - y_true
        dw2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        dz1 = np.dot(dz2, self.weights_hidden_output.T) * relu_derivative(self.z1)
        dw1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        # Обновляем веса и смещения
        self.weights_hidden_output -= learning_rate * dw2
        self.bias_output -= learning_rate * db2
        self.weights_input_hidden -= learning_rate * dw1
        self.bias_hidden -= learning_rate * db1

    # Обучение модели
    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = cross_entropy_loss(y, y_pred)
            self.backward(X, y, y_pred, learning_rate)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

    # Предсказание классов
    def predict(self, X):
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)

# Загружаем датасет digits
digits = load_digits()
X = digits.data
y = digits.target

# Преобразование целевых меток в формат OneHot
encoder = OneHotEncoder(sparse_output=False)
y_onehot = encoder.fit_transform(y.reshape(-1, 1))

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2, random_state=42)

# Параметры нейронной сети
input_size = X_train.shape[1]  # Количество входных признаков
hidden_size = 64  # Количество нейронов в скрытом слое
output_size = y_onehot.shape[1]  # Количество выходов (классов)

# Создаём и обучаем нейронную сеть
network = NeuralNetwork(input_size, hidden_size, output_size)
network.train(X_train, y_train, epochs=1000, learning_rate=0.1)

# Оцениваем качество на тестовой выборке
y_pred_test = network.predict(X_test)
y_test_labels = np.argmax(y_test, axis=1)  # Преобразуем one-hot метки обратно в классы

accuracy = accuracy_score(y_test_labels, y_pred_test)
print(f"Точность на тестовой выборке: {accuracy * 100:.2f}%")
