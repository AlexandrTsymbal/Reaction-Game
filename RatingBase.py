from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    react_time = db.Column(db.Float, nullable=False)

    def __init__(self, username, react_time):
        self.username = username
        self.react_time = react_time


class RatingBase:
    def __init__(self, app):
        db.init_app(app)
        with app.app_context():
            try:
                db.create_all()
                print("Таблицы созданы или уже существуют.")
            except Exception as e:
                print(f"Ошибка при создании таблиц: {e}")

    def write_rating(self, username, result):
        try:
            existing_record = Rating.query.filter_by(username=username).first()
            if existing_record:
                if result < existing_record.react_time:
                    existing_record.react_time = result
                    print(f"Обновлено время реакции для {username}: {result}")
                else:
                    print(f"Новое время реакции для {username} не меньше предыдущего. Запись не обновлена.")
            else:
                new_rating = Rating(username=username, react_time=result)
                db.session.add(new_rating)
                print(f"Создана новая запись для {username}: {result}")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при записи данных: {e}")

    def get_all_ratings(self):
        try:
            return Rating.query.order_by(Rating.react_time).all()
        except Exception as e:
            print(f"Ошибка при получении рейтингов: {e}")
            return []
