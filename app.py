import flask
from flask import request, jsonify, render_template, blueprints

import apps.deacon_ai.app as deacon_ai
import apps.mac.app as mac


app = flask.Flask(__name__)

app.register_blueprint(deacon_ai.bp, url_prefix='/deacon_ai')
app.register_blueprint(mac.bp, url_prefix='/mac')

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()