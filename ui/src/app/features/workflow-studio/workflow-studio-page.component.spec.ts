/**
 * workflow-studio-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowStudioPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { WorkflowStudioPageComponent } from './workflow-studio-page.component';

describe('WorkflowStudioPageComponent', () => {
  let component: WorkflowStudioPageComponent;
  let fixture: ComponentFixture<WorkflowStudioPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WorkflowStudioPageComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkflowStudioPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the redesigned studio shell in English', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.querySelector('h2')?.textContent).toContain('Workflow Studio');
    expect(element.textContent).toContain('Visual editor workspace for building, testing, and debugging workflows.');
    expect(element.textContent).toContain('Run Workflow');
    expect(element.textContent).toContain('Add Node');
    expect(element.querySelector('.library')?.getAttribute('aria-label')).toBe('Node Library');
  });
});
