from pydantic import EmailStr

from dtos.views.usersviewdto import UsersViewDTO


class UserDTO(UsersViewDTO):
    username: str
    password: str
    email: EmailStr
