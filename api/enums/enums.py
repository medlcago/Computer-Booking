from enum import Enum


class TicketStatus(str, Enum):
    open = "open"
    closed = "closed"


class ComputerCategories(str, Enum):
    vip = "VIP"
    regular = "Regular"
