from flask import Flask, g, escape, request, render_template, jsonify, make_response
from flask_cors import CORS
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../'))
from server import BaseComms
#from server.BaseComms import goForward, goBackward, goLeft, goRight


app = Flask(__name__, template_folder="")
CORS(app)

DATABASE = 'layouts.db'

#adapted from the flask website
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

    db.row_factory = make_dicts
    
    return db

#adapted from the flask website
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(sql, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    return cur.lastrowid


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/move', methods=['POST'])
def move():
    print("Move requested into layout " + str(request.json['id']))
    return {"text": "Moving"}

@app.route('/addlayout', methods=['POST'])
def add_layout():
    print(request.json)

    #find next available id
    highest_id = 0
    for layout in query_db('select * from layouts'):
        if layout['id']>highest_id :
            highest_id = layout['id']

    id = highest_id+1
    #insert into layouts
    insert_db('insert into layouts (id, name) values (?,?)', (id, request.json['name']))
    print('Inserted layout ' + request.json['name'] + ' with id ' + str(id))
    #insert into positions
    for pos in request.json['positions']:
        insert_db ('insert into positions (layoutid, x, y, rotation) values (?,?,?,?)', (id, pos['x'], pos['y'], pos['r']))
    
    print('Inserted positions')

    return {"text": "Added layout " + str(request.json['name']) + ' with id ' + str(id)}

@app.route('/getlayouts', methods=['GET'])
def get_layouts():

    #sql query the layouts
    layouts = query_db('select * from layouts')
    print(layouts)

    #format into json
    for l in layouts:
        print(l['id'])
        l['positions'] = []
        for pos in query_db('select * from positions where layoutid = ?', (l['id'],)):
            l['positions'].append({'x' : pos['x'], 'y' : pos['y'], 'rotation' : pos['rotation']})
    
    layouts = {'layouts' : layouts}
    
    #{layouts: [{id: 1, name: 'abc', positions: [{x:0,y:0,r:0}, ] },  ]}
    print(layouts)

    #send response
    return layouts

@app.route('/demo', methods=['GET'])
def demo():

    print(request.headers)

    bc = BaseComms.BaseComms()
    if request.headers['Direction']=='forwards':
        print('Moving forwards')
        
        bc.goForward()
        return {'text': 'Moving forwards'}
    
    if request.headers['Direction']=='backwards':
        print('Moving backwards')
        
        bc.goBackward()
        return {'text': 'Moving backwards'}
    
    if request.headers['Direction']=='left':
        print('Turning left')
        
        bc.turnLeft()
        return {'text': 'Turning left'}
    
    if request.headers['Direction']=='right':
        print('Turning right')
        
        bc.turnRight()
        return {'text': 'Turning right'}
    
    if request.headers['Direction']=='stop':
        bc.stop()
        return {'text': 'Stop'}


    return {'text': 'Error: invalid header'}

@app.route('/demopathfinding', methods=['GET'])
def demo_pathfinding():
    #get target coordinates from headers
    x = request.headers['x']
    y = request.headers['y']

    #MOVE TO TARGET HERE
    #robot.moveToTarget(x,y)
    #or something like that

    return {'text': 'Moving to position x: ' + str(x) + ' y: ' + str(y)}
    


