from agent import agents as ag
from tqdm import tqdm
from params import *
from lstm.lstm import LSTM
import matplotlib.pyplot as plt
import qtable.qagent as qag
import qtable.qlearn as ql
import numpy as np
import torch.nn.functional as nnf
import pickle

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'
color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

class Game():
    def __init__(self, agents_config):
        self.agents = ag.Agents(agents_config) # The agents to play against in the tournament
        self.lstm = LSTM(IN, LSTM_HIDDEN, OUT, len(self.agents.agents), LSTM_LAYERS, LSTM_LR, DEVICE)
        self.q_agents = {}
        for agent in self.agents.agents:
            self.q_agents[agent.id()] = qag.QAgent(lr = QTABLE_LR, 
                discount=QTABLE_DISCOUNT, epsilon=QTABLE_EPSILON_TRAIN, 
                decay_rate=QTABLE_DECAY_RATE, min_e=QTABLE_MIN_EPSILON, memory=QTABLE_MEMORY)

    def train_all(self):
        self.train_lstm()
        self.train_qtables()

    def train_lstm(self):
        print("Training LSTM")
        self.lstm.pretrain(self.agents, LSTM_PRETRAIN_BATCH_SIZE, 
            LSTM_PRETRAIN_EPOCHS, TEST_ROUNDS, LSTM_PRETRAIN_SAMPLE_SIZE)

    def train_qtables(self):
        print("Training QTables")
        for agent in self.agents.agents:
            ql.train(self.q_agents[agent.id()], agent, QTABLE_TRAIN_EPOCHS, TEST_ROUNDS, REWARD)

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
        self.visualize_lstm_accuracy(accuracy_file)
        for agent in self.agents.agents:
            confidence_file = f'lstm/visuals/confidence/{fname}_{agent.name}.png'
            self.visualize_lstm_confidence(agent, confidence_file)

    def play(self):
        print("Playing Game")
        self.lstm.eval()
        accuracies = {}
        for epoch in range(TEST_EPOCHS):
            print("EPOCH %d" % epoch)
            errors = 0
            total_reward = 0
            for i in tqdm(range(TEST_GAMES)):
                agent = self.agents.get_random_agent_in_tournament()
                reward, error = self._play_one_game(agent, TEST_ROUNDS)
                errors += error
                total_reward += reward
                agent.reset()

            frac = (TEST_GAMES-errors)/TEST_GAMES
            print("Prediction Accuracy: %.2f" % frac)
            print(f"Total Reward: {total_reward}")
            print(f"Average Reward per Game: {total_reward/TEST_GAMES}")
            print(f"Average Reward per Round: {total_reward/(TEST_GAMES*TEST_ROUNDS)}")

    def _play_one_game(self, agent, rounds):
        """Plays a single game against an agent, comprised of ROUNDS iterations"""
        prev_agent_choice = 0 # This should probably get replaced (assume cooperate first)
        prev_agent_moves = []
        prev_nn_moves = []
        reward = 0
        input = self.lstm.build_input_vector(prev_agent_choice)
        id = self.lstm.build_id_vector(agent)
        # Play ROUNDS iterations of the prisoners dilemma against the same agent
        for _ in range(rounds):
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

    def visualize_lstm_accuracy(self, save_path, defect_first_ids = [], max_length = 20) :
        self.lstm.eval()
        accuracies = {}
        print("Beginning Accuracy Evaluation")
        for length in range(1, max_length+1):
            errors = 0
            for game in tqdm(range(TEST_GAMES)):
                agent = self.agents.get_random_agent()
                reward, error = self._play_one_game(agent, length) 
                errors += error
                agent.reset()

            frac = (TEST_GAMES-errors)/TEST_GAMES
            print("Prediction Accuracy with Length %s: %.2f" %(length, frac))
            accuracies[length] = frac

        x = list(accuracies.keys())
        y = list(accuracies.values())
        plt.plot(x, y, 'o-')
        plt.ylim([0,1])
        plt.xlim([0, max_length+1])
        plt.grid()
        plt.xlabel("Number of Rounds Played")
        plt.ylabel("Prediction Accuracy")
        plt.title("Rounds vs Accuracy")
        plt.savefig(save_path, dpi = 200)
        plt.show()

    def visualize_lstm_confidence(self, agent, save_path, max_length=20):
        self.lstm.eval()
        confidences = []
        print("Beginning Confidence Evaluation")
        input = self.lstm.build_input_vector(agent.play())
        for i in range(1, max_length+1):
            pred_id, id_logits = self.lstm.predict_id(input, agent)
            nn_action = np.random.randint(2)
            agent_action = int(agent.play())
            input = self.lstm.rebuild_input(nn_action, agent_action, input[0])
            agent.update(nn_action)

            probs = torch.softmax(id_logits.squeeze().detach().cpu(), dim=0)
            confidences.append(probs.numpy())

        predicted_id = id_logits.argmax(dim=-1).item()
        print("The Predicted ID is: %d" % predicted_id)

        confidences = np.array(confidences)
        plt.figure()
        for i in range(confidences.shape[1]):
            plt.plot(confidences[:, i], label = "Agent %d" % i)
            plt.ylim([0,1])
            plt.legend()
            plt.grid()
            plt.xlabel("Rounds Played")
            plt.ylabel("Predicted Probability of Each Agent")
            plt.title("Network Confidence")
            plt.savefig(save_path, dpi = 200)
        plt.show()