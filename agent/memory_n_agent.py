from .base_agent import BaseAgent

class MemoryNAgent(BaseAgent):

  # (PrevSelfMove PrevOppMove: NextSelfMove)

  # The user defined strategy is a list of 4^n entries. Each entry corresponds 
  # to a sequence of the agent's previous moves and the opponent's previous 
  # moves. For instance, the sequence 00 01 corresponds to the sequence of two
  # cooperations from the agent and a cooperation and defection from the opponent.
  # The index of the list is given by the decimal representation of the sequence.
  def __init__(self, id, n, user_defined_strategy):
    super().__init__(id)
    self.n = n
    self.memory = {"agent": [0]*n, "opp": [0]*n}
    self.strategy = user_defined_strategy
    self.val = 0

  def update(self, opp_move):
    self.memory["agent"].append(self.opt())
    self.memory["opp"].append(opp_move)
    self.memory["agent"].pop(0)
    self.memory["opp"].pop(0)
    
    out_one = 0
    out_two = 0
    for bit in self.memory["agent"]:
        out_one = (out_one << 1) | bit
    for bit in self.memory["opp"]:
        out_two = (out_two << 1) | bit

    self.val = self.strategy[out_one + out_two]

  def opt(self):
    return 0 if self.val==1 else 1

  def reset(self):
    self.memory["agent"] = [0]*self.n
    self.memory["opp"] = [0]*self.n
    self.val = 0