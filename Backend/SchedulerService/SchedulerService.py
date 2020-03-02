#!flask/bin/python
from flask import Flask
import threading
import Backend.SchedulerService.scheduling as sc

app = Flask(__name__)

@app.route('/scheduler/')
def index():
    print("You have just successfully executed the Scheduling Service!")
    thread = threading.Thread(target=sc.doScheduling, args=())
    thread.daemon = True
    thread.start()
    return "You have just successfully executed the Scheduling Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5006)

