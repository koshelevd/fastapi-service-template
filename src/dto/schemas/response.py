from pydantic import BaseModel, Field


class BaseBadResponse(BaseModel):
    message: str = Field(example="Произошла ошибка при обработке запроса")
    context: dict | None = Field(example={"field_name": "error"})


class Response400(BaseBadResponse):
    ...


class Response401(BaseBadResponse):
    ...


class Response402(BaseBadResponse):
    message = "Недостаточно средств"


class Response403(BaseBadResponse):
    ...


class Response404(BaseBadResponse):
    message = "Не найдено"


class Response409(BaseBadResponse):
    message = "Объект с такими данными уже существует"


class Response500(BaseBadResponse):
    message = "Внутренняя ошибка сервера"


class Response501(Response500):
    ...


class Response502(Response500):
    ...


class Response520(Response500):
    ...


RESPONSE_200 = {200: {"content": {"application/json": {"example": {"detail": "ok"}}}}}
RESPONSE_400 = {400: {"model": Response400}}
RESPONSE_401 = {401: {"model": Response401}}
RESPONSE_402 = {402: {"model": Response402}}
RESPONSE_403 = {403: {"model": Response403}}
RESPONSE_404 = {404: {"model": Response404}}
RESPONSE_409 = {409: {"model": Response409}}
RESPONSE_500 = {500: {"model": Response500}}
RESPONSE_501 = {501: {"model": Response501}}
RESPONSE_502 = {502: {"model": Response502}}
RESPONSE_520 = {520: {"model": Response520}}
FAIL_RESPONSES = (
    RESPONSE_400
    | RESPONSE_401
    | RESPONSE_403
    | RESPONSE_409
    | RESPONSE_500
    | RESPONSE_501
    | RESPONSE_502
    | RESPONSE_520
)
