import os
import random
import string

def generate_random_words(word_count):
    try:
        words = []
        for _ in range(word_count):
            word_length = random.randint(3, 9)  # довжина слова від 3 до 10 символів
            word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
            words.append(word)

        key_words = ["mosсow", "on", "fire"]
        for word in key_words:
            position = random.randint(0, len(words))
            words.insert(position, word)
            
        return ' '.join(words)
    except Exception as e:
        print(f"Exception під час генерації слів: {e}")
        return ""

def generate_text_files(file_count, words_per_file, output_dir="text_files"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i in range(1, file_count + 1):
            file_name = os.path.join(output_dir, f"file_{i}.txt")
            try:
                content = generate_random_words(words_per_file)
                if not content:
                    raise ValueError("Генерація тексту не вдалася.")
                
                with open(file_name, 'w') as file:
                    file.write(content)
                print(f"Файл {file_name} створено.")
            except Exception as e:
                print(f"Exception під час створення файлу {file_name}: {e}")
    except OSError as e:
        print(f"Помилка роботи з файловою системою: {e}")
    except Exception as e:
        print(f"Неочікувана помилка: {e}")

# кількість файлів і слів у кожному файлі
file_count = 99999
words_per_file = 66

try:
    generate_text_files(file_count, words_per_file)
except Exception as e:
    print(f"Exception: {e}")
