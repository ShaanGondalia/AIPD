from lstm import LSTM
from dataset import PreTrainDataset
import hyper_parameters as hp

def main():
	dataset = PreTrainDataset()
	model = LSTM(hp.IN, hp.HIDDEN, hp.OUT, hp.ID, hp.LAYERS)
	model.pretrain(dataset)
	model.learn()

if __name__ == "__main__":
	main()
