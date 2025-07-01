from dtos.views.basedto import BaseDTO


class UsersViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "UsersView"
