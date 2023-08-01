from pydantic import BaseModel, Field


class HandledExceptionSchema(BaseModel):
    message: str
    context: dict


class HandledValidationExceptionSchema(HandledExceptionSchema):
    context: list = Field(
        example=[
            [
                {
                    "loc": ["loc(body/query/nested/)", "field"],
                    "msg": "field required",
                    "type": "type_error.missing",
                }
            ]
        ]
    )
