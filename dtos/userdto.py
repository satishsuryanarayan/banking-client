from pydantic import EmailStr

from dtos.views.usersviewdto import UsersViewDTO


class UserDTO(UsersViewDTO):
    username: str
    password: str
    email: EmailStr

    def __init__(self, **data):
        super().__init__(**data)
