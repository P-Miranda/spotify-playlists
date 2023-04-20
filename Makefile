VENV=.venv
PYTHON_VENV=$(VENV)/bin/python3
REQUIREMENTS=requirements.txt

PLAYLIST_SCRIPT=spotify_playlists.py

TOKEN_FILE?=.token
SPOTIFY_USER?=P-Miranda

all: playlists

playlists: $(PYTHON_VENV)
	$(PYTHON_VENV) $(PLAYLIST_SCRIPT) $(TOKEN_FILE) $(SPOTIFY_USER)

$(PYTHON_VENV):
	python3 -m venv $(VENV)
	$(PYTHON_VENV) -m pip install --upgrade pip
	$(PYTHON_VENV) -m pip install -r $(REQUIREMENTS)

clean-all:
	@rm -rf *.csv
