from src.models.chunk_state import ChunkStatus, FileChunk
from src.models.upload_state import ParentUpload, UploadStatus
from src.orchestration.status_aggregator import StatusAggregator


def make_parent_upload() -> ParentUpload:
    return ParentUpload(
        upload_id="upload-001",
        file_name="sample.csv",
        total_chunks=3,
        status=UploadStatus.PENDING,
    )


def make_chunk(chunk_id: int, status: ChunkStatus) -> FileChunk:
    return FileChunk(
        upload_id="upload-001",
        chunk_id=chunk_id,
        status=status,
        retry_count=0,
    )


def test_all_successful_chunks_produce_successful_parent_status() -> None:
    parent_upload = make_parent_upload()
    chunks = [
        make_chunk(1, ChunkStatus.SUCCESSFUL),
        make_chunk(2, ChunkStatus.SUCCESSFUL),
        make_chunk(3, ChunkStatus.SUCCESSFUL),
    ]

    result = StatusAggregator().aggregate(parent_upload, chunks)

    assert result.status == UploadStatus.SUCCESSFUL


def test_mixed_successful_and_failed_chunks_produce_partially_successful_status() -> None:
    parent_upload = make_parent_upload()
    chunks = [
        make_chunk(1, ChunkStatus.SUCCESSFUL),
        make_chunk(2, ChunkStatus.FAILED),
        make_chunk(3, ChunkStatus.SUCCESSFUL),
    ]

    result = StatusAggregator().aggregate(parent_upload, chunks)

    assert result.status == UploadStatus.PARTIALLY_SUCCESSFUL


def test_pending_or_in_progress_chunk_produces_in_progress_parent_status() -> None:
    parent_upload = make_parent_upload()
    chunks = [
        make_chunk(1, ChunkStatus.SUCCESSFUL),
        make_chunk(2, ChunkStatus.IN_PROGRESS),
        make_chunk(3, ChunkStatus.PENDING),
    ]

    result = StatusAggregator().aggregate(parent_upload, chunks)

    assert result.status == UploadStatus.IN_PROGRESS


def test_all_failed_chunks_produce_failed_parent_status() -> None:
    parent_upload = make_parent_upload()
    chunks = [
        make_chunk(1, ChunkStatus.FAILED),
        make_chunk(2, ChunkStatus.FAILED),
        make_chunk(3, ChunkStatus.FAILED),
    ]

    result = StatusAggregator().aggregate(parent_upload, chunks)

    assert result.status == UploadStatus.FAILED
