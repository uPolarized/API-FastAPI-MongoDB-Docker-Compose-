# app/crud.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from schemas import UserCreate, UserUpdate

# --- Funções CRUD ---

async def create_user(db: AsyncIOMotorDatabase, user: UserCreate):
    """Cria um novo usuário no banco de dados."""
    user_dict = user.model_dump()
    try:
        result = await db.users.insert_one(user_dict)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        return created_user
    except DuplicateKeyError:
        return None # Indica que o e-mail já existe

async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str):
    """Busca um usuário pelo seu ID."""
    if not ObjectId.is_valid(user_id):
        return None
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return user

async def get_users(
    db: AsyncIOMotorDatabase,
    q: str | None,
    min_age: int | None,
    max_age: int | None,
    is_active: bool | None,
    page: int,
    limit: int
):
    """Lista usuários com filtros e paginação."""
    query = {}
    
    # Filtro de busca por nome (case-insensitive)
    if q:
        query["name"] = {"$regex": q, "$options": "i"}
        
    # Filtro de idade
    age_filter = {}
    if min_age is not None:
        age_filter["$gte"] = min_age
    if max_age is not None:
        age_filter["$lte"] = max_age
    if age_filter:
        query["age"] = age_filter

    # Filtro de status ativo
    if is_active is not None:
        query["is_active"] = is_active
        
    # Contagem total de documentos para paginação
    total_users = await db.users.count_documents(query)

    # Lógica de paginação
    skip = (page - 1) * limit
    
    cursor = db.users.find(query).sort("name", 1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    
    return users, total_users

async def update_user(db: AsyncIOMotorDatabase, user_id: str, user_update: UserUpdate):
    """Atualiza um usuário existente."""
    if not ObjectId.is_valid(user_id):
        return None
        
    # Cria um dicionário apenas com os campos que foram fornecidos para atualização
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        return {"matched_count": 1, "modified_count": 0} # Nenhum dado para atualizar

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    return {"matched_count": result.matched_count, "modified_count": result.modified_count}

async def delete_user(db: AsyncIOMotorDatabase, user_id: str):
    """Deleta um usuário."""
    if not ObjectId.is_valid(user_id):
        return 0 # Indica que o ID é inválido
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count