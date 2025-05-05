from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.services import recommendation_service

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

@router.get("/", response_model=dict)
def get_recommendations(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    if not transactions:
        return {"message": "No transactions found for the user"}
    
    recommendations = recommendation_service.analyze_expenses(transactions)
    return recommendations