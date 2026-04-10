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
    localStorage.clear();

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
});
