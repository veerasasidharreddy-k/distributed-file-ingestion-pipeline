from dataclasses import dataclass
from enum import Enum


class UploadStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    PARTIALLY_SUCCESSFUL = "partially_successful"
    FAILED = "failed"


@dataclass
class ParentUpload:
    upload_id: str
    file_name: str
    total_chunks: int
    status: UploadStatus
