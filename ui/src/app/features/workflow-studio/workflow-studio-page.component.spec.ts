/**
 * workflow-studio-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowStudioPageComponent.
 */
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { WorkflowStudioPageComponent } from './workflow-studio-page.component';

describe('WorkflowStudioPageComponent', () => {
  let component: WorkflowStudioPageComponent;
  let fixture: ComponentFixture<WorkflowStudioPageComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    localStorage.clear();

    await TestBed.configureTestingModule({
      imports: [WorkflowStudioPageComponent],
      providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);

    fixture = TestBed.createComponent(WorkflowStudioPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    const initialRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.yaml');
    initialRequest.flush('id: support_ticket_triage');
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render header, workflow rail and default example', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('.brand-block h2')?.textContent).toContain('Workflow Studio');
    expect(element.textContent).toContain('Editor visual funcional');
    expect(element.querySelector('.workflow-rail')?.getAttribute('aria-label')).toBe('Workflow shortcuts');
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

  it('should ignore stale example responses when switching tabs quickly', () => {
    const studio = component as any;
    const jsonExample = studio.examples.find((example: any) => example.format === 'json');
    const tomlExample = studio.examples.find((example: any) => example.format === 'toml');

    studio.selectExample(jsonExample);
    studio.selectExample(tomlExample);

    const jsonRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    const tomlRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.toml');

    tomlRequest.flush('id = "support_ticket_triage"');
    jsonRequest.flush('{"id":"stale"}');

    expect(studio.selectedExample.path).toBe('/assets/workflows/examples/support-ticket-triage.toml');
    expect(studio.exampleContent).toBe('id = "support_ticket_triage"');
  });

  it('should persist and restore a local project snapshot and open tab', () => {
    const studio = component as any;

    studio.projectName = 'My Local Project';
    studio.updateSelectedNodeLabel('Edited Name');
    studio.saveProject();
    const storedId = studio.savedProjects[0]?.id;

    studio.newProject();
    studio.loadProject(storedId);

    expect(studio.projectName).toBe('My Local Project');
    expect(studio.selectedNode?.label ?? '').toBe('Edited Name');
    expect(studio.openProjectTabs.some((tab: any) => tab.id === storedId)).toBeTrue();
  });

  it('should filter saved projects by search text', () => {
    const studio = component as any;
    studio.projectName = 'Ventas';
    studio.saveProject();
    studio.newProject();
    studio.projectName = 'Soporte';
    studio.saveProject();

    studio.projectSearch = 'ven';
    expect(studio.filteredProjects.length).toBe(1);
    expect(studio.filteredProjects[0].name).toBe('Ventas');
  });

  it('should build visible connections and update them after drag', () => {
    const studio = component as any;
    const originalX2 = studio.visibleConnections[0].x2;

    studio.onNodePointerDown({ button: 0, pointerId: 3, clientX: 100, clientY: 100 } as PointerEvent, 'node_ai');
    studio.onDocumentPointerMove({ pointerId: 3, clientX: 140, clientY: 110, preventDefault: () => {}, cancelable: true } as unknown as PointerEvent);

    expect(studio.visibleConnections.length).toBeGreaterThan(0);
    expect(studio.visibleConnections[0].x2).not.toBe(originalX2);
  });

  it('should close non-draft tabs and keep draft tab protected', () => {
    const studio = component as any;
    studio.projectName = 'Closable';
    studio.saveProject();
    const projectId = studio.selectedProjectId;

    studio.closeTab('draft');
    expect(studio.openProjectTabs.some((tab: any) => tab.id === 'draft')).toBeTrue();

    studio.closeTab(projectId);
    expect(studio.openProjectTabs.some((tab: any) => tab.id === projectId)).toBeFalse();
  });
});
