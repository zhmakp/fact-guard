import { apiClient } from './api';

export interface LibrarySource {
  source_name: string;
  source_url: string;
  source_type: string;
  chunk_count: number;
}

export interface AddSourceRequest {
  source_name: string;
  source_url: string;
  source_type: 'paper' | 'webpage' | 'news' | 'user_upload';
}

export class LibraryService {
  async getSources(): Promise<LibrarySource[]> {
    return apiClient.get<LibrarySource[]>('/api/library');
  }

  async addSource(request: AddSourceRequest): Promise<{ source_id: string; message: string }> {
    return apiClient.post<{ source_id: string; message: string }>('/api/library', request);
  }

  async deleteSource(sourceId: string): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(`/api/library/${sourceId}`);
  }
}

export const libraryService = new LibraryService();