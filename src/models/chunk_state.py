from dataclasses import dataclass
from enum import Enum


class ChunkStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    FAILED = "failed"


@dataclass
class FileChunk:
    upload_id: str
    chunk_id: int
    status: ChunkStatus
    retry_count: int
