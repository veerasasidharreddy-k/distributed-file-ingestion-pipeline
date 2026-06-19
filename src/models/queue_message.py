from dataclasses import dataclass


@dataclass
class ChunkProcessingMessage:
    upload_id: str
    chunk_id: int
    source_path: str
    target_path: str
