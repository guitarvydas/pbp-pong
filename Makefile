NAME=pong
all:
	node ./pbp/das/das2json.mjs $(NAME).drawio
	python3 main.py . '' GUItest $(NAME).drawio.json

init:
	npm install yargs prompt-sync ohm-js @xmldom/xmldom
