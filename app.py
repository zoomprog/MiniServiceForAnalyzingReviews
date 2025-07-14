from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)


POSITIVE_WORDS = [
    'хорош', 'люблю', 'отлично', 'прекрасно', 'супер', 'замечательно',
    'великолепно', 'удивительно', 'рекомендую', 'чисто', 'комфортно',
    'дружелюбно', 'приветливо', 'уютно', 'превосходно', 'идеально',
    'лучший', 'восхитительно', 'понравился', 'достойно', 'приятно',
    'удобно', 'современно', 'красиво', 'быстро', 'спасибо', 'тепло',
    'безупречно', 'высший', 'потрясающе', 'шикарно', 'рад', 'доволен'
]
NEGATIVE_WORDS = [
    'плохо', 'ненавиж', 'отвратительно', 'ужасно', 'кошмар', 'ужасный',
    'грязно', 'шумно', 'невежливо', 'разочарован', 'разочарование',
    'не советую', 'проблема', 'неудобно', 'холодно', 'грязный', 'старый',
    'обман', 'обманули', 'раздражает', 'медленно', 'долго', 'не понравился',
    'хамство', 'грубость', 'неприятно', 'разбитый', 'сломано', 'грязь',
    'плесень', 'воняет', 'плесневый', 'не работает', 'не рекомендую',
    'разочарование', 'разочарован', 'разочаровала', 'разочарованы', 'разочаровал'
]

"""
    Определяет настроение отзыва по ключевым словам.
"""
def analize_sentiment(text):
    
    text_lower = text.lower()
    if any(word in text_lower for word in NEGATIVE_WORDS):
        return 'negative'
    elif any(word in text_lower for word in POSITIVE_WORDS):
        return 'positive'
    else:
        return 'neutral'

"""
Создаёт и возвращает соединение с базой данных SQLite.
"""
def get_db_connection():
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    return conn

"""
Инициализирует базу данных.
"""
def init_db():

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

"""
Принимает отзыв в формате JSON, определяет его настроение,сохраняет в БД и возвращает результат в формате JSON.
"""
@app.route('/reviews', methods=['POST'])
def add_review():
    
    data = request.get_json()
    text = data.get('text', '')
    sentiment = analize_sentiment(text)
    created_at = datetime.utcnow().isoformat()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    review_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    }), 201


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment = request.args.get('sentiment')
    conn = get_db_connection()
    c = conn.cursor()
    if sentiment:
        c.execute('SELECT * FROM reviews WHERE sentiment = ?', (sentiment,))
    else:
        c.execute('SELECT * FROM reviews')
    reviews = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(reviews)

"""
Главная страница с HTML-формой для ручного ввода отзыва.
"""
@app.route('/', methods=['GET', 'POST'])
def index():

    sentiment = None
    feedback = None
    if request.method == 'POST':
        feedback = request.form['feedback']
        sentiment = analize_sentiment(feedback)
        # Сохраняем отзыв в БД
        created_at = datetime.utcnow().isoformat()
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
            (feedback, sentiment, created_at)
        )
        conn.commit()
        conn.close()
    return render_template('index.html', sentiment=sentiment, feedback=feedback)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)