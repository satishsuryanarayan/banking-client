from datetime import datetime

from dtos.views.accountsviewdto import AccountsViewDTO


class AccountDTO(AccountsViewDTO):
    id: int
    customer_id: int
    creation_time: datetime
