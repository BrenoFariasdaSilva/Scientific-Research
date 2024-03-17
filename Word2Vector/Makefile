# Name of the virtual environment directory
VENV := venv
# Python command to use
PYTHON := python3

.PHONY: all venv dependencies run

all: venv dependencies run

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	touch $(VENV)/bin/activate

run:
	clear; $(VENV)/bin/python ./word2vec.py

dependencies:
	$(VENV)/bin/pip install colorama gensim nltk tqdm 
