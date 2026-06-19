from src.models.queue_message import ChunkProcessingMessage
from src.models.upload_state import ParentUpload, UploadStatus
from src.orchestration.status_aggregator import StatusAggregator
from src.worker.chunk_worker import ChunkWorker


def main() -> None:
    parent_upload = ParentUpload(
        upload_id="upload-001",
        file_name="sample-large-file.csv",
        total_chunks=3,
        status=UploadStatus.PENDING,
    )

    messages = [
        ChunkProcessingMessage(
            upload_id=parent_upload.upload_id,
            chunk_id=chunk_id,
            source_path=f"/incoming/{parent_upload.file_name}.part{chunk_id}",
            target_path=f"/processed/{parent_upload.file_name}.part{chunk_id}",
        )
        for chunk_id in range(1, parent_upload.total_chunks + 1)
    ]

    worker = ChunkWorker()
    processed_chunks = [worker.process(message) for message in messages]

    aggregator = StatusAggregator()
    final_upload = aggregator.aggregate(parent_upload, processed_chunks)

    for chunk in processed_chunks:
        print(f"chunk_id={chunk.chunk_id} status={chunk.status.value}")

    print(f"parent_upload_id={final_upload.upload_id} status={final_upload.status.value}")


if __name__ == "__main__":
    main()
