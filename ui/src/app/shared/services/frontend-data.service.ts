/**
 * Frontend data service abstraction for MagnetarPrometheus.
 *
 * Design intent:
 * - This abstraction is the only API that feature pages should depend on.
 * - The concrete implementation can be mock-backed today and HTTP-backed later.
 * - This keeps route components simple, focused on rendering state transitions.
 */
import { Observable } from 'rxjs';
import {
  JobSubmissionRequest,
  JobSubmissionResult,
  RunDetail,
  RunListingItem,
  ServiceHealthSnapshot,
  WorkflowSummary
} from '../models/frontend-contracts';

export abstract class FrontendDataService {
  /**
   * Fetches the current health status of the backend services.
   *
   * @returns An Observable emitting a snapshot of service health, including status, mode, and timestamp.
   */
  public abstract getServiceHealth(): Observable<ServiceHealthSnapshot>;

  /**
   * Retrieves a list of all historical and current workflow runs.
   *
   * @returns An Observable emitting a read-only array of run listing items for the dashboard and history views.
   */
  public abstract getRunHistory(): Observable<ReadonlyArray<RunListingItem>>;

  /**
   * Fetches detailed information for a specific workflow run.
   *
   * @param runId - The unique identifier of the run to retrieve.
   * @returns An Observable emitting the detailed run state or null if the run is not found.
   */
  public abstract getRunDetail(runId: string): Observable<RunDetail | null>;

  /**
   * Retrieves the catalog of available workflows that can be submitted or inspected.
   *
   * @returns An Observable emitting a read-only array of workflow summaries.
   */
  public abstract getWorkflowCatalog(): Observable<ReadonlyArray<WorkflowSummary>>;

  /**
   * Submits a new workflow job for execution.
   *
   * @param request - The job submission details, including workflow ID and execution parameters.
   * @returns An Observable emitting the result of the submission, including the new run ID if accepted.
   */
  public abstract submitJob(request: JobSubmissionRequest): Observable<JobSubmissionResult>;
}
