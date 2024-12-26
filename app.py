from flask import Flask
from routes import init_app
from models import app

init_app(app)

if __name__ == '__main__':
    app.run(debug=True)