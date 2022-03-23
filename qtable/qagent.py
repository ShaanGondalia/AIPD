import random

class QAgent:

  def __init__(self, lr, discount, epsilon=1, decay_rate=0.99, min_e=0.1):
    self.Q = {}
    self.epsilon = epsilon
    self.lr = lr
    self.discount = discount
    self.decay_rate = decay_rate
    self.min_e = min_e

  def get_q(self, state):
    state = str(state)
    q1 = self.Q[state][0] # Cooperate
    q2 = self.Q[state][1] # Defect
    return q1, q2

  def set_q(self, state, q1, q2):
    state = str(state)
    self.Q[state][0] = q1
    self.Q[state][1] = q2

  def set_epsilon(self, epsilon):
    self.epsilon = epsilon

  # Return action with highest reward, or random
  def max_q(self, state):
    state = str(state)
    q1, q2 = self.get_q(state)
    if q1 == q2 or random.random() <= self.epsilon:
      return random.randint(0,1)
    elif q1 > q2:
      return 0
    else:
      return 1

  def pick_action(self, state, is_curious):
    state = str(state)
    if state not in self.Q:
      self.Q[state] = [0, 0]
    self.epsilon = max(self.epsilon*self.decay_rate, self.min_e)

    # Explore unseen paths
    if is_curious:
      if self.Q[state][0] == self.Q[state][1]:
        return random.randint(0,1)
      if self.Q[state][0] == 0:
        return 0
      elif self.Q[state][1] == 0:
        return 1

    return self.max_q(state)
  
  def reward_action(self, prev_state, curr_state, action, reward, is_final_round):
    prev_state = str(prev_state)
    curr_state = str(curr_state)

    future_potential = 0
    if not is_final_round:
      if curr_state not in self.Q:
        self.Q[curr_state] = [0, 0]
      future_potential = self.discount * max(self.Q[curr_state])

    self.Q[prev_state][action] = self.Q[prev_state][action] + self.lr * (reward + future_potential - self.Q[prev_state][action])

  def get_table(self):
    return self.Q
