from email import message
from algokit_utils import AlgorandClient, Account
from smart_contracts.artifacts.nftcreditscore.credit_score_nft_client import CreditScoreNftClient
import os
from algosdk import transaction
from algosdk.logic import get_application_address
import base64



from smart_contracts.artifacts.nftcreditscore.credit_score_nft_client import (
        CreditScoreNftFactory,
    )

import asyncio
from dotenv import load_dotenv
load_dotenv()
# -----------------------------
# 1️⃣ Load environment variables
# -----------------------------
DEPLOYER_MNEMONIC = os.getenv("DEPLOYER_MNEMONIC")
APP_ID : str = os.getenv("NFT_CREDIT_SCORE") ;  # The deployed VaultLending App ID
USDC_ASA_ID : str = os.getenv("USDC_ASA_ID")

if not DEPLOYER_MNEMONIC or not APP_ID or not USDC_ASA_ID:
    raise ValueError("Please set DEPLOYER_MNEMONIC, VAULT_APP_ID, USDC_ASA_ID in your environment.")

# -----------------------------
# 2️⃣ Setup Algorand client
# -----------------------------
algod_client = AlgorandClient.testnet()
deployer = algod_client.account.from_mnemonic(mnemonic=DEPLOYER_MNEMONIC)
print("🔑 Deployer address:", deployer.address)

# -----------------------------
# 3️⃣ Load AppClient using App ID
# -----------------------------

#factory = algod_client.get_typed_app_factory(VaultlendingFactory, default_sender=deployer)
APP_SPEC_PATH = "smart_contracts/artifacts/nftcreditscore/CreditScoreNFT.arc56.json"

async def hello(amount_microalgos: int, mnemonic: str):
    try:
        client = CreditScoreNftClient(
            algorand=algod_client,
            app_id=int(APP_ID),
            default_sender=deployer.address,  # required to send transactions
            default_signer=deployer.signer,   # required to sign transactions
        )

        print("CreditScoreNftClient client ready. App ID:", client.app_address)

        #whitelist_tx = client.params.hello(( 'name',))
        response = client.send.hello(( 'name',))
        print(response)
    
        print("✅ Hello called ")
        #print(whitelist_tx)
        return {"message": response.abi_return, "success": True, "txId": response.tx_id}
    
    except Exception as e:
        return {"message": str(e), "success": False}
    


