from typing import Sequence

from fastapi import status


class BaseApplicationError(Exception):
    message: str = ""
    status: int = status.HTTP_400_BAD_REQUEST


class ApplicationError(BaseApplicationError):
    def __init__(self, context: str | None = None, message: str | None = None) -> None:
        self._context = context
        if message:
            self.message = message

    @property
    def context(self) -> dict:
        return {"detail": self._context}


class BadJWTTokenError(ApplicationError):
    message = "Невозможно обработать переданный JWT токен"


class AccessDeniedError(ApplicationError):
    message = "Доступ запрещен"
    status = status.HTTP_403_FORBIDDEN


class DatabaseAccessError(ApplicationError):
    message = "Ошибка доступа к базе данных"
    status = status.HTTP_500_INTERNAL_SERVER_ERROR


class FieldBasedError(ApplicationError):
    message = "Произошла ошибка при обработке тела запроса"
    context_message = "Произошла ошибка при обработке поля: {field}"

    def __init__(
        self,
        fields: Sequence,
        message: str | None = None,
        context_message: str | None = None,
    ) -> None:
        self.fields = fields
        if message:
            self.message = message
        if context_message:
            self.context_message = context_message

    @property
    def context(self) -> dict:
        return {field: self.context_message.format(field=field) for field in self.fields}


class ObjectNotFoundError(FieldBasedError):
    message = "Объект не найден"
    context_message = "Объект с таким {field} не найден"
    status = status.HTTP_404_NOT_FOUND


class ObjectAlreadyExistsError(FieldBasedError):
    message = "Объект с такими данными уже существует"
    context_message = "Объект с таким {field} уже существует"
    status = status.HTTP_409_CONFLICT
