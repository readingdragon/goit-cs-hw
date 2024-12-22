from pymongo import MongoClient, errors

def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.server_info()  # Перевіряємо підключення
        db = client["cats_database"]
        return db
    except errors.ServerSelectionTimeoutError:
        print("Помилка: Не вдалося підключитися до MongoDB.")
        return None
    except Exception as e:
        print(f"Невідома помилка: {e}")
        return None

# read
def get_all_cats():
    db = connect_to_mongo()
    try:
        cats = db["cats"].find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка під час читання даних: {e}")

# Функція для пошуку кота за ім'ям
def get_cat_by_name():
    db = connect_to_mongo()
    try:
        # Вивести інформацію про кота за ім'ям
        name = input("Введіть ім'я кота: ")
        cat = db["cats"].find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка під час пошуку кота: {e}")

# Функція для оновлення віку кота
def update_cat_age():
    db = connect_to_mongo()
    try:
        # Оновити вік кота за ім'ям
        name = input("Введіть ім'я кота: ")
        new_age = int(input("Введіть новий вік: "))
        result = db["cats"].update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print("Вік кота оновлено.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка під час оновлення віку кота: {e}")

# Функція для додавання нової характеристики коту
def add_feature_to_cat():
    db = connect_to_mongo()
    try:
        # Додати нову характеристику коту за ім'ям
        name = input("Введіть ім'я кота: ")
        new_feature = input("Введіть нову характеристику: ")
        result = db["cats"].update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count:
            print("Характеристику додано.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка під час додавання характеристики: {e}")

# Функція для видалення кота за ім'ям
def delete_cat_by_name():
    db = connect_to_mongo()
    try:
        # Видалити запис про кота за ім'ям
        name = input("Введіть ім'я кота: ")
        result = db["cats"].delete_one({"name": name})
        if result.deleted_count:
            print("Запис про кота видалено.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка під час видалення кота: {e}")

# Функція для видалення всіх записів у колекції
def delete_all_cats():
    db = connect_to_mongo()
    try:
        # Видалити всі записи з колекції
        confirmation = input("Ви впевнені, що хочете видалити всі записи? (yes/no): ")
        if confirmation.lower() == "yes":
            result = db["cats"].delete_many({})
            print(f"Видалено {result.deleted_count} записів.")
        else:
            print("Операцію скасовано.")
    except Exception as e:
        print(f"Помилка під час видалення записів: {e}")

# Меню для взаємодії
def main():
    while True:
        print("\nМеню:")
        print("1. Вивести всі записи")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати коту фічу")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити всі записи")
        print("7. Вихід")

        choice = input("Виберіть дію (1-7): ")

        if choice == "1":
            get_all_cats()
        elif choice == "2":
            get_cat_by_name()
        elif choice == "3":
            update_cat_age()
        elif choice == "4":
            add_feature_to_cat()
        elif choice == "5":
            delete_cat_by_name()
        elif choice == "6":
            delete_all_cats()
        elif choice == "7":
            print("Допобачення.")
            break
        else:
            print("Будьте уважним і спробуйте ще раз.")

if __name__ == "__main__":
    main()