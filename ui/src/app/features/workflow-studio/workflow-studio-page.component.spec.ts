/**
 * workflow-studio-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowStudioPageComponent.
 */
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
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
    restoredFixture.detectChanges();
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

  it('should use the default project name when saving whitespace-only names', () => {
    const studio = component as any;

    studio.projectName = '   ';
    studio.saveProject();

    expect(studio.savedProjects[0].name).toBe('Untitled Workflow');
  });

  it('should recover with an empty project list when local storage access fails during restore', () => {
    const getItemSpy = spyOn(Storage.prototype, 'getItem').and.throwError('blocked');

    const restoredFixture = TestBed.createComponent(WorkflowStudioPageComponent);
    const restoredComponent = restoredFixture.componentInstance as any;
    restoredFixture.detectChanges();
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

  it('should update theme, accent, selection, label, and summary through component handlers', () => {
    const studio = component as any;

    studio.onThemeChange('aurora');
    studio.onAccentChange('#10b981');
    studio.selectNode('node_trigger');
    studio.updateSelectedNodeLabel('Renamed Trigger');
    studio.updateSelectedNodeSummary('Updated summary');

    expect(studio.selectedThemeId).toBe('aurora');
    expect(studio.selectedAccent).toBe('#10b981');
    expect(studio.selectedNodeId).toBe('node_trigger');
    expect(studio.selectedNode.label).toBe('Renamed Trigger');
    expect(studio.selectedNode.summary).toBe('Updated summary');
  });

  it('should ignore label and summary updates when no node is selected', () => {
    const studio = component as any;

    studio.selectedNodeId = 'missing-node';
    studio.updateSelectedNodeLabel('Ignored');
    studio.updateSelectedNodeSummary('Ignored');

    expect(studio.selectedNode).toBeNull();
    expect(studio.selectedNodeType).toBeNull();
  });

  it('should ignore invalid project loads and fallback selected nodes when needed', () => {
    const studio = component as any;
    const initialStatus = studio.statusMessage;

    studio.loadProject(null);
    expect(studio.statusMessage).toBe(initialStatus);

    studio.loadProject('missing-project');
    expect(studio.statusMessage).toContain('Unable to load project');

    studio.savedProjects = [{
      id: 'project-invalid-selected',
      name: 'Broken selection',
      updatedAtIso: '2026-04-10T10:00:00.000Z',
      selectedNodeId: 'missing',
      nodes: [{ id: 'fallback-node', typeId: 'process_ai', label: 'Fallback', summary: 'S', x: 0, y: 0 }]
    }];
    studio.loadProject('project-invalid-selected');
    expect(studio.selectedNodeId).toBe('fallback-node');

    studio.savedProjects = [{
      id: 'project-empty',
      name: 'Empty',
      updatedAtIso: '2026-04-10T10:00:00.000Z',
      selectedNodeId: 'missing',
      nodes: []
    }];
    studio.loadProject('project-empty');
    expect(studio.selectedNodeId).toBe('');
  });

  it('should safely reset new projects even when default nodes are empty', () => {
    const studio = component as any;
    studio.defaultNodes = [];

    studio.newProject();

    expect(studio.selectedNodeId).toBe('');
    expect(studio.workflowSequence).toEqual([]);
  });

  it('should return the first node type when the requested type is unknown', () => {
    const studio = component as any;

    expect(studio.getNodeType('missing-type').id).toBe(studio.nodeTypes[0].id);
  });

  it('should handle pointerdown guard clauses and valid drag initialization', () => {
    const studio = component as any;

    studio.onNodePointerDown({ button: 1 } as PointerEvent, 'node_trigger');
    expect(studio.draggingNodeId).toBeNull();

    studio.onNodePointerDown({ button: 0 } as PointerEvent, 'missing-node');
    expect(studio.draggingNodeId).toBeNull();

    studio.onNodePointerDown({ button: 0, pointerId: 9, clientX: 10, clientY: 20 } as PointerEvent, 'node_trigger');
    expect(studio.draggingNodeId).toBe('node_trigger');
    expect(studio.dragPointerId).toBe(9);
    expect(studio.dragStartPointer).toEqual({ x: 10, y: 20 });
  });

  it('should ignore pointer moves until the drag threshold is crossed and clamp positions to non-negative coordinates', () => {
    const studio = component as any;
    const preventDefault = jasmine.createSpy('preventDefault');

    studio.onNodePointerDown({ button: 0, pointerId: 3, clientX: 100, clientY: 100 } as PointerEvent, 'node_trigger');
    studio.onDocumentPointerMove({ pointerId: 4, clientX: 110, clientY: 110, preventDefault, cancelable: true } as unknown as PointerEvent);
    expect(studio.nodes[0].x).toBe(72);

    studio.onDocumentPointerMove({ pointerId: 3, clientX: 102, clientY: 102, preventDefault, cancelable: true } as unknown as PointerEvent);
    expect(studio.isActuallyDragging).toBeFalse();
    expect(preventDefault).toHaveBeenCalled();

    studio.onDocumentPointerMove({ pointerId: 3, clientX: -50, clientY: -30, preventDefault, cancelable: true } as unknown as PointerEvent);
    expect(studio.isActuallyDragging).toBeTrue();
    expect(preventDefault).toHaveBeenCalled();
    expect(studio.nodes[0].x).toBe(0);
    expect(studio.nodes[0].y).toBe(0);
  });

  it('should stop drag updates when the node no longer exists and clear drag state on pointerup', () => {
    const studio = component as any;

    studio.onNodePointerDown({ button: 0, pointerId: 7, clientX: 10, clientY: 10 } as PointerEvent, 'node_trigger');
    studio.nodes = [];
    studio.onDocumentPointerMove({ pointerId: 7, clientX: 40, clientY: 40, preventDefault() {}, cancelable: true } as unknown as PointerEvent);

    studio.onDocumentPointerUp();
    expect(studio.draggingNodeId).toBeNull();
    expect(studio.dragPointerId).toBeNull();
    expect(studio.isActuallyDragging).toBeFalse();
  });

  it('should run and stop the workflow simulation across all nodes', fakeAsync(() => {
    const studio = component as any;

    studio.runWorkflow();
    expect(studio.isRunning).toBeTrue();
    expect(studio.activeNodeId).toBeNull();

    tick(700);
    expect(studio.activeNodeId).toBe(studio.workflowSequence[0]);

    tick(700);
    expect(studio.completedNodeIds.has(studio.workflowSequence[0])).toBeTrue();

    tick(700 * (studio.workflowSequence.length - 2));
    tick(700);
    expect(studio.isRunning).toBeFalse();
    expect(studio.activeNodeId).toBeNull();
    expect(studio.completedNodeIds.has(studio.workflowSequence[studio.workflowSequence.length - 1])).toBeTrue();

    studio.runWorkflow();
    expect(studio.isRunning).toBeTrue();
    studio.stopWorkflow();
    expect(studio.isRunning).toBeFalse();
    expect(studio.completedNodeIds.size).toBe(0);
  }));

  it('should ignore duplicate run requests while already running', () => {
    const studio = component as any;

    studio.runWorkflow();
    const subscription = studio.workflowSubscription;
    studio.runWorkflow();

    expect(studio.workflowSubscription).toBe(subscription);
    studio.stopWorkflow();
  });

  it('should unsubscribe from workflow and stop during ngOnDestroy', () => {
    const studio = component as any;

    studio.runWorkflow();
    const subscription = studio.workflowSubscription;
    spyOn(subscription, 'unsubscribe').and.callThrough();

    studio.ngOnDestroy();

    expect(subscription.unsubscribe).toHaveBeenCalled();
    expect(studio.workflowSubscription).toBeNull();
    expect(studio.isRunning).toBeFalse();
  });

  it('should keep the current example content when an older request fails after switching tabs', () => {
    const studio = component as any;
    const jsonExample = studio.examples.find((example: any) => example.format === 'json');
    const tomlExample = studio.examples.find((example: any) => example.format === 'toml');

    studio.selectExample(jsonExample);
    studio.selectExample(tomlExample);

    const jsonRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    const tomlRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.toml');

    tomlRequest.flush('id = "support_ticket_triage"');
    jsonRequest.error(new ProgressEvent('error'));

    expect(studio.selectedExample.path).toBe('/assets/workflows/examples/support-ticket-triage.toml');
    expect(studio.exampleContent).toBe('id = "support_ticket_triage"');
    expect(studio.exampleError).toBeNull();
  });

  it('should show an error when the currently selected example fails to load', () => {
    const studio = component as any;
    const jsonExample = studio.examples.find((example: any) => example.format === 'json');

    studio.selectExample(jsonExample);

    const jsonRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    jsonRequest.error(new ProgressEvent('error'));

    expect(studio.exampleContent).toBe('');
    expect(studio.exampleError).toContain('Unable to load JSON workflow example');
    expect(studio.loadingExample).toBeFalse();
  });

  it('should handle missing browser storage and malformed stored project data', () => {
    const studio = component as any;
    const storageSpy = spyOn(studio, 'getLocalStorage');

    storageSpy.and.returnValue(null);
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Local storage is unavailable');

    storageSpy.and.returnValue(localStorage);
    localStorage.setItem('mp.workflowStudio.projects.v1', '{broken');
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Could not parse saved projects');
  });

  it('should handle empty and non-array stored project payloads without changing status unexpectedly', () => {
    const studio = component as any;
    const storageSpy = spyOn(studio, 'getLocalStorage').and.returnValue(localStorage);
    const baselineStatus = studio.statusMessage;

    localStorage.removeItem('mp.workflowStudio.projects.v1');
    studio.restoreProjects();
    expect(studio.statusMessage).toBe(baselineStatus);

    localStorage.setItem('mp.workflowStudio.projects.v1', '{}');
    studio.restoreProjects();
    expect(studio.savedProjects).toEqual([]);

    localStorage.setItem('mp.workflowStudio.projects.v1', '[]');
    studio.restoreProjects();
    expect(studio.savedProjects).toEqual([]);

    storageSpy.and.callThrough();
  });

  it('should use fallback project ids and report unavailable storage from persistProjects', () => {
    const studio = component as any;
    const originalCrypto = globalThis.crypto;

    Object.defineProperty(globalThis, 'crypto', {
      configurable: true,
      value: { ...originalCrypto, randomUUID: undefined }
    });
    expect(studio.createProjectId()).toMatch(/^project_/);

    spyOn(studio, 'getLocalStorage').and.returnValue(null);
    expect(studio.persistProjects()).toBeFalse();

    Object.defineProperty(globalThis, 'crypto', {
      configurable: true,
      value: originalCrypto
    });
  });

  it('should return null when browser localStorage is unavailable', () => {
    const studio = component as any;
    const storageDescriptor = Object.getOwnPropertyDescriptor(globalThis, 'localStorage');

    Object.defineProperty(globalThis, 'localStorage', {
      configurable: true,
      value: undefined
    });

    expect(studio.getLocalStorage()).toBeNull();

    if (storageDescriptor) {
      Object.defineProperty(globalThis, 'localStorage', storageDescriptor);
    }
  });
});
