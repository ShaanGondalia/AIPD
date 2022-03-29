from agent import agents as ag
from lstm.lstm import LSTM
from lstm.hyper_parameters import *
import qtable.hyper_parameters as qhp
import qtable.qagent as qag
import qtable.qlearn as ql
from tqdm import tqdm
import numpy as np
import torch.nn.functional as nnf
import pickle


class Game():
    def __init__(self):
        self.lstm = LSTM(IN, HIDDEN, OUT, ID, LAYERS)
        self.agents = ag.Agents() # The agents to play against in the tournament
        self.q_agents = {}
        for agent in self.agents.agents:
            self.q_agents[agent.id()] = qag.QAgent(lr = qhp.LR, 
                discount = qhp.DISCOUNT, epsilon=qhp.EPSILON_TRAIN, 
                decay_rate=qhp.DECAY_RATE, min_e=qhp.MIN_EPSILON, memory=qhp.MEMORY)

    def train(self):
        print("Training LSTM")
        self.lstm.train()
        self.lstm.pretrain(self.agents)
        print("Training QTables")
        for agent in self.agents.agents:
            ql.train(self.q_agents[agent.id()], agent)

    def save(self, fname):
        print(f"Saving Models to file: {fname}")
        self.lstm.save(fname)
        with open(f'qtable/models/{fname}.pickle', 'wb') as handle:
            pickle.dump(self.q_agents, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, fname):
        print(f"Loading Models from file: {fname}")
        self.lstm.load(fname)
        with open(f'qtable/models/{fname}.pickle', 'rb') as handle:
            self.q_agents = pickle.load(handle)

    def play(self):
        print("Playing Game")
        self.lstm.eval()
        for epoch in range(EPOCHS):
            print("EPOCH %d" % epoch)
            errors = 0
            for i in tqdm(range(GAMES)):
                agent = self.agents.get_random_agent()
                errors += self._play_one_game(agent)
                agent.reset()

            frac = (GAMES-errors)/GAMES
            print("Prediction Accuracy: %.2f" % frac)

    def _play_one_game(self, agent):
        """Plays a single game against an agent, comprised of ROUNDS iterations"""
        prev_agent_choice = agent.play()
        prev_agent_moves = []
        prev_nn_moves = []
        input = self.lstm.build_input_vector(prev_agent_choice)
        id = self.lstm.build_id_vector(agent)
        # Play ROUNDS iterations of the prisoners dilemma against the same agent
        for _ in range(ROUNDS):
            prev_moves = np.array([prev_nn_moves, prev_agent_moves]).T
            pred_id, id_logits = self.lstm.predict_id(input, agent)
            probs = nnf.softmax(id_logits, dim=1).detach().cpu().numpy()
            agent_action = int(agent.play())
            # TODO: Implement Linear combination of results here
            nn_action = self.q_agents[pred_id].pick_action(prev_moves, False)
            input = self.lstm.rebuild_input(nn_action, agent_action, input[0])
            agent.update(nn_action)
            prev_agent_moves.append(agent_action)
            prev_nn_moves.append(nn_action)
        # self.lstm.learn(id_logits, id)

        return 0 if pred_id == agent.id() else 1