from .base_agent import BaseAgent
import sys
sys.path.append("..") # TODO: Remove this
from params import *
from lstm.lstm import LSTM
import pickle
import numpy as np
import torch.nn.functional as nnf


class AIAgent(BaseAgent):

	def __init__(self, name, id, id_dim, load_fname):
		super().__init__(id)
		self.lstm = LSTM(IN, LSTM_HIDDEN, OUT, id_dim, LSTM_LAYERS, LSTM_LR, DEVICE)
		self.q_tables = {}
		self.load(load_fname)
		self.name = name
		self.reset()

	def load(self, fname):
		print(f"Loading Models from file: {fname}")
		self.lstm.load(fname)
		with open(f'qtable/models/{fname}.pickle', 'rb') as handle:
			self.q_agents = pickle.load(handle)

	def update(self, opp_move):
		prev_moves = np.array([self.prev_nn_moves, self.prev_agent_moves]).T
		pred_id, id_logits = self.lstm.predict_id(self.input)
		probs = nnf.softmax(id_logits, dim=1).detach().cpu().numpy()
		# TODO: Implement Linear combination of results here
		self.val = self.q_agents[pred_id].pick_action(prev_moves, False)
		self.input = self.lstm.rebuild_input(self.val, opp_move, self.input[0])
		self.prev_agent_moves.append(opp_move)
		self.prev_nn_moves.append(self.val)

	def opt(self):
		# TODO: Fix this?
		return 0 if self.val==1 else 1

	def reset(self):
		prev_agent_choice = 0 # This should probably get replaced (assume cooperate first)
		self.prev_agent_moves = []
		self.prev_nn_moves = []
		self.input = self.lstm.build_input_vector(prev_agent_choice)
		self.val=0