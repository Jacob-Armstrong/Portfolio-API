from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("NEON_DB_URL")

# TODO: Remove echo before deployment
engine = create_engine(database_url, echo=True)