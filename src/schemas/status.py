from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    ONGOING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"

class SenderType(str, Enum):
    USER = "user"
    AI = "ai"
    AGENT = "agent"
