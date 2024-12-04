from http.client import HTTPException

from fastapi import FastAPI, Path
from typing import Annotated
from typing import Dict

app = FastAPI()
print('aaa')

users = {'1': {'Имя': 'Example', 'возраст': '18'}}


@app.get("/users/")
async def get_users() -> Dict[str, Dict[str, str]]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3, max_length=15, regex='^[a-zA-Z0-9_.-]+$', description='Имя пользователя')],
                   age: Annotated[str, Path(regex='^(100|[5-9]|[1-9][0-9]){1,3}$', description='Возраст пользователя')]) -> str:
    new_id = max(k for k, v in users.items())
    users[str(int(new_id) + 1)] = {'Имя': username, 'возраст': age}
    return f"he user {str(int(new_id) + 1)} is updated"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[str, Path(min_length=1, max_length=8, regex='[0-9]+$', description='ID пользователя')],
                      username: Annotated[str, Path(min_length=3, max_length=15, regex='^[a-zA-Z0-9_.-]+$', description='Имя пользователя')],
                      age: Annotated[str, Path(regex='^(100|[5-9]|[1-9][0-9]){1,3}$', description='Возраст пользователя')]) -> str:
    key = [key for key, value in users.items() if key == user_id]
    if len(key):
        users[key[0]] = {'Имя': username, 'возраст': age}
        return f'The user {user_id} is updated'
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete('/users/{user_id}')
async def del_user(user_id: Annotated[str, Path(min_length=1, max_length=8, regex='[0-9]+$', description='ID пользователя')]) -> None:
    key = [key for key, value in users.items() if key == user_id]
    print(type(key), ' ', key)
    if len(key):
        del users[key[0]]
        return f'User {key}has been deleted'
    raise HTTPException(status_code=404, detail="Задача не найдена")
