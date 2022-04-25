import io
import random
import pickle
import math
import torch
import torch.nn as nn
import torch.nn.functional as nnf
import numpy as np
from matplotlib.figure import Figure
from PIL import Image
from lstm.lstm import LSTM

LSTM_HIDDEN = 200
LSTM_LAYERS = 4
IN = 2
OUT = 2
NUM_AGENTS = 4
DEVICE = 'cpu'
REWARD = [[2, 2], # Coop, Coop
          [0, 3], # Coop, Dfct
          [3, 0], # Dfct, Coop
          [1, 1]] # Dfct, Dfct

class BaseAgent:

  def __init__(self, i=-1):
    self.i = i
    self.val = 0

  def id(self):
    return self.i
  
  def update(self, val):
    pass

  def play(self):
    return self.val

  def reset(self):
    self.val = 0

class AIAgent(BaseAgent):
    
    def __init__(self, load_fname):
        self.lstm = LSTM(IN, LSTM_HIDDEN, OUT, NUM_AGENTS, LSTM_LAYERS, DEVICE)
        self.load(load_fname)
        self.reset()
        
    def load(self, fname):
        print(f"Loading Models from file: {fname}")
        self.lstm.load(fname)
        with open(f'saved/{fname}.pickle', 'rb') as handle:
            self.q_agents = pickle.load(handle)
        for i in range(NUM_AGENTS):
            self.q_agents[i].set_epsilon(-1)

    def action(self, agent_moves, opponent_moves):
        combined_moves = np.vstack([agent_moves, opponent_moves]).T
        input = torch.Tensor(combined_moves).type(torch.FloatTensor).to('cpu').unsqueeze(0)
        pred_id, _ = self.lstm.predict_id(input) 
        q_agent = self.q_agents[pred_id]
        action = q_agent.pick_action(combined_moves, False)
        return action

    def update(self, opp_move):
        prev_moves = np.array([self.prev_nn_moves, self.prev_agent_moves]).T
        pred_id, id_logits = self.lstm.predict_id(self.input)
        probs = nnf.softmax(id_logits, dim=1).detach().cpu().numpy()
        # TODO: Implement Linear combination of results here
        self.val = self.q_agents[pred_id].pick_action(prev_moves, False)
        self.input = self.lstm.rebuild_input(self.val, opp_move, self.input[0])
        self.prev_agent_moves.append(opp_move)
        self.prev_nn_moves.append(self.val)

    def reset(self):
        prev_agent_choice = 0
        self.prev_agent_moves = []
        self.prev_nn_moves = []
        reward = 0
        self.input = self.lstm.build_input_vector(prev_agent_choice)
        self.val=0

class MemoryNAgent(BaseAgent):

  def __init__(self, name, id, n, user_defined_strategy):
    super().__init__(id)
    self.name = name
    self.n = n
    self.memory = {"agent": [0]*n, "opp": [0]*n}
    self.strategy = user_defined_strategy
    self.val = 0

  def update(self, opp_move):
    self.memory["agent"].append(self.val)
    self.memory["opp"].append(opp_move)
    self.memory["agent"].pop(0)
    self.memory["opp"].pop(0)
    out = 0
    for bit in self.memory["agent"]:
        out = (out << 1) | bit
    for bit in self.memory["opp"]:
        out = (out << 1) | bit
    self.val = self.strategy[out]

  def opt(self):
    return 0 if self.val==1 else 1

  def reset(self):
    self.memory["agent"] = [0]*self.n
    self.memory["opp"] = [0]*self.n
    self.val = 0

#Rather than creating multiple agents, we create a wrapper for them
#reduces memory requirements
class AgentWrapper:

    def __init__(self, agent):
        self.agent = agent
    
    def update(self, opp_move):
        self.agent.update(opp_move)

    def reset(self):
        self.agent.reset()
    
    def play(self):
        return self.agent.play()
    
    def id(self):
        return self.agent.id()

class Tournament:

    def __init__(self, generations, interactions, rounds, reproduction_rate, config):
        self.interactions = interactions
        self.generations = generations
        self.rounds = rounds
        self.reproduction_rate = reproduction_rate
        self.unique_agents = len(config['agents'])
        self.agents = self.create_agents(config)

    def create_agents(self, config):
        agents = []
        for agent_cfg in config["agents"]:
            if agent_cfg['type'] == 'ai':
                agent = AIAgent('default')
                agent.i = agent_cfg["id"]
            else: 
                agent = MemoryNAgent(agent_cfg['name'], agent_cfg['id'], agent_cfg['n'], agent_cfg['strategy'])
            copies = [AgentWrapper(agent) for i in range(agent_cfg['count'])]
            agents.extend(copies)
        return agents

    def get_reward(self, action_1, action_2, reward):
        reward_1 = 0
        reward_2 = 0
        if action_1 == 0 and action_2 == 0: # Both players cooperate
            reward_1 = reward[0][0]
            reward_2 = reward[0][1]
        elif action_1 == 0 and action_2 == 1: # Only player 2 defects
            reward_1 = reward[1][0]
            reward_2 = reward[1][1]
        elif action_1 == 1 and action_2 == 0: # Only player 1 defects
            reward_1 = reward[2][0]
            reward_2 = reward[2][1]
        elif action_1 == 1 and action_2 == 1: # Both players defect
            reward_1 = reward[3][0]
            reward_2 = reward[3][1]
        return reward_1, reward_2

    def play_IPD(self, agent0, agent1, reward):
        prev_agent0_moves = []
        prev_agent1_moves = []
        rewards = [0, 0]
        # Play ROUNDS iterations of the prisoners dilemma against the same agent
        for _ in range(self.rounds):
            prev_moves = np.array([prev_agent0_moves, prev_agent1_moves]).T
            agent0_action = int(agent0.play())
            agent1_action = int(agent1.play())
            agent0.update(agent1_action)
            agent1.update(agent0_action)
            prev_agent0_moves.append(agent0_action)
            prev_agent1_moves.append(agent1_action)
            # TODO: use words "move" or "action" consistently
            rewards[0] += self.get_reward(agent0_action, agent1_action, REWARD)[0]
            rewards[1] += self.get_reward(agent0_action, agent1_action, REWARD)[1]
        return rewards

    def natural_selection(self, agents_pre_selection):
        pop_size = len(agents_pre_selection)
        replacements = min(math.floor(self.reproduction_rate * pop_size), pop_size // 2)
        for i in range(replacements):
            agents_pre_selection[i] = agents_pre_selection[-i]
        return agents_pre_selection

    def animate_tournament(self, generations, agent_length):
        image_buffers = []
        for idx, generation in enumerate(generations):
            fig = Figure(figsize=(5,5))
            ax = fig.add_subplot(1, 1, 1)
            ax.axis('off')
            buffer = io.BytesIO()
            side = int(np.ceil(np.sqrt(len(generation))))
            img = np.full((side*side, 1), agent_length+1)
            for i, tournament_agent in enumerate(generation):
                img[i] = tournament_agent.id()
            img = img.reshape((side, side)).astype(np.uint8)
            im = ax.imshow(img, cmap='gist_ncar', vmin=0, vmax=agent_length)
            ax.set_title("Generation %d" % idx)
            fig.suptitle("Population Evolution in a Tournament Setting")
            fig.colorbar(im, ax=ax, location='right', shrink=0.7)
            fig.savefig(buffer, format='png')
            image_buffers.append(buffer)
        images = [Image.open(buffer) for buffer in image_buffers]
        gif_buffer = io.BytesIO()
        images[0].save(gif_buffer, 
                       format="GIF", 
                       save_all=True, 
                       append_images=images[1:],
                       optimize=False, 
                       loop=0, 
                       duration=len(images)*20)
        return gif_buffer

    def tournament(self):
        generations = []
        generations.append(self.agents)
        for generation in range(self.generations):
            tournament_agents = self.agents
            rewards = [0] * len(tournament_agents)
            agents_and_rewards = [list(a_r) for a_r in zip(tournament_agents, rewards)]
            for interaction in range(self.interactions):
                random.shuffle(agents_and_rewards)
                for i in range(0, len(agents_and_rewards) - 1, 2):
                    agent0 = agents_and_rewards[i][0]
                    agent1 = agents_and_rewards[i+1][0]
                    agent0.reset()
                    agent1.reset()
                    reward0, reward1 = self.play_IPD(agent0, agent1, REWARD)
                    agents_and_rewards[i][1] += reward0
                    agents_and_rewards[i+1][1] += reward1   
            agents_and_rewards.sort(key=lambda x: x[1])
            agents_pre_selection = [list(a_r) for a_r in zip(*agents_and_rewards)][0]
            agents_post_selection = self.natural_selection(agents_pre_selection)
            generations.append(agents_post_selection)
            self.agents = agents_post_selection
        return self.animate_tournament(generations, self.unique_agents)


if __name__ == "__main__":

    generations = 20
    interactions = 2
    rounds = 10
    reproduction_rate = 0.5
    config = {
        "agents":[
            {
                "name": "Cooperate",
                "id": 0,
                "count": 5,                
                "type": "memory",
                "n": 1,
                "strategy": [0, 0, 0, 0]
            },
            {
                "name": "Defect",
                "id": 1,                
                "type": "memory",
                "count": 5,
                "n": 1,
                "strategy": [1, 1, 1, 1]
            },
            {
                "name": "Copy",
                "id": 2,                
                "type": "memory",
                "count": 5,
                "n": 1,
                "strategy": [0, 1, 0, 1]
            },
            {
                "name": "Generic",
                "id": 3,
                "type": "memory",
                "count": 5,
                "n": 1,
                "strategy": [1, 0, 0, 1]
            },  {
                "name": "AI",
                "id": 4,
                "type": "ai",
                "count": 5,
            }
        ]
    }

    tournament = Tournament(generations, interactions, rounds, reproduction_rate, config)
    buffer = tournament.tournament()
    print(buffer.getvalue())

    