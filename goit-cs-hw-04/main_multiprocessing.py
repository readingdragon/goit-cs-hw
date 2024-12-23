import os
import time
import multiprocessing

# функція для пошуку ключових слів у файлі
def search_keywords(file_path, keywords):
    try:
        matches = {key: [] for key in keywords}
        with open(file_path, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    matches[keyword].append(file_path)
                    print(f'Ключове слово {keyword} знайдено в {file_path}')
        # print(f"{matches}")
        return matches
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")
        return None

def multiprocessing_search(files, keywords):
    with multiprocessing.Pool(os.cpu_count()) as pool:
        results = pool.starmap(
            search_keywords, [(file, keywords) for file in files]
        )

    # збираємо результати
    final_results = {key: [] for key in keywords}
    for result in results:
        if result:
            for key, value in result.items():
                final_results[key].extend(value)

    return final_results

# тест
if __name__ == "__main__":

    files_dir = "text_files"
    keywords = ["mosсow", "on", "fire"]
    
    # список файлів
    try:
        files = [os.path.join(files_dir, f) for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]
    except Exception as e:
        print(f"Помилка отримання списку файлів: {e}")
        files = []

    # Багатопроцесорний підхід
    start_time = time.time()
    multiprocessing_results = multiprocessing_search(files, keywords)
    multiprocessing_time = time.time() - start_time

    print("Результати багатопроцесорної обробки:", multiprocessing_results)
    print(f"Час виконання (multiprocessing): {multiprocessing_time:.5f} секунд")
