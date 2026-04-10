/**
 * HTTP-backed frontend data adapter for MagnetarPrometheus.
 *
 * This adapter is selected when environment.useMockDataService is false.
 * It provides the concrete implementation for FrontendDataService by
 * communicating with the backend API service via Angular's HttpClient.
 *
 * Design intent:
 * - Feature components still consume the abstract FrontendDataService and remain transport-agnostic.
 * - This adapter handles API transport details, such as endpoint URL construction and mapper orchestration.
 * - It relies on FrontendApiMappers to transform raw API JSON payloads into stable frontend contracts.
 */
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable, catchError, map, of, throwError } from 'rxjs';
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

  /**
   * Fetches the current health status from the backend API.
   *
   * Calls the /health/status endpoint and maps the raw response to a service health snapshot
   * using mapHealthApiResponseToSnapshot, marking the mode as 'api'.
   *
   * @returns An Observable of the service health snapshot.
   */
  public getServiceHealth(): Observable<ServiceHealthSnapshot> {
    return this.http
      .get<HealthApiResponse>(`${this.baseUrl}/health/status`)
      .pipe(map((response) => mapHealthApiResponseToSnapshot(response, 'api')));
  }

  /**
   * Retrieves the full history of workflow runs from the backend.
   *
   * Fetches from the /runs endpoint and maps the resulting array of API response items
   * to their stable frontend RunListingItem representation.
   *
   * @returns An Observable of a read-only array of run listing items.
   */
  public getRunHistory(): Observable<ReadonlyArray<RunListingItem>> {
    return this.http
      .get<ReadonlyArray<RunListItemApiResponse>>(`${this.baseUrl}/runs`)
      .pipe(map((items) => items.map(mapRunListItemApiResponseToRunListingItem)));
  }

  /**
   * Fetches detailed state for a specific run from the backend.
   *
   * Requests /runs/:runId and safely maps the result, handling potential null responses.
   *
   * @param runId - The ID of the run to fetch.
   * @returns An Observable of the run detail or null if not found.
   */
  public getRunDetail(runId: string): Observable<RunDetail | null> {
    return this.http
      .get<RunDetailApiResponse>(`${this.baseUrl}/runs/${encodeURIComponent(runId)}`)
      .pipe(
        map((response) => mapRunDetailApiResponseToRunDetail(response)),
        catchError((error: HttpErrorResponse) =>
          error.status === 404 ? of(null) : throwError(() => error)
        )
      );
  }

  /**
   * Retrieves the catalog of all available workflows.
   *
   * Fetches from the /workflows endpoint and maps the result using mapWorkflowSummaryApiResponseToWorkflowSummary.
   *
   * @returns An Observable of a read-only array of workflow summaries.
   */
  public getWorkflowCatalog(): Observable<ReadonlyArray<WorkflowSummary>> {
    return this.http
      .get<ReadonlyArray<WorkflowSummaryApiResponse>>(`${this.baseUrl}/workflows`)
      .pipe(map((items) => items.map(mapWorkflowSummaryApiResponseToWorkflowSummary)));
  }

  /**
   * Submits a new job request for execution to the backend API.
   *
   * Maps the frontend JobSubmissionRequest into the format expected by the API,
   * posts to /jobs/submit, and returns the result mapped into a stable JobSubmissionResult.
   *
   * @param request - The job submission parameters.
   * @returns An Observable of the job submission outcome.
   */
  public submitJob(request: JobSubmissionRequest): Observable<JobSubmissionResult> {
    return this.http
      .post<JobSubmissionApiResponse>(`${this.baseUrl}/jobs/submit`, mapJobSubmissionRequestToApiRequest(request))
      .pipe(map(mapJobSubmissionApiResponseToJobSubmissionResult));
  }
}
