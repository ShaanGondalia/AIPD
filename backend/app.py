from flask import Flask, request
from flask_cors import CORS
from models import AIAgent, Tournament
import base64

app = Flask(__name__)
CORS(app)
agent = AIAgent("default")

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

@app.route('/tournament', methods=['POST'])
def get_tournament_visual():

    generations = request.json.get('generations')
    interactions = request.json.get('interactions')
    rounds = request.json.get('rounds')
    reproduction_rate = request.json.get('reproduction_rate')
    config = request.json.get('config')

    if 'agents' not in config:
        return {'message': 'config is not properly formatted'}, 400
    if type(generations) != int:
        return {'message': 'generations must be a number'}, 400
    if type(interactions) != int:
        return {'message': 'interactions must be a number'}, 400
    if type(rounds) != int:
        return {'message': 'rounds must be a number'}, 400
    if type(reproduction_rate) != float or reproduction_rate > 1 or reproduction_rate <= 0:
        return {'message': 'reproduction rate must be decimal between 0 and 1'}, 400

    tournament = Tournament(generations, interactions, rounds, reproduction_rate, config)
    buffer = tournament.tournament()
    gif_base64 = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return {'gif': gif_base64}, 200