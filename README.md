# Мини-сервис для анализа отзывов

Этот сервис на Flask и SQLite принимает отзывы и определяет их настроение (positive, negative, neutral).

## Копировать/Редактировать

```bash
# Установите Flask
pip install Flask

# Запустите приложение
python app.py
```

### Отправить отзыв (POST)

```bash
curl -X POST http://127.0.0.1:5000/reviews -H "Content-Type: application/json" -d "{\"text\": \"Очень хороший отель,рекомендую!\"}"
```

### Получить все отзывы (GET)

```bash
curl http://127.0.0.1:5000/reviews

```

### Получить только негативные отзывы

```bash
curl http://127.0.0.1:5000/reviews?sentiment=negative
```
### Получить только позитивные отзывы

```bash
curl http://127.0.0.1:5000/reviews?sentiment=positive
```
### Получить только нейтральные отзывы

```bash
curl http://127.0.0.1:5000/reviews?sentiment=neutral
```
## Ручное тестирование через браузер

- Для GET-запроса можно просто открыть в браузере:
  - http://127.0.0.1:5000/reviews?sentiment=positive
  - http://127.0.0.1:5000/reviews 