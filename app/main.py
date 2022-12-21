from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, auth, payment_book, monthly_payments
from mangum import Mangum

app = FastAPI(
        title="flasede",
        root_path="/prod",
        docs_url="/docs",
        openapi_url="/prod/openapi.json",
        )

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
app.include_router(monthly_payments.router)

@app.get("/")
def root():
    ''' root url '''
    return {"message": "Hello flasede api"}

handler = Mangum(app)
