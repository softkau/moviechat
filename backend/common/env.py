import os
from dotenv import load_dotenv

load_dotenv()
ENV_PROJECT_ROOT=os.getenv("PROJECT_ROOT")
ENV_OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
ENV_TMDB_API_KEY=os.getenv("TMDB_API_KEY")