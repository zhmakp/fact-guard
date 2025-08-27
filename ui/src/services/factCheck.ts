import type { JobResponse, JobStatusResponse } from "../types/api";
import type { FactCheckInput } from "../types/factCheck";
import { apiClient } from "./api";

export class FactCheckService {
  async submitCheck(input: FactCheckInput): Promise<JobResponse> {
    return apiClient.post<JobResponse>('/api/check', input);
  }

  async getJobStatus(jobId: string): Promise<JobStatusResponse> {
    return apiClient.get<JobStatusResponse>(`/api/job/${jobId}`);
  }
}

export const factCheckService = new FactCheckService();