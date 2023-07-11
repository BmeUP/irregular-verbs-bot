from pydantic import BaseModel


class DictModel(BaseModel):
    first_form: str
    second_form: str
    third_form: str
    description: list[str]