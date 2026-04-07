/**
 * HTTP-backed frontend data adapter.
 *
 * This adapter is selected when environment.useMockDataService is false.
 * Feature components still consume FrontendDataService and remain transport-agnostic.
 */
import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable, map } from 'rxjs';
import {
  JobSubmissionRequest,
  JobSubmissionResult,
  RunDetail,
  RunListingItem,
  ServiceHealthSnapshot,
  WorkflowSummary
} from '../models/frontend-contracts';
import {
  mapHealthApiResponseToSnapshot,
  mapJobSubmissionApiResponseToJobSubmissionResult,
  mapJobSubmissionRequestToApiRequest,
  mapRunDetailApiResponseToRunDetail,
  mapRunListItemApiResponseToRunListingItem,
  mapWorkflowSummaryApiResponseToWorkflowSummary
} from './mappers/frontend-api.mappers';
import { FrontendDataService } from './frontend-data.service';
import {
  HealthApiResponse,
  JobSubmissionApiResponse,
  RunDetailApiResponse,
  RunListItemApiResponse,
  WorkflowSummaryApiResponse
} from './transport/api-transport.contracts';

@Injectable()
export class ApiFrontendDataService extends FrontendDataService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiBaseUrl;

  getServiceHealth(): Observable<ServiceHealthSnapshot> {
    return this.http
      .get<HealthApiResponse>(`${this.baseUrl}/health/status`)
      .pipe(map((response) => mapHealthApiResponseToSnapshot(response, 'api')));
  }

  getRunHistory(): Observable<ReadonlyArray<RunListingItem>> {
    return this.http
      .get<ReadonlyArray<RunListItemApiResponse>>(`${this.baseUrl}/runs`)
      .pipe(map((items) => items.map(mapRunListItemApiResponseToRunListingItem)));
  }

  getRunDetail(runId: string): Observable<RunDetail | null> {
    return this.http
      .get<RunDetailApiResponse>(`${this.baseUrl}/runs/${runId}`)
      .pipe(map((response) => mapRunDetailApiResponseToRunDetail(response)));
  }

  getWorkflowCatalog(): Observable<ReadonlyArray<WorkflowSummary>> {
    return this.http
      .get<ReadonlyArray<WorkflowSummaryApiResponse>>(`${this.baseUrl}/workflows`)
      .pipe(map((items) => items.map(mapWorkflowSummaryApiResponseToWorkflowSummary)));
  }

  submitJob(request: JobSubmissionRequest): Observable<JobSubmissionResult> {
    return this.http
      .post<JobSubmissionApiResponse>(`${this.baseUrl}/jobs/submit`, mapJobSubmissionRequestToApiRequest(request))
      .pipe(map(mapJobSubmissionApiResponseToJobSubmissionResult));
  }
}
