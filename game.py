from lstm.lstm import LSTM
from lstm.hyper_parameters import *
from tqdm import tqdm
from agent import agents as ag

class Game():
	def __init__(self, train, load, save):
		self.lstm = LSTM(IN, HIDDEN, OUT, ID, LAYERS)
		self.train = train
		self.load = load
		self.save = save
		self.agents = ag.Agents() # The agents to play against in the tournament
		if self.train:
			self.lstm.train()
			if not self.load:
				self.lstm.pretrain(self.agents)
		else:
			self.lstm.eval()
		if self.load:
			self.lstm.load(self.load)

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
		if self.save:
			self.lstm.save(self.save)

	def _play_one_game(self, agent):
		"""Plays a single game against an agent, comprised of ROUNDS iterations"""
		prev_agent_choice = agent.play()
		input = self.lstm.build_input_vector(prev_agent_choice)
		id = self.lstm.build_id_vector(agent)
		# Play ROUNDS iterations of the prisoners dilemma against the same agent
		for _ in range(ROUNDS):
			pred_id, id_logits = self.lstm.predict_id(input, agent, id)
			# TODO: Implement Q Table here
			nn_action = agent.opt() # Currently make the optimal move
			agent_action = int(agent.play())
			input = self.lstm.rebuild_input(nn_action, agent_action, input[0])
			agent.update(nn_action)
		# self.lstm.learn(id_logits, id)

		return 0 if pred_id == agent.id() else 1