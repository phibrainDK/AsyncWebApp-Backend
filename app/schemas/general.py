from pydantic import PositiveInt

from common.enums import OrderOption


class PaginationParams:
    def __init__(
        self,
        order: OrderOption = OrderOption.ASCENDING,
        page: PositiveInt = 1,
        page_size: PositiveInt = 10,
    ):
        self.page = page
        self.page_size = page_size
        self.order = order
