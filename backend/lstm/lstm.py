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

    def build_input_vector(self, prev_agent_choice):
        """Creates NN input vector"""
        input = [0, 0]
        input[1] = prev_agent_choice
        return torch.Tensor(input).to(self.device).unsqueeze(0).unsqueeze(0)

    def build_id_vector(self, agent):
        """Find id of agent (another input to NN for regularization)"""
        id = [agent.id()]
        id = torch.Tensor(id).to(self.device)
        return id.to(torch.int64)

    def rebuild_input(self, nn_action, opp_action, prev_input):
        curr_input = [0, 0]
        curr_input[0] = nn_action
        curr_input[1] = opp_action
        curr_input = torch.Tensor(curr_input).to(self.device).unsqueeze(0)
        return torch.cat([prev_input, curr_input]).unsqueeze(0)