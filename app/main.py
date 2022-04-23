from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, auth, payment_book

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(payment_book.router)


@app.get("/")
def root():
    ''' root url '''
    return {"message": "Hello flasede api"}
