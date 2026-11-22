from flask import Flask
import os

app = Flask(__name__)

if __name__ == "__main__":
    from views import bp
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=1337, debug=False)