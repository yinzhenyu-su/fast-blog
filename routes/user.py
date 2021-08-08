from typing import List
import uuid
from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.user import User
from db import database
from db.users import users

router = APIRouter(prefix='/user')


@router.post('/', response_model=User)
async def create(user: User):
    id = str(uuid.uuid4())
    query = users.insert().values(id=id,
                                  username=user.username,
                                  password=user.password)
    try:
        await database.execute(query)
        return {**user.dict(), 'id': id}
    except:
        return JSONResponse({'msg': 'error'}, status_code=500)


@router.get('/', response_model=List[User])
async def get():
    query = users.select()
    return await database.fetch_all(query)


@router.delete('/{user_id}')
async def delete(user_id: str):
    query = users.delete().where(users.c.id == user_id)
    del_rows = await database.execute(query)
    if (del_rows > 0):
        return JSONResponse(
            {'msg': 'success del {row} rows'.format(row=del_rows)},
            status_code=204)
    else:
        return JSONResponse(status_code=404)
