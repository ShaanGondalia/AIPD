import torch
import torch.nn as nn

class LSTM(nn.Module):

    def __init__(self, in_dim, hidden_dim, out_dim, id_dim, layer_num, device):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden_dim, layer_num, batch_first=True)
        self.relu = nn.ReLU()
        self.id_fc = nn.Linear(hidden_dim, id_dim)
        self.device = device
        self.to(device)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.relu(out)
        out = self.id_fc(out)
        return out

    def predict_id(self, input):
        out = self(input)
        id_logits = out[:, -1, :]
        pred_id = id_logits.argmax(dim=-1)
        return pred_id.item(), id_logits

    def load(self, fname):
        state_dict = torch.load(f"saved/{fname}.pth", map_location=torch.device('cpu'))
        self.load_state_dict(state_dict)
        self.to(self.device)