import argparse
from game import Game


AGENT_HELP = 'Filename to load agent configuration from.'
MODELS_HELP = 'Models to train (qtable, lstm, or all).'
MODEL_CHOICES = ['qtable', 'lstm', 'all']

def main(args):
	game = Game(args['agents'])
	if args['train']:
		if args['models'] == 'qtable':
			game.train_qtables()
			game.save_qtables(args['save'])    
		elif args['models'] == 'lstm':
			game.train_lstm()
			game.save_lstm(args['save'])
		else:
			game.train_all()
			game.save_all(args['save'])
	else:
		game.load(args['load'])
		if args['visualize']:
			game.visualize_lstm(args['load'])
		game.play()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--agents', help=AGENT_HELP, type=argparse.FileType('r'), required=True)
	parser.add_argument('-t', '--train', help='Flag to train LSTM', action='store_true')
	parser.add_argument('-v', '--visualize', help='Enables Visualizations', action='store_true')
	opts, rem_args = parser.parse_known_args()
	if opts.train:
		parser.add_argument('-s', '--save', help='Filename to save LSTM after training', required=True, type=str)
		parser.add_argument('-m', '--models', help=MODELS_HELP, default='all', 
			const='all', nargs='?', choices=MODEL_CHOICES)
	else:
		parser.add_argument('-l', '--load', help='Filename to load LSTM', required=True, type=str)
	args = vars(parser.parse_args())

	main(args)

