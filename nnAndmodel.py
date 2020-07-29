import nltk
import numpy as np
import json
import torch
import random
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from nltk.stem.porter import PorterStemmer

#stemer to stem the words of a query-- readucing words
stemmer  = PorterStemmer()


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(token_sentence, all_words):
    token_sentence = [stem(w) for w in token_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)

    for index, w in enumerate(all_words):
        if w in token_sentence:
            bag[index] = 1.0

    return bag


with open('intents.json', 'r') as file:
    intents = json.load(file)

all_words = []
tags = []
xy = []


for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# elements to be ignored in list
ignore = ['?', '.', ',', '!']

all_words = [stem(w) for w in all_words if w not in ignore]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
Y_train = []

for (pattent_sentence, tag) in xy:
    bag = bag_of_words(pattent_sentence, all_words)
    X_train.append(bag)

    labels = tags.index(tag)

    Y_train.append(labels)

X_train = np.array(X_train)
Y_train = np.array(Y_train)


class Chat_Dataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


batch_size = 8

dataset = Chat_Dataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)


class NuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        return out

hidden_size = 8
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = .001
num_epochs = 1000

device = torch.device('cpu')
model = NuralNet(input_size, hidden_size, output_size).to(device)
creterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)

        outputs = model(words)
        loss = creterion(outputs, labels.long())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"epoch : {epoch + 1}/{num_epochs}, loss : {loss.item():.4f}")

print(f"final epoch : {epoch + 1}/{num_epochs}, final loss : {loss.item():.4f}")

data = {
    "model_state":model.state_dict(),
    "input_size":input_size,
    "output_size":output_size,
    "hidden_size":hidden_size,
    "all_words":all_words,
    "tags":tags
}

FILE = "data.pth"
torch.save(data, FILE)
print(f"Training completed. Data saved to {FILE}")

# while True:
#     data = torch.load(FILE)
#
#     query = input("You :")
#     query = tokenize(query)
#     x = bag_of_words(query, all_words)
#     x = x.reshape(1, x.shape[0])
#     x = torch.from_numpy(x)
#
#     op = model(x)
#
#     _, predicted = torch.max(op, dim=1)
#     tg = tags[predicted.item()]
#
#     # probs = torch.softmax(outputs, dim=1)
#     # prob = probs[0][predicted.item()]
#
#     # if prob.item() > 0.75:
#     for intent in intents['intents']:
#         if tg == intent['tag']:
#             print(f"Answer : {random.choice(intent['responses'])}")