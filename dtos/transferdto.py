from datetime import datetime
from decimal import Decimal

from dtos.views.transfersviewdto import TransfersViewDTO


class TransferDTO(TransfersViewDTO):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    time: datetime
