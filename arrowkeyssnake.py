import logging
import os
import time
from flask import Flask
from flask import request
from pynput import keyboard

moves = []
in_game = False
last_move = "up"



app = Flask(__name__)
@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#00FF00",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }



@app.post("/start")
def handle_start():
	global in_game, moves
	moves = ['up']
	in_game = True
	data = request.get_json()

	print(f"{data['game']['id']} START")
	return "ok"


@app.post("/move")
def handle_move():
	global last_move
	time.sleep(0.4)
	if len(moves) == 0:
		return {"move": last_move}
	move = moves[0]
	del moves[0]
	last_move = move
	return {"move": move}


@app.post("/end")
def handle_end():
	global in_game
	in_game = False
	data = request.get_json()

	print(f"{data['game']['id']} END")
	return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "BattlesnakeOfficial/starter-snake-python"
    return response



def run():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8082"))

    print(f"\nRunning Battlesnake server at http://{host}:{port}")
    app.debug = 'development'
    app.run(host=host, port=port, debug=True)
 

def on_press(key):
	if in_game:
		global moves
		if key == keyboard.Key.esc:
			return False  # stop listener
		try:
			k = key.char  # single-char keys
		except:
			k = key.name  # other keys
		if len(moves) == 0:
			end_move = last_move
		else:
			end_move = moves[-1]
		if k in ['up', 'down']:
			if end_move not in ['up', 'down']:
				moves.append(k)
		if k in ['left', 'right']:
			if end_move not in ['left', 'right']:
				moves.append(k)
		 
		
       

if __name__ == '__main__':
	listener = keyboard.Listener(on_press=on_press)
	listener.start() 
	run()
	listener.join()
