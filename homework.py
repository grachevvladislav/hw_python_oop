from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # тип тренировки
    duration: float  # длительность тренировки
    distance: float  # дистанция, преодолённая за тренировку
    speed: float  # средняя скорость движения
    calories: float  # потраченные за время тренировки килокалории
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; Ср. '
               'скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(training_type=self.training_type,
                                   duration=self.duration,
                                   distance=self.distance,
                                   speed=self.speed,
                                   calories=self.calories)


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
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                            - self.COEFF_CALORIE_2) * self.weight
                           / self.M_IN_KM * self.duration_h * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: int = 0.035
    COEFF_CALORIE_2: int = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float  # Рост
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_CALORIE_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.height)
                     * self.COEFF_CALORIE_2 * self.weight)
                    * self.duration_h * self.MIN_IN_H)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1: int = 1.1
    COEFF_CALORIE_2: int = 2

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
        calories = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                    * self.COEFF_CALORIE_2 * self.weight)
        return calories


class_select: dict = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in class_select:
        obj = class_select[workout_type](*data)
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
