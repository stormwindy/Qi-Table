from flask import Flask, escape, request, render_template, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__, template_folder="")
CORS(app)

DATABASE = 'layouts.db'

@app.route('/move', methods=['POST'])
def move():
    #print(request.json['layoutID'])
    print("Move requested into layout " + str(request.json['layoutID']))
    return {"text": "Moving"}