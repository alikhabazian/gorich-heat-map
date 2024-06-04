from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the directory containing the tiles
TILE_DIR = './maps/'

@app.route('/tiles/<int:z>/<int:x>/<int:y>@2x.webp')
def serve_tile(z, x, y):
    try:
        # Construct the path to the requested tile
        tile_path = os.path.join(TILE_DIR, str(z), str(x), f'{y}@2x.webp')
        print(tile_path)
        # Check if the tile exists
        if not os.path.exists(tile_path):
            abort(404)  # Tile not found
        
        # Serve the tile
        return send_from_directory(os.path.dirname(tile_path), os.path.basename(tile_path))
    except Exception as e:
        print(f"Error serving tile: {e}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
