import os
import random

def generate_random_files(file_count, output_dir="test_dir"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        suffixes = ["txt", "doc", "pdf", "py"]
        for i in range(1, file_count + 1):
            suffix = random.choice(suffixes)
            file_name = os.path.join(output_dir, f"file_{i}.{suffix}")

            with open(file_name, 'w') as file:
                file.write("moscow on fire!")
            print(f"Файл {file_name} створено.")
    except OSError as e:
        print(f"Помилка роботи з файловою системою: {e}")
    except Exception as e:
        print(f"Неочікувана помилка: {e}")

# кількість файлів
file_count = 99999

try:
    generate_random_files(file_count)
except Exception as e:
    print(f"Exception: {e}")
