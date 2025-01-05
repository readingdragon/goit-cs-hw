FROM python:3.12

# Робоча директорія
WORKDIR /hw06

# Копіювання залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання файлів
COPY . .

# Вказівка порту
EXPOSE 3000

# Запуск програми
ENTRYPOINT ["python", "main.py"]

