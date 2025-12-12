from fastapi import APIRouter, Depends
from AI_Insights.service import InsightsService
from app.utils.auth_dependency import auth_user  # already existing

router = APIRouter(tags=["Insights"])

@router.get("/insights")
def insights(user_id: str = Depends(auth_user)):
    return {
        "categoryTrends": InsightsService.get_category_trends(user_id),
        "dailySpending": InsightsService.get_daily_spending(user_id)
    }

@router.get("/category-analysis")
def category_analysis(user_id: str = Depends(auth_user)):
    return {
        "categoryDistribution": InsightsService.get_category_distribution(user_id)
    }

@router.get("/recommendations")
def recs(user_id: str = Depends(auth_user)):
    return {
        "recommendations": InsightsService.get_recommendations(user_id)
    }
