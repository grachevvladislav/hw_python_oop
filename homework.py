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
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,  # шаг — бег, ходьба; гребок — плавание
                 duration: float,  # длительность тренировки
                 weight: float  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean: float = self.get_distance() / self.duration_h
        return mean

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        obj: InfoMessage = InfoMessage(type(self).__name__,
                                       self.duration_h,
                                       self.get_distance(),
                                       self.get_mean_speed(),
                                       self.get_spent_calories())
        return obj


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.coeff_calorie_1 * self.get_mean_speed()
                            - self.coeff_calorie_2) * self.weight
                           / self.M_IN_KM * self.duration_h * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: int = 0.035
    coeff_calorie_2: int = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float  # Рост
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.coeff_calorie_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.height)
                     * self.coeff_calorie_2 * self.weight)
                    * self.duration_h * self.MIN_IN_H)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_1: int = 1.1
    coeff_calorie_2: int = 2

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
                / self.M_IN_KM / self.duration_h)
        return mean

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.coeff_calorie_1)
                    * self.coeff_calorie_2 * self.weight)
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
