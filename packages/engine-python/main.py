import argparse
import logging
import uvicorn
from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.server import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Noetic Engine Reference Implementation")
    parser.add_argument("--codex", type=str, required=True, help="Path to the .noetic Codex file")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve the UI on")
    args = parser.parse_args()

    engine = NoeticEngine()
    app = create_app(engine, args.codex)

    # Start Web Server (lifespan will handle the engine)
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
