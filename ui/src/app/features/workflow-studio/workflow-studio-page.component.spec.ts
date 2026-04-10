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

  it('should render the redesigned studio header, layout, and default example', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('.brand-block h2')?.textContent).toContain('Workflow Studio');
    expect(element.textContent).toContain('Visual editor workspace for building, testing, and debugging workflows.');
    expect(element.textContent).toContain('Saved Example Workflow');
    expect(element.textContent).toContain('id: support_ticket_triage');
    expect(element.querySelector('.library')?.getAttribute('aria-label')).toBe('Node Library');
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

  it('should expose ARIA tab semantics for example switching', () => {
    const element: HTMLElement = fixture.nativeElement;
    const buttons = Array.from(element.querySelectorAll('.example-tab')) as HTMLButtonElement[];
    const yamlButton = buttons.find((button) => button.textContent?.trim() === 'YAML');
    const jsonButton = buttons.find((button) => button.textContent?.trim() === 'JSON');

    expect(yamlButton?.getAttribute('role')).toBe('tab');
    expect(yamlButton?.getAttribute('aria-selected')).toBe('true');
    expect(jsonButton?.getAttribute('aria-selected')).toBe('false');
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

  it('should persist and restore a local project snapshot', () => {
    const studio = component as any;

    studio.projectName = 'My Local Project';
    studio.updateSelectedNodeLabel('Edited Name');

    studio.saveProject();

    studio.newProject();
    expect(studio.selectedProjectId).toBeNull();

    const storedId = studio.savedProjects[0]?.id;
    expect(storedId).toBeTruthy();

    studio.loadProject(storedId);

    expect(studio.projectName).toBe('My Local Project');
    expect(studio.selectedNode?.label ?? '').toBe('Edited Name');
  });

  it('should ignore null entries when restoring saved projects from local storage', () => {
    localStorage.setItem(
      'mp.workflowStudio.projects.v1',
      JSON.stringify([
        null,
        {
          id: 'project_valid',
          name: 'Recovered Project',
          updatedAtIso: '2026-04-10T10:00:00.000Z',
          selectedNodeId: 'node_ai',
          nodes: [
            { id: 'node_ai', typeId: 'process_ai', label: 'AI Engine', summary: 'Analyze lead context', x: 0, y: 0 }
          ]
        }
      ])
    );

    const restoredFixture = TestBed.createComponent(WorkflowStudioPageComponent);
    const restoredComponent = restoredFixture.componentInstance as any;
    const restoredInitial = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.yaml');
    restoredInitial.flush('id: support_ticket_triage');
    restoredFixture.detectChanges();

    expect(restoredComponent.savedProjects.length).toBe(1);
    expect(restoredComponent.savedProjects[0].id).toBe('project_valid');
    expect(restoredComponent.statusMessage).toContain('Found 1 locally saved project');
  });

  it('should use crypto.randomUUID when creating a new project id', () => {
    const generatedUuid = '00000000-0000-4000-8000-000000000000';
    const randomUuidSpy = spyOn(globalThis.crypto, 'randomUUID').and.returnValue(generatedUuid);
    const studio = component as any;

    studio.saveProject();

    expect(randomUuidSpy).toHaveBeenCalled();
    expect(studio.selectedProjectId).toBe(generatedUuid);
    expect(studio.savedProjects[0].id).toBe(generatedUuid);
  });

  it('should move an updated project to the top of the saved list', () => {
    const studio = component as any;

    studio.projectName = 'First Project';
    studio.saveProject();
    const firstProjectId = studio.selectedProjectId;

    studio.newProject();
    studio.projectName = 'Second Project';
    studio.saveProject();
    expect(studio.savedProjects.map((project: any) => project.name)).toEqual(['Second Project', 'First Project']);

    studio.loadProject(firstProjectId);
    studio.projectName = 'First Project Updated';
    studio.saveProject();

    expect(studio.savedProjects[0].id).toBe(firstProjectId);
    expect(studio.savedProjects[0].name).toBe('First Project Updated');
  });

  it('should recover with an empty project list when local storage access fails during restore', () => {
    const getItemSpy = spyOn(Storage.prototype, 'getItem').and.throwError('blocked');

    const restoredFixture = TestBed.createComponent(WorkflowStudioPageComponent);
    const restoredComponent = restoredFixture.componentInstance as any;
    const restoredInitial = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.yaml');
    restoredInitial.flush('id: support_ticket_triage');
    restoredFixture.detectChanges();

    expect(restoredComponent.savedProjects).toEqual([]);
    expect(restoredComponent.statusMessage).toContain('Could not access saved projects');

    getItemSpy.and.callThrough();
  });

  it('should surface a storage-unavailable message when saving fails', () => {
    const setItemSpy = spyOn(Storage.prototype, 'setItem').and.throwError('quota exceeded');
    const studio = component as any;

    studio.projectName = 'Blocked Save';
    studio.saveProject();

    expect(studio.statusMessage).toContain('Could not save');
    expect(studio.savedProjects[0].name).toBe('Blocked Save');

    setItemSpy.and.callThrough();
  });
});
