#!flask/bin/python
from flask import Flask, jsonify, abort, request, url_for, render_template
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

rasps = [
    {
        'id': 1,
        'address':
            {
                'ip': '172.0.0.1',
                'mac': '00:EF:4G:00:45:OP'
            },
        'status':
            {
                'cpu': '22',
                'power': 'On'
            },
        'position':
            {
                'stack': '2',
                'level': '4'
            }
    },
    {
        'id': 2,
        'address':
            {
                'ip': '172.0.0.2',
                'mac': '00:EF:4B:00:43:OP'
            },
        'status':
            {
                'cpu': '50',
                'power': 'Off'
            },
        'position':
            {
                'stack': '2',
                'level': '5'
            }
    },
    {
        'id': 3,
        'address':
            {
                'ip': '172.0.0.3',
                'mac': '00:43:4G:00:45:OP'
            },
        'status':
            {
                'cpu': '22',
                'power': 'On'
            },
        'position':
            {
                'stack': '2',
                'level': '6'
            }
    }
]

@app.route('/api/v1.0/rasps', methods=['GET'])
def get_rasps():
    return jsonify({'rasps': [make_public_rasp(rasp) for rasp in rasps]})

@app.route('/api/v1.0/rasps/<int:rasp_id>', methods=['GET'])
def get_rasp(rasp_id):
    rasp = [rasp for rasp in rasps if rasp['id'] == rasp_id]
    if len(rasp) == 0:
        abort(404)
    return jsonify({'rasp': make_public_rasp(rasp[0])})

@app.route('/api/v1.0/rasps', methods=['POST'])
def create_rasp():
    requestRasp = request.json
    print(requestRasp)
    rasp = {
        'id': rasps[-1]['id'] + 1,
        'address':
            {
                'ip':requestRasp["address"]["ip"],
                'mac':requestRasp["address"]["mac"],
            },
        'status':
            {
                'cpu':requestRasp["status"]["cpu"],
                'power':requestRasp["status"]["power"]
            },
        'position':
            {
                'stack':requestRasp["position"]["stack"],
                'level':requestRasp["position"]["level"]
            }
    }
    rasps.append(rasp)
    return jsonify({'rasp': rasp}), 201

@app.route('/api/v1.0/rasps/<int:rasp_id>', methods=['PUT'])
def update_rasp(rasp_id):
    rasp = [rasp for rasp in rasps if rasp['id'] == rasp_id]
    if len(rasp) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    rasp[0]['title'] = request.json.get('title', rasp[0]['title'])
    rasp[0]['description'] = request.json.get('description', rasp[0]['description'])
    rasp[0]['done'] = request.json.get('done', rasp[0]['done'])
    return jsonify({'rasp': rasp[0]})

@app.route('/api/v1.0/rasps/<int:rasp_id>', methods=['DELETE'])
def delete_rasp(rasp_id):
    rasp = [rasp for rasp in rasps if rasp['id'] == rasp_id]
    if len(rasp) == 0:
        abort(404)
    rasps.remove(rasp[0])
    return jsonify({'result': True})

def make_public_rasp(rasp):
    new_rasp = {}
    for field in rasp:
        if field == 'id':
            new_rasp['uri'] = url_for('get_rasp', rasp_id=rasp['id'], _external=True)
        new_rasp[field] = rasp[field]
    return new_rasp

if __name__ == '__main__':
    app.run(port=5000,debug=True)
