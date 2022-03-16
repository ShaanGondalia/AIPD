from lstm.lstm import LSTM
from lstm.dataset import PreTrainDataset
from lstm.hyper_parameters import *
from tqdm import tqdm
from agent import agents as ag


class Game():
	def __init__(self):
		self.dataset = PreTrainDataset()
		self.model = LSTM(IN, HIDDEN, OUT, ID, LAYERS)
		self.model.pretrain(self.dataset)

	def play(self):
		agents = ag.Agents() # The agents to play against in the tournament

		for epoch in range(EPOCHS):
			print("EPOCH %d" % epoch)
			errors = 0
			for i in tqdm(range(GAMES)):
				agent = agents.get_random_agent()
				errors += self._play_one_game(agent)

		frac = (GAMES-errors)/GAMES
		print("Prediction Accuracy: %.2f" % frac)

	def _play_one_game(self, agent):
		"""Plays a single game against an agent, comprised of ROUNDS iterations"""
		prev_agent_choice = agent.previous()
		input = self.model.build_input_vector(prev_agent_choice)
		id = self.model.build_id_vector(agent)
		# Play ROUNDS iterations of the prisoners dilemma against the same agent
		for _ in range(ROUNDS):
			pred_id, id_logits = self.model.predict_id(input, agent, id)
			# TODO: Implement Q Table here
			nn_action = agent.opt() # Currently make the optimal move
			agent_action = int(agent.play())
			input = self.model.learn(nn_action, agent_action, input[0], id_logits, id)
			agent.update(nn_action)

		if pred_id != agent.id():
		  	return 1

		return 0


def main():
	game = Game()
	game.play()

if __name__ == "__main__":
	main()
