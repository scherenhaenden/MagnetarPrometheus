/**
 * workflow-studio-page.component.spec.ts intent header.
 *
 * This test validates the WorkflowStudioPageComponent.
 */
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { WorkflowStudioPageComponent } from './workflow-studio-page.component';

describe('WorkflowStudioPageComponent', () => {
  let component: WorkflowStudioPageComponent;
  let fixture: ComponentFixture<WorkflowStudioPageComponent>;

  beforeEach(async () => {
    localStorage.clear();

    await TestBed.configureTestingModule({
      imports: [WorkflowStudioPageComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(WorkflowStudioPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the redesigned studio header and layout', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('.brand-block h2')?.textContent).toContain('Workflow Studio');
    expect(element.textContent).toContain('Visual editor workspace for building, testing, and debugging workflows.');
    expect(element.textContent).toContain('Run Workflow');
    expect(element.textContent).toContain('Save Local');
    expect(element.querySelector('.library')?.getAttribute('aria-label')).toBe('Node Library');
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

  it('should select a node', () => {
    const studio = component as any;
    studio.selectNode('node_trigger');
    expect(studio.selectedNodeId).toBe('node_trigger');
    expect(studio.selectedNode?.id).toBe('node_trigger');
  });

  it('should update selected node label and summary', () => {
    const studio = component as any;
    studio.selectNode('node_trigger');
    studio.updateSelectedNodeLabel('New Label');
    studio.updateSelectedNodeSummary('New Summary');
    expect(studio.selectedNode?.label).toBe('New Label');
    expect(studio.selectedNode?.summary).toBe('New Summary');
  });

  it('should not update label or summary if no node is selected', () => {
    const studio = component as any;
    studio.selectedNodeId = 'non-existent';
    
    expect(studio.selectedNode).toBeNull();
    expect(studio.selectedNodeType).toBeNull();
    
    studio.updateSelectedNodeLabel('New Label');
    studio.updateSelectedNodeSummary('New Summary');
    expect(studio.selectedNode).toBeNull();
  });

  it('should use default name if project name is empty on save', () => {
    const studio = component as any;
    studio.projectName = '   ';
    studio.saveProject();
    expect(studio.savedProjects[0].name).toBe('Untitled Workflow');
  });

  it('should do nothing if loadProject is called without id', () => {
    const studio = component as any;
    const initialStatus = studio.statusMessage;
    studio.loadProject(null);
    expect(studio.statusMessage).toBe(initialStatus);
  });

  it('should set error message if project to load does not exist', () => {
    const studio = component as any;
    studio.loadProject('non-existent');
    expect(studio.statusMessage).toContain('Unable to load project');
  });

  it('should fallback to first node if loaded project has invalid selectedNodeId', () => {
    const studio = component as any;
    studio.savedProjects = [{
      id: 'p1',
      name: 'P1',
      selectedNodeId: 'invalid',
      nodes: [{ id: 'n1', typeId: 't1', label: 'L', summary: 'S', x: 0, y: 0 }]
    }];
    studio.loadProject('p1');
    expect(studio.selectedNodeId).toBe('n1');
  });

  it('should fallback to empty string if loaded project has no nodes', () => {
    const studio = component as any;
    studio.savedProjects = [{
      id: 'p_empty',
      name: 'Empty',
      selectedNodeId: 'n1',
      nodes: []
    }];
    studio.loadProject('p_empty');
    expect(studio.selectedNodeId).toBe('');
  });

  it('should handle newProject with empty default nodes safely', () => {
    const studio = component as any;
    studio.defaultNodes = [];
    studio.newProject();
    expect(studio.selectedNodeId).toBe('');
  });

  it('should return default node type if typeId is unknown', () => {
    const studio = component as any;
    const type = studio.getNodeType('unknown');
    expect(type.id).toBe(studio.nodeTypes[0].id);
  });

  it('should run workflow and complete steps', fakeAsync(() => {
    const studio = component as any;
    studio.newProject();
    fixture.detectChanges();
    studio.runWorkflow();
    expect(studio.isRunning).toBeTrue();
    tick(10000); 
    fixture.detectChanges();
    expect(studio.isRunning).toBeFalse();
    expect(studio.activeNodeId).toBeNull();
    expect(studio.completedNodeIds.size).toBeGreaterThan(0);
  }));

  it('should not run workflow if already running', () => {
    const studio = component as any;
    studio.runWorkflow();
    const initialTimers = studio.timers.length;
    studio.runWorkflow();
    expect(studio.timers.length).toBe(initialTimers);
  });

  it('should handle local storage being unavailable during restore', () => {
    const studio = component as any;
    spyOn(studio, 'getLocalStorage').and.returnValue(null);
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Local storage is unavailable');
  });

  it('should handle JSON parse error during restore', () => {
    localStorage.setItem('mp.workflowStudio.projects.v1', 'invalid-json');
    const studio = component as any;
    studio.restoreProjects();
    expect(studio.statusMessage).toContain('Could not parse saved projects');
  });

  it('should handle non-array data in local storage during restore', () => {
    localStorage.setItem('mp.workflowStudio.projects.v1', JSON.stringify({ not: 'an-array' }));
    const studio = component as any;
    studio.restoreProjects();
    expect(studio.savedProjects).toEqual([]);
  });

  it('should return false if persist fails due to missing storage', () => {
    const studio = component as any;
    spyOn(studio, 'getLocalStorage').and.returnValue(null);
    const result = studio.persistProjects();
    expect(result).toBeFalse();
  });

  it('should use fallback project id if randomUUID is unavailable', () => {
    const studio = component as any;
    spyOnProperty(globalThis, 'crypto', 'get').and.returnValue({} as any);
    const id = studio.createProjectId();
    expect(id).toContain('project_');
  });

  it('should clear timers on destroy', () => {
    const studio = component as any;
    studio.runWorkflow();
    expect(studio.timers.length).toBeGreaterThan(0);
    const clearSpy = spyOn(globalThis, 'clearTimeout').and.callThrough();
    component.ngOnDestroy();
    expect(clearSpy).toHaveBeenCalled();
    expect(studio.timers.length).toBe(0);
  });

  it('should return null from getLocalStorage if globalThis.localStorage is undefined', () => {
    const studio = component as any;
    const originalStorage = globalThis.localStorage;
    Object.defineProperty(globalThis, 'localStorage', {
      get: () => undefined,
      configurable: true
    });
    expect(studio.getLocalStorage()).toBeNull();
    Object.defineProperty(globalThis, 'localStorage', {
      get: () => originalStorage,
      configurable: true
    });
  });

  it('should change theme and accent', () => {
    const studio = component as any;
    studio.onThemeChange('graphite');
    expect(studio.selectedThemeId).toBe('graphite');
    studio.onAccentChange('#7c3aed');
    expect(studio.selectedAccent).toBe('#7c3aed');
  });

  it('should handle node drag and drop', () => {
    const studio = component as any;
    const nodeId = 'node_trigger';
    const node = studio.nodes.find((n: any) => n.id === nodeId);
    const initialX = node.x;
    const initialY = node.y;

    // Start dragging
    const pointerDownEvent = new PointerEvent('pointerdown', {
      button: 0,
      clientX: 100,
      clientY: 100
    });
    studio.onNodePointerDown(pointerDownEvent, nodeId);
    expect(studio.draggingNodeId).toBe(nodeId);

    // Move
    const pointerMoveEvent = new PointerEvent('pointermove', {
      clientX: 150,
      clientY: 150
    });
    studio.onDocumentPointerMove(pointerMoveEvent);
    expect(node.x).toBe(initialX + 50);
    expect(node.y).toBe(initialY + 50);

    // Stop dragging
    studio.onDocumentPointerUp();
    expect(studio.draggingNodeId).toBeNull();
  });

  it('should not start drag if button is not 0', () => {
    const studio = component as any;
    const pointerDownEvent = new PointerEvent('pointerdown', { button: 1 });
    studio.onNodePointerDown(pointerDownEvent, 'node_trigger');
    expect(studio.draggingNodeId).toBeNull();
  });

  it('should not drag if node does not exist', () => {
    const studio = component as any;
    studio.onNodePointerDown(new PointerEvent('pointerdown', { button: 0 }), 'invalid');
    expect(studio.draggingNodeId).toBeNull();
  });

  it('should not move if nothing is dragging', () => {
    const studio = component as any;
    const node = studio.nodes[0];
    const initialX = node.x;
    studio.onDocumentPointerMove(new PointerEvent('pointermove', { clientX: 200 }));
    expect(node.x).toBe(initialX);
  });

  it('should handle case where dragging node disappears during move', () => {
    const studio = component as any;
    studio.draggingNodeId = 'node_trigger';
    studio.nodes = []; // Empty nodes
    studio.onDocumentPointerMove(new PointerEvent('pointermove', { clientX: 200 }));
    expect(studio.draggingNodeId).toBe('node_trigger');
  });
});
