from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import NFTReward, User
from app.schemas import NFTRewardCreate, NFTRewardResponse
from app.auth import get_current_user
import os
from web3 import Web3
from eth_account import Account
import json

router = APIRouter(prefix="/api/nft", tags=["nft"])

@router.post("/mint", response_model=NFTRewardResponse)
async def mint_nft(
    nft_data: NFTRewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ethereum_rpc_url = os.getenv("ETHEREUM_RPC_URL")
    if not ethereum_rpc_url:
        raise HTTPException(status_code=500, detail="Ethereum RPC URL not configured")
    
    try:
        w3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))
        
        if not w3.is_connected():
            raise HTTPException(status_code=500, detail="Failed to connect to Ethereum network")
        
        nft_contract_address = os.getenv("NFT_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
        
        db_nft = NFTReward(
            user_id=current_user.id,
            token_id=nft_data.token_id,
            contract_address=nft_contract_address,
            nft_metadata=nft_data.nft_metadata,
            achievement_type=nft_data.achievement_type
        )
        
        db.add(db_nft)
        db.commit()
        db.refresh(db_nft)
        
        return db_nft
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mint NFT: {str(e)}")

@router.get("/{user_id}", response_model=List[NFTRewardResponse])
async def get_user_nfts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role.value not in ["teacher", "parent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view these NFTs")
    
    nfts = db.query(NFTReward).filter(NFTReward.user_id == user_id).all()
    return nfts
