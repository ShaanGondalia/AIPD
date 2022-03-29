import argparse
from game import Game


def main(args):
    game = Game()
    if args['train']:
        game.train()
        game.save(args['save'])    
    else:
        game.load(args['load'])
        game.play()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--train', help='Flag to train LSTM', type=bool)
	opts, rem_args = parser.parse_known_args()
	if opts.train:
		parser.add_argument('-s', '--save', help='Filename to save LSTM after training', required=True, type=str)
	else:
		parser.add_argument('-l', '--load', help='Filename to load LSTM', required=True, type=str)
	args = vars(parser.parse_args())

	main(args)

