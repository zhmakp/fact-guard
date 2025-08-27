import { apiClient } from './api';

export interface LibrarySource {
  source_name: string;
  source_url: string;
  source_type: string;
  chunk_count: number;
}

export class LibraryService {
  async getSources(): Promise<LibrarySource[]> {
    return apiClient.get<LibrarySource[]>('/api/library');
  }

  async deleteSource(sourceId: string): Promise<{ message: string }> {
    return apiClient.delete<{ message: string }>(`/api/library/${sourceId}`);
  }
}

export const libraryService = new LibraryService();