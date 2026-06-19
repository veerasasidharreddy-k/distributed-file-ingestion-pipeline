from collections.abc import Iterable

from src.models.chunk_state import ChunkStatus, FileChunk
from src.models.upload_state import ParentUpload, UploadStatus


class StatusAggregator:
    def aggregate(
        self,
        parent_upload: ParentUpload,
        chunks: Iterable[FileChunk],
    ) -> ParentUpload:
        chunk_statuses = [chunk.status for chunk in chunks]

        if not chunk_statuses:
            parent_upload.status = UploadStatus.PENDING
        elif any(
            status in {ChunkStatus.PENDING, ChunkStatus.IN_PROGRESS}
            for status in chunk_statuses
        ):
            parent_upload.status = UploadStatus.IN_PROGRESS
        elif all(status == ChunkStatus.SUCCESSFUL for status in chunk_statuses):
            parent_upload.status = UploadStatus.SUCCESSFUL
        elif all(status == ChunkStatus.FAILED for status in chunk_statuses):
            parent_upload.status = UploadStatus.FAILED
        else:
            parent_upload.status = UploadStatus.PARTIALLY_SUCCESSFUL

        return parent_upload
