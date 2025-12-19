from flask import Flask,jsonify,abort,render_template,request
import json

app = Flask(__name__)

welcome = "Welcome to 3ESE API!"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/')
def hello_world():
	return 'Hello, World!\n'
@app.route('/api/welcome/', methods=['GET', 'POST', 'DELETE'])
def api_welcome():
    global welcome
    if request.method == 'GET':
        return jsonify({"val": welcome})
    elif request.method == 'POST':
        new_welcome_data = request.get_json()
        if new_welcome_data and 'message' in new_welcome_data:
            welcome = new_welcome_data['message']
            return '', 202 # No Content
        else:
            abort(400, description="Invalid data for POST: 'message' field is required.")
    elif request.method == 'DELETE':
        welcome = ""
        return '', 202 # No Content

@app.route('/api/welcome/<int:index>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_welcome_index(index):
    global welcome
    if index < 0 or index >= len(welcome):
        abort(404, description=f"Index {index} is out of bounds for welcome message of length {len(welcome)}.")

    if request.method == 'GET':
        return jsonify({"index": index, "val": welcome[index]})
    elif request.method == 'PUT':
        new_word_data = request.get_json()
        if new_word_data and 'word' in new_word_data:
            word_to_insert = new_word_data['word']
            welcome = welcome[:index] + word_to_insert + welcome[index:]
            return '', 202 # No Content
        else:
            abort(400, description="Invalid data for PUT: 'word' field is required.")
    elif request.method == 'PATCH':
        new_char_data = request.get_json()
        if new_char_data and 'char' in new_char_data and len(new_char_data['char']) == 1:
            char_to_change = new_char_data['char']
            welcome_list = list(welcome)
            welcome_list[index] = char_to_change
            welcome = "".join(welcome_list)
            return '', 202 # No Content
        else:
            abort(400, description="Invalid data for PATCH: 'char' field with single character is required.")
    elif request.method == 'DELETE':
        welcome = welcome[:index] + welcome[index+1:]
        return '', 202 # No Content

@app.route('/api/request/', methods=['GET', 'POST'])
@app.route('/api/request/<path>', methods=['GET','POST'])
def api_request(path=None):
    resp = {
            "method":   request.method,
            "url" :  request.url,
            "path" : path,
            "args": request.args,
            "headers": dict(request.headers),
    }
    if request.method == 'POST':
        resp["POST"] = {
                "data" : request.get_json(),
                }
    return jsonify(resp)
