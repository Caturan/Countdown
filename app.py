from flask import Flask, render_template, request, jsonify
from threading import Thread
import time
import countdown

app = Flask(__name__)

timer_info = {
    'running': False,
    'time_remaining': 0,
}

def run_countdown(duration):
    timer_info['running'] = True
    timer_info['time_remaining'] = duration
    while timer_info['time_remaining'] > 0:
        time.sleep(1)
        timer_info['time_remaining'] -= 1
    timer_info['running'] = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    duration = int(request.form['time'])
    thread = Thread(target=run_countdown, args=(duration,))
    thread.start()
    return jsonify(status='Timer started!')

@app.route('/get_time')
def get_time():
    if timer_info['running']:
        minutes, seconds = divmod(timer_info['time_remaining'], 60)
        timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
        return jsonify(time=timeformat)
    else:
        return jsonify(time="Time's up!", done=True)

if __name__ == '__main__':
    app.run(debug=True)
