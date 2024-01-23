from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "_app_secrete_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "status": "OK",
        "version": "1.0.0",
        "API_name": "authentication-flask-api"
    })


if __name__ == "__main__":
    app.run(debug=True)
