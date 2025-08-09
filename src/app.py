import asyncio
import json
import logging
import threading
import os
import sys
import tempfile
import shutil
import flask
import websockets
from werkzeug.serving import run_simple


def is_pyinstaller():
    return getattr(sys, 'frozen', False)


def get_assets_path():
    if is_pyinstaller():
        # Running as PyInstaller executable
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'assets')
    else:
        # Running as script
        return "assets"


app = flask.Flask(__name__)
app.static_folder = get_assets_path()
# Silence Flask and Werkzeug startup messages
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('flask').setLevel(logging.ERROR)
app.logger.setLevel(logging.ERROR)

output_folder = "output"


def first_time_setup():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if is_pyinstaller():
        if not os.path.exists('scripts'):
            os.makedirs('scripts')
        script_path = os.path.join(sys._MEIPASS, 'obs', 'update_life_totals.lua')
        with open(script_path) as f:
            lua_script = f.read()
        with open("scripts/update_life_totals.lua", "w") as f:
            f.write(lua_script)

    
@app.route("/")
def tracker():
    return app.send_static_file("tracker.html")


def write_life_total(player_num, life):
    """Write life total to player file using atomic file operations."""
    temp_file_path = None
    final_file_path = f'{output_folder}/player_{player_num}_life.txt'
    try:
        # Create temporary file in the same directory as the final file
        with tempfile.NamedTemporaryFile(
            mode='w', 
            dir=output_folder, 
            prefix=f'player_{player_num}_life_', 
            suffix='.tmp', 
            delete=False
        ) as temp_file:
            temp_file.write(str(life))
            temp_file_path = temp_file.name
        
        # Atomically replace the final file
        shutil.move(temp_file_path, final_file_path)
        
    except Exception as e:
        print(f"Error writing life total for player {player_num}: {e}")
        # Clean up temporary file if it exists
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass


async def message_handler(websocket):
    try:
        async for message in websocket:
            message = json.loads(message)
            if message.get("type") == "update":
                data = message.get("data")
                print(f"Received update: {data}")
                for player_num, life in data.items():
                    write_life_total(player_num, life)
            else:
                print(f'Received unexpected message: {message}')
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


def start_websocket_server():
    async def run_server():
        async with websockets.serve(message_handler, "0.0.0.0", 8765):
            # Run forever
            await asyncio.Future()
    asyncio.run(run_server())


if __name__ == "__main__":
    first_time_setup()
    ws_thread = threading.Thread(target=start_websocket_server)
    ws_thread.start()
    print("Starting server.")
    print("You should be able to access the life tracker on your phone at: http://<device_name>.<tailscale_dns_name>.ts.net:5000")
    run_simple("0.0.0.0", 5000, app, use_reloader=False, use_debugger=False, use_evalex=False)