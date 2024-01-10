# chat.py
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pickle
import random
import json

stemmer = LancasterStemmer()

def load_chatbot_data():
    with open("intents.json") as file:
        data = json.load(file)

    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []

            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    return words, labels, training, output, data

def load_chatbot_model(training, output):
    model = Sequential([
        Dense(8, input_shape=(len(training[0]),), activation='relu'),
        Dense(8, activation='relu'),
        Dense(len(output[0]), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

 
    model.fit(np.array(training), np.array(output), epochs=100, batch_size=5, verbose=1)
    model.save_weights("model.tflearn")

    return model

def get_chatbot_response(user_input, model, words, labels, data):
    results = model.predict([bag_of_words(user_input, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            return random.choice(tg['responses'])

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return bag
