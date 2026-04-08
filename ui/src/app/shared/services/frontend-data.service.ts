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
  public abstract getServiceHealth(): Observable<ServiceHealthSnapshot>;
  public abstract getRunHistory(): Observable<ReadonlyArray<RunListingItem>>;
  public abstract getRunDetail(runId: string): Observable<RunDetail | null>;
  public abstract getWorkflowCatalog(): Observable<ReadonlyArray<WorkflowSummary>>;
  public abstract submitJob(request: JobSubmissionRequest): Observable<JobSubmissionResult>;
}
