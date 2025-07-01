from dtos.views.basedto import BaseDTO


class CustomersViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "CustomersView"
