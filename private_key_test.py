from dotenv import load_dotenv
import os

print("cwd:", os.getcwd())
print("dotenv loaded:", load_dotenv())
print("key:", os.getenv("KRAKEN_API_KEY"))