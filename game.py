from lstm.lstm import LSTM
from lstm.hyper_parameters import *
from tqdm import tqdm
import numpy as np
import torch.nn.functional as nnf
from agent import agents as ag


class Game():
    def __init__(self):
        self.lstm = LSTM(IN, HIDDEN, OUT, ID, LAYERS)
        self.agents = ag.Agents() # The agents to play against in the tournament

    def train(self):
        self.lstm.train()
        self.lstm.pretrain(self.agents)

    def save(self, fname):
        self.lstm.save(fname)

    def load(self, fname):
        self.lstm.load(fname)

    def play(self):
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
        input = self.lstm.build_input_vector(prev_agent_choice)
        id = self.lstm.build_id_vector(agent)
        # Play ROUNDS iterations of the prisoners dilemma against the same agent
        for _ in range(ROUNDS):
            pred_id, id_logits = self.lstm.predict_id(input, agent)
            # TODO: Implement Q Table here
            probs = nnf.softmax(id_logits, dim=1)
            # nn_action = agent.opt() # Make the optimal move
            nn_action = np.random.choice([0,1]) # Make a random move
            agent_action = int(agent.play())
            input = self.lstm.rebuild_input(nn_action, agent_action, input[0])
            agent.update(nn_action)
        # self.lstm.learn(id_logits, id)

        return 0 if pred_id == agent.id() else 1