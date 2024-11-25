FROM python:3.12

# Встановимо змінну середовища
ENV APP_HOME /hw02

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

COPY requirements.txt .

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Встановимо залежності всередині контейнера
RUN pip install --no-cache-dir -r requirements.txt

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 8000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "main.py"]