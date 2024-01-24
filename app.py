from database import db
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "O username e o password devem ser informados"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.password == password:
        return jsonify({"message": "Credenciais inválidas"}), 401

    login_user(user)

    return "LOGGED"


@app.route("/info", methods=["GET"])
def hello_world():
    return jsonify({
        "API_name": "api-auth-flask-sqlite",
        "API_status": "OK",
        "API_version": "1.0.0",
    })


if __name__ == '__main__':
    app.run(debug=True)
