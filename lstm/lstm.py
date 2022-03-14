import sys,os
sys.path.append(os.getcwd())

import torch
import torch.nn as nn
import torch.optim as optim
import hyper_parameters as hp
import numpy as np
from torch.utils.data import DataLoader
from tqdm import tqdm
from agent import tournament


class LSTM(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, id_dim, layer_num):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden_dim, layer_num, batch_first=True)
        self.relu = nn.ReLU()
        self.id_fc = nn.Linear(hidden_dim, id_dim)
        self.optimizer = None
        self.criterion = None

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.relu(out)
        out = self.id_fc(out)
        return out

    def pretrain(self, dataset):
        dataloader = DataLoader(dataset, batch_size = hp.BATCH_SIZE)
        self.apply(_initialize_weights)
        self.to(hp.DEVICE)
        self.train()

        self.optimizer = optim.Adam(self.parameters(), lr=hp.LR)
        self.criterion = nn.CrossEntropyLoss()
        self.criterion = self.criterion.to(hp.DEVICE)

        for epoch in range(hp.EPOCHS):
            epoch_accs = []
            for batch in tqdm(dataloader):
                self._train_batch(batch, epoch_accs)
            print(np.mean(epoch_accs))

    def learn(self):
        #Train with Regularization
        tment = tournament.Tournament()

        for epoch in range(hp.EPOCHS):
          print("EPOCH %d" % epoch)
          errors = 0
          for i in tqdm(range(hp.GAMES)):

            agent = tment.get_random_agent()
            prev_agent_choice = agent.previous()

            input = [0, 0]
            input[1] = prev_agent_choice
            input = torch.Tensor(input).to(hp.DEVICE).unsqueeze(0).unsqueeze(0)

            id = [agent.id()]
            id = torch.Tensor(id).to(hp.DEVICE)
            id = id.to(torch.int64)

            for _ in range(hp.ROUNDS):

                out = self(input)
                id_logits = out[:, -1, :]
                pred_id = id_logits.argmax(dim=-1)
                pred_id = pred_id.item()

                # TODO: Implement Q Table here
                nn_action = agent.opt()
                agent_action = int(agent.play())

                curr_input = [0, 0]

                curr_input[0] = nn_action
                curr_input[1] = agent_action
                curr_input = torch.Tensor(curr_input).to(hp.DEVICE).unsqueeze(0)
                prev_input = input[0]
                input = torch.cat([prev_input, curr_input]).unsqueeze(0)

                agent.update(nn_action)

                id_loss = self.criterion(id_logits, id)
                id_loss.backward()
                self.optimizer.step()

            predicted_id = id_logits.argmax(dim=-1).item()
            if predicted_id != agent.id():
              errors += 1

          frac = (hp.GAMES-errors)/hp.GAMES
          print("Prediction Accuracy: %.2f" % frac)

    def _train_batch(self, batch, epoch_accs):
        input = batch["input"].type(torch.FloatTensor).to(hp.DEVICE)
        output = batch["output"].to(hp.DEVICE)
        pred = self(input)
        pred_logits = pred[:, -1, :]
        loss = self.criterion(pred_logits, output)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        accuracy = _get_accuracy(pred_logits, output)
        epoch_accs.append(accuracy.item())

def _get_accuracy(prediction, label):
    batch_size, _ = prediction.shape
    predicted_classes = prediction.argmax(dim=-1)
    correct_predictions = predicted_classes.eq(label).sum()
    accuracy = correct_predictions / batch_size
    return accuracy

def _initialize_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_normal_(m.weight)
        nn.init.zeros_(m.bias)
    elif isinstance(m, nn.LSTM):
        for name, param in m.named_parameters():
            if 'bias' in name:
                nn.init.zeros_(param)
            elif 'weight' in name:
                nn.init.orthogonal_(param)