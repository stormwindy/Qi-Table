from flask import Flask, escape, request, render_template, jsonify, make_response

app = Flask(__name__, template_folder="")

@app.route('/move', methods=['POST'])
def move():
    print(request.form)
    return make_response("Moving...")