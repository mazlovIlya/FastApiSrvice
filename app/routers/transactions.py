from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    # Проверка существования категории и пользователя
    db_category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=list[schemas.Transaction])
def get_transactions(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(database.get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int, 
    transaction_update: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db)
):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Проверка существования категории и пользователя
    db_category = db.query(models.Category).filter(models.Category.id == transaction_update.category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_user = db.query(models.User).filter(models.User.id == transaction_update.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in transaction_update.dict().items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(database.get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return