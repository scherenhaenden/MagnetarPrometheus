/**
 * run-history-page.component.spec.ts intent header.
 *
 * This test validates the RunHistoryPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { RunHistoryPageComponent } from './run-history-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('RunHistoryPageComponent', () => {
  let component: RunHistoryPageComponent;
  let fixture: ComponentFixture<RunHistoryPageComponent>;

  beforeEach(async () => {
    const mockDataService = {
      getRunHistory: jasmine.createSpy('getRunHistory').and.returnValue(of([
        {
          runId: 'run-1',
          workflowId: 'workflow-a',
          status: 'succeeded',
          createdAtIso: '2026-04-09T10:00:00Z',
          completedAtIso: '2026-04-09T10:00:01Z',
          summary: 'Done'
        }
      ]))
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
});
