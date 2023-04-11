from fastapi import FastAPI
from crud import router
app = FastAPI(title='Web App')

app.include_router(router)