import type { UploadResponse } from '../types/api';
import type { UploadMetadata } from '../types/factCheck';
import { apiClient } from './api';

export class UploadService {
  async uploadFile(file: File, metadata: UploadMetadata): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source_name', metadata.source_name);
    formData.append('source_type', metadata.source_type);
    if (metadata.description) {
      formData.append('description', metadata.description);
    }
    formData.append('is_trusted', metadata.is_trusted.toString());

    return apiClient.upload<UploadResponse>('/api/upload', formData);
  }
}

export const uploadService = new UploadService();