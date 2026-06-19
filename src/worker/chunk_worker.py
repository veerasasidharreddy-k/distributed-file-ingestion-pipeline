from src.models.chunk_state import ChunkStatus, FileChunk
from src.models.queue_message import ChunkProcessingMessage


class ChunkWorker:
    def process(self, message: ChunkProcessingMessage) -> FileChunk:
        return FileChunk(
            upload_id=message.upload_id,
            chunk_id=message.chunk_id,
            status=ChunkStatus.SUCCESSFUL,
            retry_count=0,
        )
