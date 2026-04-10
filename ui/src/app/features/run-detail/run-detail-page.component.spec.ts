/**
 * run-detail-page.component.spec.ts intent header.
 *
 * This test validates the RunDetailPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { BehaviorSubject, Subject, of, throwError } from 'rxjs';
import { RunDetailPageComponent } from './run-detail-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('RunDetailPageComponent', () => {
  let component: RunDetailPageComponent;
  let fixture: ComponentFixture<RunDetailPageComponent>;
  let routeParamMap$: BehaviorSubject<ReturnType<typeof convertToParamMap>>;
  let mockDataService: {
    getRunDetail: jasmine.Spy;
  };

  beforeEach(async () => {
    routeParamMap$ = new BehaviorSubject(convertToParamMap({ runId: 'run-1' }));
    mockDataService = {
      getRunDetail: jasmine.createSpy('getRunDetail').and.returnValue(of(null))
    };

    await TestBed.configureTestingModule({
      imports: [RunDetailPageComponent, RouterTestingModule],
      providers: [
        { provide: ActivatedRoute, useValue: { paramMap: routeParamMap$.asObservable() } },
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RunDetailPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should request the selected run', () => {
    expect(TestBed.inject(FrontendDataService).getRunDetail).toHaveBeenCalledWith('run-1');
  });

  it('should fall back to an empty run id when the route parameter is missing', async () => {
    routeParamMap$.next(convertToParamMap({}));
    fixture.detectChanges();

    expect(mockDataService.getRunDetail).toHaveBeenCalledWith('');
  });

  it('should show the loading state before the selected run resolves', () => {
    mockDataService.getRunDetail.and.returnValue(new Subject().asObservable());

    const loadingFixture = TestBed.createComponent(RunDetailPageComponent);
    loadingFixture.detectChanges();

    const element: HTMLElement = loadingFixture.nativeElement;
    expect(element.textContent).toContain('Loading run detail...');
  });

  it('should render the run detail when the selected run is found', () => {
    mockDataService.getRunDetail.and.returnValue(
      of({
        runId: 'run-1',
        workflowId: 'workflow-a',
        status: 'succeeded',
        createdAtIso: '2026-04-09T10:00:00Z',
        completedAtIso: '2026-04-09T10:00:01Z',
        steps: [{ name: 'collect-input', state: 'done', detail: 'Collected input.' }],
        errorMessage: null,
        outputPreview: 'Preview'
      })
    );

    const successFixture = TestBed.createComponent(RunDetailPageComponent);
    successFixture.detectChanges();

    const element: HTMLElement = successFixture.nativeElement;
    expect(element.textContent).toContain('run-1');
    expect(element.textContent).toContain('Workflow: workflow-a');
    expect(element.textContent).toContain('Output preview: Preview');
    expect(element.textContent).toContain('collect-input');
  });

  it('should show the not-found state when the selected run does not exist', () => {
    mockDataService.getRunDetail.and.returnValue(of(null));

    const notFoundFixture = TestBed.createComponent(RunDetailPageComponent);
    notFoundFixture.detectChanges();

    const element: HTMLElement = notFoundFixture.nativeElement;
    expect(element.textContent).toContain('No run found for the selected identifier.');
  });

  it('should show the error state when the selected run fails to load', () => {
    mockDataService.getRunDetail.and.returnValue(
      throwError(() => new Error('run detail exploded'))
    );

    const errorFixture = TestBed.createComponent(RunDetailPageComponent);
    errorFixture.detectChanges();

    const element: HTMLElement = errorFixture.nativeElement;
    expect(element.textContent).toContain('Unable to load run detail: run detail exploded');
  });
});
