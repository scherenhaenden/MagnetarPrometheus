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

  it('should open tabs, load projects, and fall back to draft when closing the active tab', () => {
    const studio = component as any;
    studio.projectName = 'Open Me';
    studio.saveProject();
    const projectId = studio.selectedProjectId;

    studio.newProject();
    studio.openTab(projectId);
    expect(studio.activeTabId).toBe(projectId);
    expect(studio.projectName).toBe('Open Me');

    studio.closeTab(projectId);
    expect(studio.activeTabId).toBe('draft');
    expect(studio.selectedProjectId).toBeNull();
    expect(studio.projectName).toBe('Untitled Workflow');
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

  it('should render tab close actions as separate accessible buttons', () => {
    const studio = component as any;
    studio.projectName = 'Closable';
    studio.saveProject();
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    const closeButton = Array.from(element.querySelectorAll('.close')).find(
      (button) => button.getAttribute('aria-label') === 'Close Closable'
    ) as HTMLButtonElement;

    expect(closeButton).toBeTruthy();
    expect(closeButton.tagName).toBe('BUTTON');
  });

  it('should guard pointerdown and pointermove edge cases and clear drag state on pointerup', () => {
    const studio = component as any;

    studio.onNodePointerDown({ button: 1 } as PointerEvent, 'node_ai');
    expect(studio.draggingNodeId).toBeNull();

    studio.onNodePointerDown({ button: 0 } as PointerEvent, 'missing-node');
    expect(studio.draggingNodeId).toBeNull();

    studio.onNodePointerDown({ button: 0, pointerId: 5, clientX: 100, clientY: 100 } as PointerEvent, 'node_ai');
    studio.onDocumentPointerMove({ pointerId: 6, clientX: 110, clientY: 110, preventDefault: () => {}, cancelable: true } as unknown as PointerEvent);
    expect(studio.isActuallyDragging).toBeFalse();

    studio.onDocumentPointerMove({ pointerId: 5, clientX: 102, clientY: 102, preventDefault: () => {}, cancelable: true } as unknown as PointerEvent);
    expect(studio.isActuallyDragging).toBeFalse();

    studio.onDocumentPointerMove({ pointerId: 5, clientX: 150, clientY: 115, preventDefault: () => {}, cancelable: true } as unknown as PointerEvent);
    expect(studio.isActuallyDragging).toBeTrue();

    studio.nodes = [];
    studio.onDocumentPointerMove({ pointerId: 5, clientX: 160, clientY: 120, preventDefault: () => {}, cancelable: true } as unknown as PointerEvent);
    studio.onDocumentPointerUp();
    expect(studio.draggingNodeId).toBeNull();
    expect(studio.dragPointerId).toBeNull();
    expect(studio.isActuallyDragging).toBeFalse();
  });

  it('should use default names, reorder saved projects, and surface save failures', () => {
    const studio = component as any;

    studio.projectName = '   ';
    studio.saveProject();
    expect(studio.savedProjects[0].name).toBe('Untitled Workflow');

    const originalId = studio.savedProjects[0].id;
    studio.newProject();
    studio.projectName = 'Second';
    studio.saveProject();
    studio.loadProject(originalId);
    studio.projectName = 'First Updated';
    studio.saveProject();

    expect(studio.savedProjects[0].id).toBe(originalId);

    spyOn(studio, 'getLocalStorage').and.returnValue(null);
    studio.saveProject();
    expect(studio.statusMessage).toContain('Browser storage is unavailable');
  });

  it('should handle missing projects and invalid selected nodes while loading', () => {
    const studio = component as any;

    studio.loadProject(null);
    studio.loadProject('missing-project');
    expect(studio.statusMessage).toContain('Unable to load project');

    studio.savedProjects = [{
      id: 'project-invalid-selected',
      name: 'Broken selection',
      updatedAtIso: '2026-04-11T10:00:00.000Z',
      selectedNodeId: 'missing',
      nodes: [{ id: 'fallback-node', typeId: 'process_ai', label: 'Fallback', summary: 'S', x: 0, y: 0 }]
    }];
    studio.loadProject('project-invalid-selected');
    expect(studio.selectedNodeId).toBe('fallback-node');

    studio.savedProjects = [{
      id: 'project-empty',
      name: 'Empty',
      updatedAtIso: '2026-04-11T10:00:00.000Z',
      selectedNodeId: 'missing',
      nodes: []
    }];
    studio.loadProject('project-empty');
    expect(studio.selectedNodeId).toBe('');
  });

  it('should reset new projects and fall back to the first node type when needed', () => {
    const studio = component as any;
    studio.defaultNodes = [];

    studio.newProject();

    expect(studio.selectedNodeId).toBe('');
    expect(studio.workflowSequence).toEqual([]);
    expect(studio.getNodeType('missing-type').id).toBe(studio.nodeTypes[0].id);
  });

  it('should drop invalid edges when building connections for missing nodes', () => {
    const studio = component as any;

    studio.workflowSequence = ['node_trigger', 'missing-node'];

    expect(studio.buildConnections()).toEqual([]);
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
    const subscription = studio.workflowSubscription;
    studio.runWorkflow();
    expect(studio.workflowSubscription).toBe(subscription);

    studio.stopWorkflow();
    expect(studio.isRunning).toBeFalse();
    expect(studio.completedNodeIds.size).toBe(0);
    expect(studio.workflowSubscription).toBeNull();
  }));

  it('should clear workflow state during ngOnDestroy', () => {
    const studio = component as any;

    studio.runWorkflow();
    studio.ngOnDestroy();

    expect(studio.isRunning).toBeFalse();
    expect(studio.activeNodeId).toBeNull();
    expect(studio.completedNodeIds.size).toBe(0);
  });

  it('should show an error when the selected example fails and ignore stale errors', () => {
    const studio = component as any;
    const jsonExample = studio.examples.find((example: any) => example.format === 'json');
    const tomlExample = studio.examples.find((example: any) => example.format === 'toml');

    studio.selectExample(jsonExample);
    const jsonRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    jsonRequest.error(new ProgressEvent('error'));

    expect(studio.exampleContent).toBe('');
    expect(studio.exampleError).toContain('Unable to load JSON workflow example');
    expect(studio.loadingExample).toBeFalse();

    studio.selectExample(jsonExample);
    studio.selectExample(tomlExample);
    const secondJsonRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.json');
    const tomlRequest = httpMock.expectOne('/assets/workflows/examples/support-ticket-triage.toml');

    tomlRequest.flush('id = "support_ticket_triage"');
    secondJsonRequest.error(new ProgressEvent('error'));

    expect(studio.selectedExample.path).toBe('/assets/workflows/examples/support-ticket-triage.toml');
    expect(studio.exampleContent).toBe('id = "support_ticket_triage"');
    expect(studio.exampleError).toBeNull();
  });

  it('should handle unavailable, unreadable, malformed, and filtered local storage payloads', () => {
    const studio = component as any;
    const storageSpy = spyOn(studio, 'getLocalStorage');

    storageSpy.and.returnValue(null);
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Local storage is unavailable');

    const getItemSpy = spyOn(Storage.prototype, 'getItem').and.throwError('blocked');
    storageSpy.and.returnValue(localStorage);
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Could not access saved projects');
    getItemSpy.and.callThrough();

    localStorage.setItem('mp.workflowStudio.projects.v1', '{broken');
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Could not parse saved projects');

    localStorage.setItem('mp.workflowStudio.projects.v1', '{}');
    studio.restoreProjects();
    expect(studio.savedProjects).toEqual([]);

    localStorage.setItem(
      'mp.workflowStudio.projects.v1',
      JSON.stringify([null, {
        id: 'project-valid',
        name: 'Valid',
        updatedAtIso: '2026-04-11T10:00:00.000Z',
        selectedNodeId: 'node_trigger',
        nodes: [{ id: 'node_trigger', typeId: 'trigger_http', label: 'Webhook', summary: 'Lead', x: 0, y: 0 }]
      }])
    );
    studio.restoreProjects();
    expect(studio.savedProjects.length).toBe(1);
    expect(studio.statusMessage).toContain('Found 1 locally saved project');
  });

  it('should return false from persistProjects when storage is unavailable or writes fail', () => {
    const studio = component as any;

    spyOn(studio, 'getLocalStorage').and.returnValue(null);
    expect(studio.persistProjects()).toBeFalse();

    const setItemSpy = spyOn(Storage.prototype, 'setItem').and.throwError('blocked');
    (studio.getLocalStorage as jasmine.Spy).and.returnValue(localStorage);
    expect(studio.persistProjects()).toBeFalse();
    setItemSpy.and.callThrough();
  });

  it('should use fallback project ids and handle missing browser localStorage', () => {
    const studio = component as any;
    const originalCrypto = globalThis.crypto;
    const cryptoDescriptor = Object.getOwnPropertyDescriptor(globalThis, 'crypto');
    const storageDescriptor = Object.getOwnPropertyDescriptor(globalThis, 'localStorage');

    try {
      Object.defineProperty(globalThis, 'crypto', {
        configurable: true,
        value: { ...originalCrypto, randomUUID: undefined }
      });
      expect(studio.createProjectId()).toMatch(/^project_/);

      Object.defineProperty(globalThis, 'localStorage', {
        configurable: true,
        value: undefined
      });
      expect(studio.getLocalStorage()).toBeNull();
    } finally {
      if (cryptoDescriptor) {
        Object.defineProperty(globalThis, 'crypto', cryptoDescriptor);
      }
      if (storageDescriptor) {
        Object.defineProperty(globalThis, 'localStorage', storageDescriptor);
      }
    }
  });
});
