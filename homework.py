class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type  # тип тренировки
        self.duration = duration  # длительность тренировки
        self.distance = distance  # дистанция, преодолённая за тренировку
        self.speed = speed  # средняя скорость движения
        self.calories = calories  # потраченные за время тренировки килокалории

    def get_message(self) -> str:
        message = f'''Тип тренировки: {self.training_type}; \
Длительность: {self.duration:.3f} ч.; \
Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; \
Потрачено ккал: {self.calories:.3f}.'''
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,  # шаг — бег, ходьба; гребок — плавание
                 duration: float,  # длительность тренировки
                 weight: float  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean = self.get_distance() / self.duration
        return mean

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        obj = InfoMessage(type(self).__name__,
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return obj


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories = ((18 * self.get_mean_speed() - 20) * self.weight
                    / self.M_IN_KM * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float  # Рост
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((0.035 * self.weight + (self.get_mean_speed() ** 2
                    // self.height) * 0.029 * self.weight)
                    * self.duration * 60)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean = (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)
        return mean

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        obj = Swimming(*data)
    elif workout_type == 'RUN':
        obj = Running(*data)
    elif workout_type == 'WLK':
        obj = SportsWalking(*data)
    else:
        obj = None
    return obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
