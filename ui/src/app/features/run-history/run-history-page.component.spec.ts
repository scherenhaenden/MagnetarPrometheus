/**
 * run-history-page.component.spec.ts intent header.
 *
 * This test validates the RunHistoryPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Subject, of, throwError } from 'rxjs';
import { RunHistoryPageComponent } from './run-history-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('RunHistoryPageComponent', () => {
  let component: RunHistoryPageComponent;
  let fixture: ComponentFixture<RunHistoryPageComponent>;
  let mockDataService: {
    getRunHistory: jasmine.Spy;
  };

  const runHistoryItems = [
    {
      runId: 'run-1',
      workflowId: 'workflow-a',
      status: 'succeeded',
      createdAtIso: '2026-04-09T10:00:00Z',
      completedAtIso: '2026-04-09T10:00:01Z',
      summary: 'Done'
    },
    {
      runId: 'run-2',
      workflowId: 'workflow-b',
      status: 'failed',
      createdAtIso: '2026-04-09T11:00:00Z',
      completedAtIso: '2026-04-09T11:00:01Z',
      summary: 'Failed'
    }
  ];

  beforeEach(async () => {
    mockDataService = {
      getRunHistory: jasmine.createSpy('getRunHistory').and.returnValue(of(runHistoryItems))
    };

    await TestBed.configureTestingModule({
      imports: [RunHistoryPageComponent, RouterTestingModule],
      providers: [
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RunHistoryPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the filter controls', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('input[formcontrolname="search"]')).withContext('search input').not.toBeNull();
    expect(element.querySelector('select[formcontrolname="status"]')).withContext('status select').not.toBeNull();
  });

  it('should show the loading state before run history resolves', () => {
    mockDataService.getRunHistory.and.returnValue(new Subject().asObservable());

    const loadingFixture = TestBed.createComponent(RunHistoryPageComponent);
    loadingFixture.detectChanges();

    const element: HTMLElement = loadingFixture.nativeElement;
    expect(element.textContent).toContain('Loading run history...');
  });

  it('should filter runs by search query and status', () => {
    component['filterForm'].setValue({ search: 'run-2', status: 'failed' });
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.textContent).toContain('run-2');
    expect(element.textContent).toContain('workflow-b');
    expect(element.textContent).not.toContain('run-1');
  });

  it('should show the empty-state message when filters exclude all runs', () => {
    component['filterForm'].setValue({ search: 'missing', status: 'all' });
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    expect(element.textContent).toContain('No runs match the current filters.');
  });

  it('should show the error state when run history fails to load', () => {
    mockDataService.getRunHistory.and.returnValue(
      throwError(() => new Error('run history exploded'))
    );

    const errorFixture = TestBed.createComponent(RunHistoryPageComponent);
    errorFixture.detectChanges();

    const element: HTMLElement = errorFixture.nativeElement;
    expect(element.textContent).toContain('Unable to load run history: run history exploded');
  });
});
