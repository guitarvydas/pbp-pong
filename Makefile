NAME=pong
all: looptest.py
	node ./pbp/das/das2json.mjs $(NAME).drawio
	python3 main.py . '' GUItest $(NAME).drawio.json

looptest.py : looptest.py.m4 looptestsm.inc
	m4 looptest.py.m4 > looptest.py

init:
	npm install yargs prompt-sync ohm-js @xmldom/xmldom
