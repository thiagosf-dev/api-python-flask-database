import bcrypt
from database import db
from flask import Flask, jsonify, request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin@localhost:3307/flask-crud"

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

    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "O username e o password devem ser informados"}), 400

    username = data.get("username")
    password = str.encode(data.get("password"))

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.checkpw(password, str.encode(user.password)):
        return jsonify({"message": "Credenciais inválidas"}), 401

    login_user(user)

    return jsonify({"message": "Autenticação realizada com sucesso"})


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    # password = data.get("password")
    password = bcrypt.hashpw(str.encode(
        data.get("password")), bcrypt.gensalt())
    role = data.get("role")

    if not username or not password:
        return jsonify({"message": "O username e o password devem ser informados"}), 400

    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201


@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if not id_user or not user:
        return jsonify({"message": "Dados do usuário inválidos"})

    return jsonify({"message": "Usuário atualizado com sucesso"})


@app.route("/users", methods=["GET"])
@login_required
def read_users():
    users = db.session.query(User).order_by(User.username).all()
    users_list = [{"id": user.id, "username": user.username,
                   "role": user.role} for user in users]
    return jsonify(users_list)


@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    if current_user.role != "admin":
        return jsonify({"message": "Você não possui permissão para executar esta operação"}), 403

    user = User.query.get(id_user)

    if not id_user or not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if current_user.id == user.id:
        return jsonify({"message": "Operação não permitida"}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário excluído com sucesso"})


@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    password = data.get("password")
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Você não possui permissão para executar esta operação"}), 403

    if not id_user or not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if not password:
        return jsonify({"message": "Credenciais inválidas"}), 401

    user.password = data.get("password")
    db.session.commit()

    return jsonify({"message": "Usuário atualizado com sucesso"})


@app.route("/info", methods=["GET"])
def hello_world():
    return jsonify({
        "API_name": "api-auth-flask-sqlite",
        "API_status": "OK",
        "API_version": "1.0.0",
    })


if __name__ == '__main__':
    app.run(debug=True)
