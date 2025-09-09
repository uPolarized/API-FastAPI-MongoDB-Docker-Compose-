from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    # A MUDANÇA ESTÁ AQUI
    # A assinatura do método foi atualizada para aceitar o 'handler'
    # e a lógica foi ajustada para o padrão do Pydantic v2
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        # Simplesmente dizemos ao Pydantic/FastAPI que este campo
        # deve ser tratado como uma string na documentação do OpenAPI.
        return {'type': 'string'}