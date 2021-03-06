import numpy
import tensorflow as tf
# from tf.keras.datasets import imdb
from tensorflow import keras
# from keras import datasets
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence

__all__ = [Sequential, Dense, LSTM]

# initializing the random number generator to a constant value to ensure we can easily reproduce the results.
numpy.random.seed(7)

# load the IMDB dataset.
# We are constraining the dataset to the top 5,000 words.
# We also split the dataset into train (50%) and test (50%) sets.
top_words = 5000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=top_words)
# truncate and pad the input sequences so that they are all the same length for modeling.
max_review_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

# Define LSTM Model
# first layer is the Embedded layer that uses 32 length vectors to represent each word.
# The next layer is the LSTM layer with 100 memory units (smart neurons).
# Finally, because this is a classification problem we use a Dense output layer with a single neuron and
# a sigmoid activation function to make 0 or 1 predictions for the two classes (good and bad) in the problem.
# input dropout and recurrent drop out has been added to overcome overfitting
embedding_vector_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_review_length))
# lstm with input dropout and recurrent dropout
model.add(LSTM(100,dropout=0.2,recurrent_dropout=0))
model.add(Dense(1, activation='sigmoid'))
# log loss is used as the loss function (ADAM optimization algorithm).
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
# A large batch size of 64 reviews is used to space out weight updates.
model.fit(X_train, y_train, epochs=3, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy:%.2f%%" % (scores[1] * 100))

print('-----Bidirectional LSTM-------')
