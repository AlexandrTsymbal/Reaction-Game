from flask import Flask, render_template, redirect, url_for, request, jsonify
from RatingBase import RatingBase


class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ReactionGame.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.base = RatingBase(self.app)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            if request.method == 'POST':
                name = request.form.get('name')
                if name:
                    return redirect(url_for('game', name=name))
            return render_template('home.html')

        @self.app.route('/game/<name>')
        def game(name):
            return render_template('game.html', name=name)

        @self.app.route('/rating')
        def rating():
            ratings = self.base.get_all_ratings()
            return render_template('rating.html', ratings=ratings)

        @self.app.route('/save_reaction_time', methods=['POST'])
        def save_reaction_time():
            data = request.get_json()
            reaction_time = data.get('reaction_time')
            username = data.get('username')
            if not reaction_time or not username:
                return jsonify({"status": "error", "message": "Invalid data"}), 400

            try:
                self.base.write_rating(username, reaction_time)
                return jsonify({"status": "success", "reaction_time": reaction_time})
            except Exception as e:
                print(f"Ошибка при сохранении времени реакции: {e}")
                return jsonify({"status": "error", "message": "Failed to save reaction time"}), 500

    def run(self):
        self.app.run(debug=True)
