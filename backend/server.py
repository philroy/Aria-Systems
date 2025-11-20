from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from ai_engine import AriaAI

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
socketio = SocketIO(app, host='0.0.0.0, port=8080')

aria = AriaAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_panel')
def ai_panel():
    return render_template('ai_panel.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')
    output = aria.execute_code(code)
    return jsonify({'output': output})

@socketio.on('message')
def handle_message(msg):
    response = aria.chat(msg)
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
