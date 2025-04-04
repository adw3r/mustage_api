import uvicorn
from fastapi import FastAPI

import src.core.config
from src.payments import route

app = FastAPI(title="API v1")
app.include_router(router=route.router)

@app.get('/test')
async def root_test():
    return {'status': 'ok'}


def main():
    uvicorn.run('src.main:app', host=src.core.config.APP_HOST, port=int(src.core.config.APP_PORT))


if __name__ == '__main__':
    main()
