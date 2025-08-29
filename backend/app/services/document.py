from fastapi import UploadFile
import io
from typing import List, Dict, Any
from app.models.requests import UploadMetadata
from app.services.vector_store import vector_store_service
from app.core.chunking import text_chunker
import logging
from docling.document_converter import DocumentConverter
import tempfile
import os

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for processing documents (PDF, TXT)."""
    def __init__(self):
        self.converter = DocumentConverter()

    async def process_uploaded_file(
        self,
        upload_id: str,
        file: UploadFile,
        metadata: UploadMetadata
    ) -> Dict[str, Any]:
        """Process an uploaded file and store it in the vector database"""
        try:
            # Read file content
            file_content = await file.read()
            # Extract text based on file type
            if metadata.source_type == "pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file_content)
                    tmp_file_path = tmp_file.name
                    doc = self.converter.convert(source=tmp_file_path)
                    text = doc.document.export_to_markdown()
            elif metadata.source_type == "text":
                text = file_content.decode("utf-8")
            else:
                raise ValueError(
                    f"Unsupported file type: {metadata.source_type}")

            # Chunk the text
            chunks = text_chunker.chunk_text(text)

            # Prepare chunks for storage
            document_chunks = []
            for i, chunk in enumerate(chunks):
                document_chunks.append({
                    "text": chunk,
                    "source_name": metadata.source_name,
                    "source_url": f"upload://{upload_id}",
                    "source_type": "user_upload",
                    "page": 0,  # Could be enhanced to track actual pages
                    "chunk_index": i
                })

            # Store in vector database
            point_ids = await vector_store_service.store_document_chunks(document_chunks)

            logger.info(
                f"Processed upload {upload_id}: {len(chunks)} chunks created")

            return {
                "chunks_processed": len(chunks),
                "point_ids": point_ids,
                "text_length": len(text)
            }

        except Exception as e:
            logger.error(f"Error processing upload {upload_id}: {str(e)}")
            raise

    async def _extract_csv_text(self, csv_content: bytes) -> str:
        """Extract and format text from CSV content (future implementation)"""
        # This would be implemented for CSV processing
        return csv_content.decode("utf-8")


# Global service instance
document_service = DocumentService()
