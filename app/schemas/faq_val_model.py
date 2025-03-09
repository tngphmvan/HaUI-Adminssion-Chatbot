from pydantic import Field, BaseModel

class EvalFAQ(BaseModel):
    is_relevant: bool = Field(description="Câu hỏi có liên quan đến FAQ không", title="Is Relevant")