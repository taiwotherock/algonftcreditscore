from algopy import ARC4Contract, String
from algopy.arc4 import abimethod
from algopy import ARC4Contract, arc4, UInt64

from algopy import (
    ARC4Contract,
    Account,
    Asset,
    BoxMap,
    Global,
    UInt64,
    Txn,
    arc4,
    gtxn,
    itxn,
    String,
)

class CreditInfo(arc4.Struct):
    owner: arc4.Address
    limit: arc4.UInt64
    score: arc4.UInt64
    metadata_url: arc4.String

class CreditScoreNFT(ARC4Contract):
    admin: arc4.Address
    credit_score: UInt64
    credit_limit: UInt64
    metadata_ipfs: arc4.String

    def __init__(self) -> None:
        self.nft_map = BoxMap(arc4.UInt64, CreditInfo, key_prefix="bcsnft_")
        self.address_map = BoxMap(arc4.Address, arc4.UInt64, key_prefix="bcsaddr_")
        #self.admin = Global.creator_address.auth_address  # ✅ FIXED

    @abimethod
    def create(self, admin: arc4.Address, metadata_ipfs: arc4.String) -> None:
        self.admin = admin
        self.metadata_ipfs = metadata_ipfs
    
    @arc4.abimethod
    def mint(self, tokenId: arc4.UInt64, owner: arc4.Address, limit: arc4.UInt64, 
             score: arc4.UInt64, url: arc4.String) -> None:
        #assert Txn.sender == self.admin, "Only admin can update credit info"
        info = CreditInfo(owner, limit, score,url)
        self.nft_map[tokenId] = info.copy()
        self.address_map[owner] = tokenId

    @arc4.abimethod
    def get_credit_info(self, tokenId: arc4.UInt64) -> CreditInfo:
        return self.nft_map[tokenId]
    
    @arc4.abimethod
    def get_credit_info_by_address(self, owner: arc4.Address) -> CreditInfo:
        tokenId = self.address_map[owner]
        return self.nft_map[tokenId]
    
    @arc4.abimethod
    def get_metadata_url(self, tokenId: arc4.UInt64) -> arc4.String:
        return self.nft_map[tokenId].metadata_url
    
    @arc4.abimethod
    def update_credit_info_by_address(self, owner: arc4.Address, new_limit: arc4.UInt64, new_score: arc4.UInt64) -> None:
        #assert Txn.sender == self.admin, "Only admin can update credit info"
        tokenId = self.address_map[owner]
        info = self.nft_map[tokenId].copy()
        info.limit = new_limit
        info.score = new_score
        self.nft_map[tokenId] = info.copy()
    
    @arc4.abimethod
    def arc72_ownerOf(self, tokenId: arc4.UInt64) -> arc4.Address:
        return self.nft_map[tokenId].owner
    
    @arc4.abimethod
    def arc72_transferFrom(self, from_: arc4.Address, to: arc4.Address, tokenId: arc4.UInt64) -> None:
        # Soulbound: disallow all transfers
        assert False, "This NFT is soulbound and cannot be transferred"
    
    @abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name
    

