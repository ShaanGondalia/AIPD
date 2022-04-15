from flask import Flask, request
from flask_cors import CORS
from models import MiniAgent

app = Flask(__name__)
CORS(app)
agent = MiniAgent("default")

def validate_moves(moves):
    valid_moves = set([0, 1])
    if not isinstance(moves, list):
        return False
    for move in valid_moves:
        if move not in valid_moves:
            return False
    return True


@app.route('/play', methods=['POST'])
def get_agent_move():

    user_moves = request.json.get('user_moves')
    agent_moves = request.json.get('agent_moves')

    if len(user_moves) == 0 and len(agent_moves) == 0:
        return {'agent_decision': 0}, 200

    if len(user_moves) != len(agent_moves):
        return {'message': 'user and agent history not the same length'}, 400

    if not validate_moves(user_moves):
        return {'message': 'invalid user moves'}, 400

    if not validate_moves(agent_moves):
        return {'message': 'invalid agent moves'}, 400

    agent_decision = agent.action(agent_moves, user_moves)

    return {'agent_decision' : agent_decision}, 200

