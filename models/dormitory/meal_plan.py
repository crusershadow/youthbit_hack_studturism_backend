from pydantic import BaseModel


class MealPlanCreate(BaseModel):
    meal_plan_name: str


class MealPlan(MealPlanCreate):
    meal_plan_id: int