from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"

class SenderType(str, Enum):
    USER = "user"
    AI = "ai"
    AGENT = "agent"