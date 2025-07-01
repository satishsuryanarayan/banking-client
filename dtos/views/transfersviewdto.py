from dtos.views.basedto import BaseDTO


class TransfersViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "TransfersView"
