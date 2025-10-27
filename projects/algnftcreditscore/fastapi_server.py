from ast import And
from typing import Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
from nftcreditscore_client import hello


# --------------------------
# Configuration
# --------------------------
CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
#SOURCE_CODE = os.getenv("X_SOURCE_CODE")

# --------------------------
# FastAPI setup
# --------------------------

app = FastAPI(
    title="Borderless Fuse Pay BNPL",
    description="Borderless Fuse Pay BNPL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Request body model
# --------------------------
class DepositDataRequest(BaseModel):
    key: str   # Wallet Public Address
    amount: str  # amount
    symbol: str

class BalanceRequest(BaseModel):
    tokenAddress: str  
    walletAddress: str  
    symbol: str
    rpcUrl:str


class DocumentUploadRequest(BaseModel):
    docUrl: str   #  Document Url
    docType: str  # document Type



# --------------------------
# API Route to fetch wallet transaction onchain by address
# --------------------------
@app.post("/hello")
async def deposit(
    req: DepositDataRequest,
     x_client_id: str = Header(..., alias="x-client-id"),
    x_client_secret: str = Header(..., alias="x-client-secret")
):
    print('welcome')

    result = await hello(req.amount,req.key);
    #result = await check_vault_balance()
    return result
