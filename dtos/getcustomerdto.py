from typing import Self

from pydantic import model_validator

from dtos.views.customersviewdto import CustomersViewDTO


class GetCustomerDTO(CustomersViewDTO):
    customer_id: int

    def __init__(self, **data):
        super().__init__(**data)
        self.method = "get_customer"
