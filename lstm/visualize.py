from tqdm import tqdm
import matplotlib.pyplot as plt
from .hyper_parameters import *
import numpy as np
import torch

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'
color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)


def visualize_model_accuracy(
    model, 
    agents, 
    save_path,
    defect_first_ids = [],
    max_length = 20,
    games = 100) :
    model.eval()
    accuracies = {}
    print("Beginning Evaluation")
    for length in range(1, max_length+1):
      errors = 0
      for game in tqdm(range(GAMES)):

        agent = np.random.choice(agents)
        agent_id = agent.id()
        prev_agent_choice = 1 if agent_id in defect_first_ids else 0
        input = [0,0]
        input[1] = prev_agent_choice
        input = torch.Tensor(input).to(DEVICE).unsqueeze(0).unsqueeze(0)
        id = [agent_id]
        id = torch.Tensor(id).to(DEVICE)
        id = id.to(torch.int64)

        for _ in range(length):
          out = model(input)
          id_logits = out[:, -1, :]
          pred_id = id_logits.argmax(dim=-1)
          pred_id = pred_id.item()

          nn_action = np.random.randint(2)
          agent_action = int(agent.play())

          curr_input = [0, 0]
          curr_input[0] = nn_action
          curr_input[1] = agent_action
          curr_input = torch.Tensor(curr_input).to(DEVICE).unsqueeze(0)

          prev_input = input[0]
          input = torch.cat([prev_input, curr_input]).unsqueeze(0)
          agent.update(nn_action)

        predicted_id = id_logits.argmax(dim=-1).item()
        if predicted_id != agent_id:
          errors += 1      
        agent.reset()

      frac = (GAMES-errors)/GAMES
      print("Prediction Accuracy with Length %s: %.2f" %(length, frac))
      accuracies[length] = frac

    x = list(accuracies.keys())
    y = list(accuracies.values())
    plt.plot(x, y, 'o-')
    plt.ylim([0,1])
    plt.xlim([0, max_length])
    plt.grid()
    plt.xlabel("Number of Rounds Played")
    plt.ylabel("Prediction Accuracy")
    plt.title("Rounds vs Accuracy")
    plt.savefig(save_path, dpi = 200)
    plt.show()

def visualize_model_confidence(
    model,
    opponent,
    opponent_first_move,
    max_length,
    save_path):
  
  model.eval()
  confidences = []
  print("Beginning Accuracy Evaluation")

  input = [0,0]
  input[1] = opponent_first_move
  input = torch.Tensor(input).to(DEVICE).unsqueeze(0).unsqueeze(0)
  for i in range(1, max_length+1):
    out = model(input)
    id_logits = out[:, -1, :]
    pred_id = id_logits.argmax(dim=-1)
    pred_id = pred_id.item()

    nn_action = np.random.randint(2)
    agent_action = int(opponent.play())

    curr_input = [0, 0]
    curr_input[0] = nn_action
    curr_input[1] = agent_action
    curr_input = torch.Tensor(curr_input).to(DEVICE).unsqueeze(0)

    prev_input = input[0]
    input = torch.cat([prev_input, curr_input]).unsqueeze(0)
    opponent.update(nn_action)

    probs = torch.softmax(id_logits.squeeze().detach().cpu(), dim=0)
    confidences.append(probs.numpy())
  
  predicted_id = id_logits.argmax(dim=-1).item()
  print("The Predicted ID is: %d" % predicted_id)

  confidences = np.array(confidences)
  plt.figure()
  for i in range(confidences.shape[1]):
    plt.plot(confidences[:, i], label = "Agent %d" % i)
  plt.ylim([0,1])
  plt.legend()
  plt.grid()
  plt.xlabel("Rounds Played")
  plt.ylabel("Predicted Probability of Each Agent")
  plt.title("Network Confidence")
  plt.savefig(save_path, dpi = 200)
  plt.show()


