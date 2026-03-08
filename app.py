import flask
from flask import request, jsonify, render_template, blueprints

"""
from apps.deacon_ai.app import bp as deacon_ai_bp
from apps.mac.app import bp as mac_bp
"""

app = flask.Flask(__name__)

"""
app.register_blueprint(deacon_ai.bp, url_prefix='/deacon_ai')
app.register_blueprint(mac.bp, url_prefix='/mac')
"""

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)