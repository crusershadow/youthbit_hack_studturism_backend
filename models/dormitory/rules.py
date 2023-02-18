from pydantic import BaseModel


class RuleCreate(BaseModel):
    required_uni_documents: str
    required_student_documents: str
    committee_name: str = None
    committee_email: str = None
    committee_phone: str = None


class Rule(RuleCreate):
    rule_id: int