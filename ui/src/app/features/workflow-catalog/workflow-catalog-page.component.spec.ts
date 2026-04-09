/**
 * workflow-catalog-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowCatalogPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { WorkflowCatalogPageComponent } from './workflow-catalog-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('WorkflowCatalogPageComponent', () => {
  let component: WorkflowCatalogPageComponent;
  let fixture: ComponentFixture<WorkflowCatalogPageComponent>;

  beforeEach(async () => {
    const mockDataService = {
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
});
