from app import create_app
import threading
import time
import requests

app = create_app()


# Define a function that sends a request to the server to keep the connection alive
def keep_alive():
    while True:
        try:
            requests.get("https://retro-buster.onrender.com/bounce")
            time.sleep(300)  # Send request every 5 minutes
        except Exception as e:
            print(e)
            time.sleep(60)  # Retry every minute if there is an error


# Define a route that returns a simple response to indicate that the server is still running
@app.route("/bounce")
def ping():
    return "back"


if __name__ == "__main__":
    # Start the keep-alive thread when the app is started
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.start()

    app.run()
