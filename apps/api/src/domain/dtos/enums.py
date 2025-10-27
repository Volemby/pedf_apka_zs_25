import enum

from src.domain.enums import Role
from src.domain.enums import ArtStatus as OriginalStatus
from src.domain.enums import PrintStatus


class ArtEdition(enum.Enum):
    original = "original"
    print = "print"
    both = "Original & Print"