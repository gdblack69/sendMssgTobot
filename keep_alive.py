from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running..."

def run():
    # Run the Flask app in production mode (set threaded=True for multiple requests handling)
    app.run(host="0.0.0.0", port=8080, threaded=True)

def keep_alive():
    # Run the Flask app in a separate thread to keep it alive
    t = threading.Thread(target=run)
    t.start()
