EPOCHS = 10000
TEST_EPOCHS = 1000
ROUNDS = 10
LR = 1            # Higher value means more aggressive learning [0, 1]
DISCOUNT = 1      # Higher value means trust more in Q-Table [0, 1]
EPSILON_TRAIN = 1 # Higher value means more random [0, 1]
EPSILON_TEST = 0  # Higher value means more random [0, 1]
MIN_EPSILON = 0   # Bounds how low epsilon can decay [0, 1]
DECAY_RATE = 1    # Lower value means faster decay [0, 1]
MEMORY = 1000     # Number of past moves remembered in any given state [0, INF]
REWARD = [[2, 2], # Coop, Coop
          [0, 3], # Coop, Dfct
          [3, 0], # Dfct, Coop
          [1, 1]] # Dfct, Dfct