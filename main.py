import argparse
from game import Game


def main(args):
	game = Game(args['train'])
	game.play()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--train', help='Flag to train LSTM and QTable', nargs='?', const=False, type=bool)
	args = vars(parser.parse_args())

	main(args)

