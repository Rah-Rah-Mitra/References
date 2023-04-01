
import numpy as np
from keras.layers import Conv1D, BatchNormalization, Flatten, Dense, Dropout, MaxPooling2D, Reshape
from keras.models import Sequential, Model
from keras.utils import to_categorical, normalize
from math import gamma



# Player Class
class Player:
    def __init__(self):
        self.x = np.random.randint(-50, 50)
        self.y = np.random.randint(-50, 50)
        self.speed = 1
        self.WASD = [False, False, False, False]

    def update(self):
        if self.WASD[0] and not self.WASD[2]:
            self.y += self.speed
        if self.WASD[1] and not self.WASD[3]:
            self.x -= self.speed
        if self.WASD[2] and not self.WASD[0]:
            self.y -= self.speed
        if self.WASD[3] and not self.WASD[1]:
            self.x += self.speed


class Objective:
    def __init__(self):
        self.x = np.random.randint(-50, 50)
        self.y = np.random.randint(-50, 50)


player = Player()
objective = Objective()

X = []
y = []
for _ in range(1):
    action = np.random.randint(0, 4)
    action_onehot = to_categorical(action, num_classes=4)
    X.append(player.WASD + [objective.x - player.x, objective.y - player.y])
    y.append(action_onehot)

    if action == 0:
        player.WASD[0] = True
        player.WASD[not 0] = False
    elif action == 1:
        player.WASD[1] = True
        player.WASD[not 1] = False
    elif action == 2:
        player.WASD[2] = True
        player.WASD[not 2] = False
    elif action == 3:
        player.WASD[3] = True
        player.WASD[not 3] = False

    player.update()

X = np.array(X)
X = normalize(X)
y = np.array(y)

input_shape = X[0].shape

# Create your Model
model = Sequential()
model.add(Dense(128, input_dim=input_shape, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(4, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
              
# Reinforcement learning loop
player = Player()
objective = Objective()

for i in range(1000):
    state = player.WASD + [objective.x - player.x, objective.y - player.y]
    action_probs = model.predict(np.array([state]))[0]
    action = np.argmax(action_probs)

    if action == 0:
        player.WASD[0] = True
        player.WASD[not 0] = False
    elif action == 1:
        player.WASD[1] = True
        player.WASD[not 1] = False
    elif action == 2:
        player.WASD[2] = True
        player.WASD[not 2] = False
    else:
        player.WASD[3] = True
        player.WASD[not 3] = False

    player.update()

    reward = -1

    if player.x == objective.x and player.y == objective.y:
        reward = 100
        objective = Objective()

    new_state = player.WASD + [objective.x - player.x, objective.y - player.y]
    new_action_probs = model.predict(np.array([new_state]))[0]
    new_action = np.argmax(new_action_probs)

    if new_action == 0:
        player.WASD[0] = True
        player.WASD[not 0] = False
    elif new_action == 1:
        player.WASD[1] = True
        player.WASD[not 1] = False
    elif new_action == 2:
        player.WASD[2] = True
        player.WASD[not 2] = False
    else:
        player.WASD[3] = True
        player.WASD[not 3] = False

    new_state_value = model.predict(np.array([new_state]))[0]
    target = reward + gamma(np.max(new_state_value))

    target_f = model.predict(np.array([state]))
    target_f[0][action] = target

    model.fit(np.array([state]), target_f, epochs=1, verbose=0)