/**
 * workflow-studio-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowStudioPageComponent.
 */
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { WorkflowStudioPageComponent } from './workflow-studio-page.component';

describe('WorkflowStudioPageComponent', () => {
  let component: WorkflowStudioPageComponent;
  let fixture: ComponentFixture<WorkflowStudioPageComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WorkflowStudioPageComponent],
      providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkflowStudioPageComponent);
    component = fixture.componentInstance;

    const initialRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.yaml');
    initialRequest.flush('id: support_ticket_triage');
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the studio shell in English', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.querySelector('h2')?.textContent).toContain('Workflow Studio');
    expect(element.textContent).toContain('Visual editor workspace for building, testing, and debugging workflows.');
    expect(element.textContent).toContain('Saved Example Workflow');
    expect(element.textContent).toContain('id: support_ticket_triage');
  });

  it('should request and render the JSON workflow example when selected', () => {
    const element: HTMLElement = fixture.nativeElement;
    const jsonButton = Array.from(element.querySelectorAll('.example-tab')).find(
      (button) => button.textContent?.trim() === 'JSON'
    ) as HTMLButtonElement;

    jsonButton.click();

    const request = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    request.flush('{"id": "support_ticket_triage"}');
    fixture.detectChanges();

    expect(element.textContent).toContain('{"id": "support_ticket_triage"}');
  });
});
