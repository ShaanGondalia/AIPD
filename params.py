LSTM_HIDDEN = 200
LSTM_LAYERS = 4
LSTM_LR = 1e-4
LSTM_PRETRAIN_EPOCHS = 20
LSTM_PRETRAIN_BATCH_SIZE = 32
LSTM_PRETRAIN_SAMPLE_SIZE = 1024

QTABLE_TRAIN_EPOCHS = 10000
QTABLE_TEST_EPOCHS = 1000
QTABLE_LR = 1            # Higher value means more aggressive learning [0, 1]
QTABLE_DISCOUNT = 1      # Higher value means trust more in Q-Table [0, 1]
QTABLE_EPSILON_TRAIN = 1 # Higher value means more random [0, 1]
QTABLE_EPSILON_TEST = 0  # Higher value means more random [0, 1]
QTABLE_MIN_EPSILON = 0   # Bounds how low epsilon can decay [0, 1]
QTABLE_DECAY_RATE = 1    # Lower value means faster decay [0, 1]
QTABLE_MEMORY = 1000     # Number of past moves remembered in any given state [0, INF]

DEVICE = 'cuda'
IN = 2
OUT = 2
REWARD = [[2, 2], # Coop, Coop
          [0, 3], # Coop, Dfct
          [3, 0], # Dfct, Coop
          [1, 1]] # Dfct, Dfct

TEST_GAMES = 200
TEST_ROUNDS = 10
TEST_EPOCHS = 20

ROUNDS = 10
GENERATIONS = 10
INTERACTIONS = 3
REPRODUCTION_RATE = 0.5