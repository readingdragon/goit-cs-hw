import os
import time
import threading
from queue import Queue

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
        return matches
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")
        return None

# багатопотоковa обробкa
def threaded_search(files, keywords):
    def worker(file_list, result_queue):
        results = {key: [] for key in keywords}
        for file in file_list:
            file_results = search_keywords(file, keywords)
            if file_results:
                for key, value in file_results.items():
                    results[key].extend(value)
        result_queue.put(results)

    threads = []
    result_queue = Queue()
    num_threads = min(len(files), 10)  # 10 потоків, якщо файлів більше 10
    chunk_size = len(files) // num_threads

    for i in range(num_threads):
        start = i * chunk_size
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=worker, args=(files[start:end], result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # збираємо результати
    final_results = {key: [] for key in keywords}
    while not result_queue.empty():
        thread_result = result_queue.get()
        for key, value in thread_result.items():
            print('/n')
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

    start_time = time.time()
    threaded_results = threaded_search(files, keywords)
    threaded_time = time.time() - start_time

    print("Результати багатопотокової обробки:", threaded_results)
    print(f"Час виконання (threading): {threaded_time:.5f} секунд")
