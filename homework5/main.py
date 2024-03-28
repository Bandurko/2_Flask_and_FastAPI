'''
Задание

Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой
задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку
Pydantic.
'''

from typing import Optional
#import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


tasks = [
    {
        'id': 1,
        'title': 'first',
        'description': 'text',
        'status': True
    },
    {
        'id': 2,
        'title': '2',
        'description': '2222',
        'status': False
    },
]
count = len(tasks)


class Task(BaseModel):
    title: str
    description: str
    status: Optional[bool] = False


@app.get('/tasks/')
async def get_tasks(status: bool = None):
    print(type(status))
    res = []
    if status is not None:
        for item in tasks:
            if item['status'] == status:
                res.append(item)
        return res
    return tasks


@app.get('/tasks/{id}')
async def get_task_id(id: int):
    for item in tasks:
        if item['id'] == id:
            return item
    return JSONResponse({'error': 'ID not found'}, 404)


@app.post('/tasks/')
async def create_tasks(task: Task):
    global count
    count += 1
    res = {
        'id': count,
        'title': task.title,
        'description': task.description,
        'status': task.status
    }
    tasks.append(res)
    return JSONResponse({'message': 'Success'}, 201)


@app.put('/tasks/{id}')
async def update_task(id: int, task: Task):
    for item in tasks:
        if item['id'] == id:
            item.update(task)
    return JSONResponse({'message': 'Success'}, 200)


@app.delete('/tasks/{id}')
async def delete_task(id: int):
    for item in tasks:
        if item['id'] == id:
            tasks.remove(item)
            return JSONResponse({'message': 'Success'}, 200)
    return JSONResponse({'error': 'ID not found'}, 404)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)