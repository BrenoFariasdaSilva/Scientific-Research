# Word2Vec

Word2Vec is a neural network-based algorithm used to generate word embeddings, which are vector representations of words in a high-dimensional space. These word embeddings are used to capture the semantic meaning of words and their relationships with other words. This is the algorithm i'm studying in my scientific research.

## Original Repository

This code is based on the [original repository](https://github.com/danielfrg/word2vec) by Daniel Rodriguez, which contains the C source code for the Word2Vec algorithm.

## Running the Code

In order to run the code, you can use my makefile or use command line. But, more importantly, you must open `getTitles.py` and, in line 4, add the path to the `issue.json` file.

## How it works

Word2Vec uses a two-layer neural network to generate word embeddings. The first layer, called the input layer, takes a one-hot encoded vector representing a word as input. The second layer, called the output layer, generates a probability distribution over the vocabulary. The weights of the neural network are adjusted during training to maximize the probability of predicting the context words given the input word.

There are two different architectures for Word2Vec: Continuous Bag of Words (CBOW) and Skip-gram. In CBOW, the model predicts the current word given the surrounding context words. In Skip-gram, the model predicts the context words given the current word.

## Applications

Word2Vec has been used in a wide range of natural language processing tasks, including language translation, text classification, sentiment analysis, and more. It has also been used in recommendation systems, search engines, and chatbots.

## Limitations

Word2Vec has some limitations, such as difficulty in handling out-of-vocabulary words and inability to capture certain types of relationships between words, such as antonyms. However, it remains a popular and effective algorithm for generating word embeddings.
