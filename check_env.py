from pathlib import Path
import os
from dotenv import load_dotenv

print("Current directory:", Path.cwd())

env_path = Path(".env")
print("Exists:", env_path.exists())
print("Resolved path:", env_path.resolve())

loaded = load_dotenv(dotenv_path=env_path, override=True)
print("Loaded:", loaded)

print("Environment variable:", os.getenv("OPENWEATHER_API_KEY"))