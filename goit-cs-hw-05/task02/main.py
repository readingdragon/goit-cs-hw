import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        print('text downloaded')
        return response.text
    except requests.RequestException as e:
        print(f'ooooppsss, something goes wrong: {e}')
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    text = text.lower()
    words = text.split()


    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))
    
    all_words_dict = dict(reduced_values)

    top_10 = dict(sorted(all_words_dict.items(), key=lambda x: x[1], reverse=True)[:10])

    return top_10
    # return dict(reduced_values)

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://archive.org/stream/cu31924024323242/cu31924024323242_djvu.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        # search_words = ['moscow', 'on', 'fire']

        # result = map_reduce(text, search_words)
        result = map_reduce(text)

        top_words = list(result.keys())
        frequency = list(result.values())

        plt.rcParams['figure.facecolor'] = '#333333'
        plt.rcParams['axes.facecolor'] = '#242424'
        plt.rcParams['axes.labelcolor'] = 'y'
        plt.rcParams['xtick.color'] = 'c'
        plt.rcParams['ytick.color'] = 'c'
        plt.rcParams['grid.alpha'] = '0.4'

        plt.figure(figsize=(11, 6))
        plt.barh(top_words, frequency, color='#036896', edgecolor='0', alpha=0.8)
        plt.title(f"Top 10 Most Frequent Words in Text",  fontsize=12, color="#f09902")
        plt.xlabel(f'Frequency')
        plt.ylabel('Words')
        plt.grid(True, color = '#036896')
        plt.gca().invert_yaxis()
        plt.show()

        print("Результат підрахунку слів:", result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
