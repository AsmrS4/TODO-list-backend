from uuid import uuid4

async def uuid_generator():
    return str(uuid4())