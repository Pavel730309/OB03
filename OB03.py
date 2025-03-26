import json
from typing import List, Dict, Union


# 1. Базовый класс Animal
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def make_sound(self) -> None:
        print(f"{self.name} издает звук")

    def eat(self) -> None:
        print(f"{self.name} ест")

    def to_dict(self) -> Dict:
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age
        }


# 2. Подклассы животных
class Bird(Animal):
    def __init__(self, name: str, age: int, wingspan: float):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self) -> None:
        print(f"{self.name} чирикает!")

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['wingspan'] = self.wingspan
        return data


class Mammal(Animal):
    def __init__(self, name: str, age: int, fur_color: str):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self) -> None:
        print(f"{self.name} рычит!")

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['fur_color'] = self.fur_color
        return data


class Reptile(Animal):
    def __init__(self, name: str, age: int, scale_type: str):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self) -> None:
        print(f"{self.name} шипит!")

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['scale_type'] = self.scale_type
        return data


# 5. Классы сотрудников
class ZooKeeper:
    def feed_animal(self, animal: Animal) -> None:
        print(f"Смотритель кормит {animal.name}")
        animal.eat()

    def to_dict(self) -> Dict:
        return {'type': 'ZooKeeper'}


class Veterinarian:
    def heal_animal(self, animal: Animal) -> None:
        print(f"Ветеринар лечит {animal.name}")
        print(f"{animal.name} чувствует себя лучше!")

    def to_dict(self) -> Dict:
        return {'type': 'Veterinarian'}


# 4. Класс Zoo с композицией
class Zoo:
    def __init__(self):
        self.animals: List[Animal] = []
        self.staff: List[Union[ZooKeeper, Veterinarian]] = []

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)

    def add_staff(self, employee: Union[ZooKeeper, Veterinarian]) -> None:
        self.staff.append(employee)

    # 3. Демонстрация полиморфизма
    def animal_sounds(self) -> None:
        for animal in self.animals:
            animal.make_sound()

    def save_to_file(self, filename: str) -> None:
        data = {
            'animals': [animal.to_dict() for animal in self.animals],
            'staff': [employee.to_dict() for employee in self.staff]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Zoo':
        zoo = cls()
        with open(filename) as f:
            data = json.load(f)

        # Восстановление животных
        animal_classes = {
            'Bird': Bird,
            'Mammal': Mammal,
            'Reptile': Reptile
        }
        for animal_data in data['animals']:
            cls_name = animal_data.pop('type')
            if cls_name in animal_classes:
                animal = animal_classes[cls_name](**animal_data)
                zoo.add_animal(animal)

        # Восстановление сотрудников
        staff_classes = {
            'ZooKeeper': ZooKeeper,
            'Veterinarian': Veterinarian
        }
        for staff_data in data['staff']:
            cls_name = staff_data['type']
            if cls_name in staff_classes:
                employee = staff_classes[cls_name]()
                zoo.add_staff(employee)

        return zoo


# Пример использования
def main():
    # Создаем зоопарк
    zoo = Zoo()

    # Добавляем животных
    zoo.add_animal(Bird("Воробей", 2, 15.5))
    zoo.add_animal(Mammal("Лев", 5, "золотистый"))
    zoo.add_animal(Reptile("Змея", 3, "гладкая"))

    # Добавляем сотрудников
    zoo.add_staff(ZooKeeper())
    zoo.add_staff(Veterinarian())

    # Демонстрация полиморфизма
    print("Звуки животных:")
    zoo.animal_sounds()

    # Работа сотрудников
    print("\nРабота сотрудников:")
    zoo.staff[0].feed_animal(zoo.animals[0])  # Смотритель кормит
    zoo.staff[1].heal_animal(zoo.animals[1])  # Ветеринар лечит

    # Сохраняем зоопарк в файл
    zoo.save_to_file('zoo_data.json')
    print("\nДанные зоопарка сохранены в файл 'zoo_data.json'")

    # Загружаем зоопарк из файла
    loaded_zoo = Zoo.load_from_file('zoo_data.json')
    print("\nЗагруженные данные зоопарка:")
    loaded_zoo.animal_sounds()


if __name__ == "__main__":
    main()