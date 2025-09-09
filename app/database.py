# app/database.py
import os
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    db: motor.motor_asyncio.AsyncIOMotorDatabase = None

db_handler = Database()

async def connect_to_mongo():
    """Conecta ao MongoDB e cria o índice único."""
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable not set!")
        
    try:
        print("Connecting to MongoDB...")
        db_handler.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        
        db_handler.db = db_handler.client.userdb
        
        await db_handler.db.users.create_index("email", unique=True)
        print("Successfully connected to MongoDB and created unique index.")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        
        raise

async def close_mongo_connection():
    """Fecha a conexão com o MongoDB."""
    print("Closing MongoDB connection...")
    if db_handler.client:
        db_handler.client.close()
    print("MongoDB connection closed.")

def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """Retorna a instância do banco de dados."""
    if db_handler.db is None:
        raise RuntimeError("Database is not connected. Call connect_to_mongo first.")
    return db_handler.db