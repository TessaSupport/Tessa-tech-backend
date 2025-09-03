from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    ONGOING = "ongoing"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class SenderType(str, Enum):
    USER = "user"
    AI = "ai"
    AGENT = "agent"