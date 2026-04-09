/**
 * workflow-catalog-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowCatalogPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Subject, of, throwError } from 'rxjs';
import { WorkflowCatalogPageComponent } from './workflow-catalog-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('WorkflowCatalogPageComponent', () => {
  let component: WorkflowCatalogPageComponent;
  let fixture: ComponentFixture<WorkflowCatalogPageComponent>;
  let mockDataService: {
    getWorkflowCatalog: jasmine.Spy;
  };

  beforeEach(async () => {
    mockDataService = {
      getWorkflowCatalog: jasmine.createSpy('getWorkflowCatalog').and.returnValue(of([]))
    };

    await TestBed.configureTestingModule({
      imports: [WorkflowCatalogPageComponent],
      providers: [
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkflowCatalogPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should request the workflow catalog', () => {
    expect(TestBed.inject(FrontendDataService).getWorkflowCatalog).toHaveBeenCalled();
  });

  it('should show the loading state before the catalog resolves', () => {
    mockDataService.getWorkflowCatalog.and.returnValue(new Subject().asObservable());

    const loadingFixture = TestBed.createComponent(WorkflowCatalogPageComponent);
    loadingFixture.detectChanges();

    const element: HTMLElement = loadingFixture.nativeElement;
    expect(element.textContent).toContain('Loading workflow catalog...');
  });

  it('should render the returned workflows', () => {
    mockDataService.getWorkflowCatalog.and.returnValue(
      of([
        {
          workflowId: 'workflow-a',
          title: 'Workflow A',
          description: 'Description',
          tags: ['alpha'],
          version: '1.0.0'
        }
      ])
    );

    const successFixture = TestBed.createComponent(WorkflowCatalogPageComponent);
    successFixture.detectChanges();

    const element: HTMLElement = successFixture.nativeElement;
    expect(element.textContent).toContain('Workflow A');
    expect(element.textContent).toContain('workflow-a');
    expect(element.textContent).toContain('v1.0.0');
  });

  it('should show the error state when the catalog fails to load', () => {
    mockDataService.getWorkflowCatalog.and.returnValue(
      throwError(() => new Error('catalog exploded'))
    );

    const errorFixture = TestBed.createComponent(WorkflowCatalogPageComponent);
    errorFixture.detectChanges();

    const element: HTMLElement = errorFixture.nativeElement;
    expect(element.textContent).toContain('Unable to load workflow catalog: catalog exploded');
  });
});
