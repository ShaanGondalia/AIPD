from agent import agents as ag
from lstm.lstm import LSTM
from lstm.hyper_parameters import *
from lstm.visualize import visualize_model_accuracy, visualize_model_confidence
import qtable.hyper_parameters as qhp
import qtable.qagent as qag
import qtable.qlearn as ql
from tqdm import tqdm
import numpy as np
import torch.nn.functional as nnf
import pickle


class Game():
    def __init__(self, agents_config):
        self.agents = ag.Agents(agents_config) # The agents to play against in the tournament
        self.lstm = LSTM(IN, HIDDEN, OUT, len(self.agents.agents), LAYERS)
        self.q_agents = {}
        for agent in self.agents.agents:
            self.q_agents[agent.id()] = qag.QAgent(lr = qhp.LR, 
                discount = qhp.DISCOUNT, epsilon=qhp.EPSILON_TRAIN, 
                decay_rate=qhp.DECAY_RATE, min_e=qhp.MIN_EPSILON, memory=qhp.MEMORY)

    def train_all(self):
        self.train_lstm()
        self.train_qtables()

    def train_lstm(self):
        print("Training LSTM")
        self.lstm.pretrain(self.agents)

    def train_qtables(self):
        print("Training QTables")
        for agent in self.agents.agents:
            ql.train(self.q_agents[agent.id()], agent)

    def save_all(self, fname):
        self.save_lstm(fname)
        self.save_qtables(fname)

    def save_lstm(self, fname):
        print(f"Saving LSTM to file: lstm/models/{fname}.pth")
        self.lstm.save(fname)

    def save_qtables(self, fname):
        print(f"Saving Qtables to file: qtable/models/{fname}.pickle")
        with open(f'qtable/models/{fname}.pickle', 'wb') as handle:
            pickle.dump(self.q_agents, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, fname):
        print(f"Loading Models from file: {fname}")
        self.lstm.load(fname)
        with open(f'qtable/models/{fname}.pickle', 'rb') as handle:
            self.q_agents = pickle.load(handle)

    def visualize_lstm(self, fname):
        accuracy_file = f'lstm/visuals/accuracy/{fname}.png'
        visualize_model_accuracy(self.lstm, self.agents.agents, accuracy_file)
        for agent in self.agents.agents:
            confidence_file = f'lstm/visuals/confidence/{fname}_{agent.name}.png'
            visualize_model_confidence(self.lstm, agent, agent.play(), 20, confidence_file)

    def play(self):
        print("Playing Game")
        self.lstm.eval()
        accuracies = {}
        for epoch in range(EPOCHS):
            print("EPOCH %d" % epoch)
            errors = 0
            total_reward = 0
            for i in tqdm(range(GAMES)):
                agent = self.agents.get_random_agent_in_tournament()
                reward, error = self._play_one_game(agent)
                errors += error
                total_reward += reward
                agent.reset()

            frac = (GAMES-errors)/GAMES
            print("Prediction Accuracy: %.2f" % frac)
            print(f"Total Reward: {total_reward}")
            print(f"Average Reward per Game: {total_reward/GAMES}")
            print(f"Average Reward per Round: {total_reward/(GAMES*ROUNDS)}")

    def _play_one_game(self, agent):
        """Plays a single game against an agent, comprised of ROUNDS iterations"""
        prev_agent_choice = 0 # This should probably get replaced (assume cooperate first)
        prev_agent_moves = []
        prev_nn_moves = []
        reward = 0
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
            reward += ql.get_reward(nn_action, agent_action)[0]
        # self.lstm.learn(id_logits, id)

        return reward, 0 if pred_id == agent.id() else 1