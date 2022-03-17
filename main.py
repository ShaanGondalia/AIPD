import argparse
from game import Game


def main(args):
	game = Game(args['train'], args['load'], args['save'])
	game.play()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--train', help='Flag to train LSTM', nargs='?', const=False, type=bool)
	parser.add_argument('-l', '--load', help='Filename to load LSTM', nargs='?', const="default", type=str)
	parser.add_argument('-s', '--save', help='Filename to save LSTM', nargs='?', const=None, type=str)
	args = vars(parser.parse_args())

	main(args)

