/**
 * Workflow Studio page.
 *
 * This component provides a local-first workflow project editing experience.
 * Users can edit node metadata, save snapshots as local projects, and reload
 * those projects from browser storage without requiring backend integration.
 */
import { NgClass, NgFor, NgIf } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

type NodeCategory = 'trigger' | 'process' | 'logic' | 'integration';

interface StudioNodeType {
  id: string;
  label: string;
  icon: string;
  category: NodeCategory;
  accent: string;
}

interface StudioNode {
  id: string;
  typeId: string;
  label: string;
  summary: string;
  x: number;
  y: number;
}

interface StudioProject {
  id: string;
  name: string;
  updatedAtIso: string;
  selectedNodeId: string;
  nodes: StudioNode[];
}

@Component({
  standalone: true,
  imports: [NgFor, NgIf, NgClass, FormsModule],
  templateUrl: './workflow-studio-page.component.html',
  styleUrl: './workflow-studio-page.component.css'
})
export class WorkflowStudioPageComponent implements OnInit, OnDestroy {
  protected readonly nodeTypes: StudioNodeType[] = [
    { id: 'trigger_http', label: 'HTTP Webhook', icon: '🌐', category: 'trigger', accent: 'violet' },
    { id: 'trigger_cron', label: 'Schedule', icon: '⏰', category: 'trigger', accent: 'blue' },
    { id: 'process_ai', label: 'AI Engine', icon: '🤖', category: 'process', accent: 'emerald' },
    { id: 'process_script', label: 'Run Script', icon: '🧩', category: 'process', accent: 'amber' },
    { id: 'logic_if', label: 'Condition', icon: '🔀', category: 'logic', accent: 'pink' },
    { id: 'integration_db', label: 'CRM Insert', icon: '🗄️', category: 'integration', accent: 'indigo' },
    { id: 'integration_slack', label: 'Slack Notify', icon: '📣', category: 'integration', accent: 'sky' },
    { id: 'integration_email', label: 'Send Email', icon: '✉️', category: 'integration', accent: 'orange' }
  ];

  protected readonly defaultNodes: StudioNode[] = [
    { id: 'node_trigger', typeId: 'trigger_http', label: 'New Lead Form', summary: 'POST /api/leads/new', x: 72, y: 128 },
    { id: 'node_ai', typeId: 'process_ai', label: 'Enrich & Score', summary: 'Analyze lead context', x: 384, y: 128 },
    { id: 'node_logic', typeId: 'logic_if', label: 'Is High Quality?', summary: 'Score >= 80', x: 696, y: 128 },
    { id: 'node_db', typeId: 'integration_db', label: 'Save VIP Lead', summary: 'salesforce_leads', x: 1008, y: 48 },
    { id: 'node_email', typeId: 'integration_email', label: 'Nurture Drip', summary: 'template: nurture_1', x: 1008, y: 232 }
  ];

  protected nodes: StudioNode[] = this.cloneNodes(this.defaultNodes);
  protected workflowSequence: string[] = this.nodes.map((node) => node.id);

  protected selectedNodeId = 'node_ai';
  protected isRunning = false;
  protected activeNodeId: string | null = null;
  protected completedNodeIds = new Set<string>();

  protected projectName = 'Untitled Workflow';
  protected selectedProjectId: string | null = null;
  protected savedProjects: StudioProject[] = [];
  protected statusMessage = 'Local mode ready. Save your first project.';

  private readonly storageKey = 'mp.workflowStudio.projects.v1';
  private readonly nodeTypesById = new Map(this.nodeTypes.map((type) => [type.id, type]));
  private timers: ReturnType<typeof setTimeout>[] = [];

  public ngOnInit(): void {
    this.restoreProjects();
  }

  protected get selectedNode(): StudioNode | null {
    return this.nodes.find((node) => node.id === this.selectedNodeId) ?? null;
  }

  protected get selectedNodeType(): StudioNodeType | null {
    const node = this.selectedNode;
    return node ? this.getNodeType(node.typeId) : null;
  }

  protected selectNode(nodeId: string): void {
    this.selectedNodeId = nodeId;
  }

  protected updateSelectedNodeLabel(value: string): void {
    const node = this.selectedNode;
    if (!node) {
      return;
    }

    node.label = value;
  }

  protected updateSelectedNodeSummary(value: string): void {
    const node = this.selectedNode;
    if (!node) {
      return;
    }

    node.summary = value;
  }

  protected saveProject(): void {
    const trimmedName = this.projectName.trim();
    const nowIso = new Date().toISOString();
    const nextId = this.selectedProjectId ?? this.createProjectId();

    const project: StudioProject = {
      id: nextId,
      name: trimmedName.length > 0 ? trimmedName : 'Untitled Workflow',
      updatedAtIso: nowIso,
      selectedNodeId: this.selectedNodeId,
      nodes: this.cloneNodes(this.nodes)
    };

    const existingIndex = this.savedProjects.findIndex((savedProject) => savedProject.id === nextId);
    if (existingIndex >= 0) {
      this.savedProjects.splice(existingIndex, 1);
    }
    this.savedProjects.unshift(project);

    this.selectedProjectId = project.id;
    this.projectName = project.name;
    if (this.persistProjects()) {
      this.statusMessage = `Saved '${project.name}' locally at ${new Date(project.updatedAtIso).toLocaleTimeString()}.`;
    } else {
      this.statusMessage = `Could not save '${project.name}' locally. Browser storage is unavailable.`;
    }
  }

  protected loadProject(projectId: string | null): void {
    if (!projectId) {
      return;
    }
    const project = this.savedProjects.find((savedProject) => savedProject.id === projectId);
    if (!project) {
      this.statusMessage = 'Unable to load project. It may have been removed.';
      return;
    }

    this.nodes = this.cloneNodes(project.nodes);
    this.workflowSequence = this.nodes.map((node) => node.id);
    this.selectedNodeId = this.nodes.some((node) => node.id === project.selectedNodeId)
      ? project.selectedNodeId
      : this.nodes[0]?.id ?? '';

    this.selectedProjectId = project.id;
    this.projectName = project.name;
    this.statusMessage = `Loaded '${project.name}' from local storage.`;
    this.stopWorkflow();
  }

  protected newProject(): void {
    this.stopWorkflow();
    this.nodes = this.cloneNodes(this.defaultNodes);
    this.workflowSequence = this.nodes.map((node) => node.id);
    this.selectedNodeId = this.nodes[0]?.id ?? '';
    this.selectedProjectId = null;
    this.projectName = 'Untitled Workflow';
    this.statusMessage = 'Started a new unsaved workflow project.';
  }

  protected runWorkflow(): void {
    if (this.isRunning) {
      return;
    }

    this.isRunning = true;
    this.activeNodeId = null;
    this.completedNodeIds.clear();

    this.workflowSequence.forEach((nodeId, index) => {
      const timer = setTimeout(() => {
        this.activeNodeId = nodeId;
        if (index > 0) {
          this.completedNodeIds.add(this.workflowSequence[index - 1]);
        }

        if (index === this.workflowSequence.length - 1) {
          const endTimer = setTimeout(() => {
            this.completedNodeIds.add(nodeId);
            this.activeNodeId = null;
            this.isRunning = false;
          }, 700);
          this.timers.push(endTimer);
        }
      }, 700 * (index + 1));
      this.timers.push(timer);
    });
  }

  protected stopWorkflow(): void {
    this.isRunning = false;
    this.activeNodeId = null;
    this.completedNodeIds.clear();
    this.clearTimers();
  }

  protected getNodeType(typeId: string): StudioNodeType {
    return this.nodeTypesById.get(typeId) ?? this.nodeTypes[0];
  }

  protected isSelected(nodeId: string): boolean {
    return this.selectedNodeId === nodeId;
  }

  protected isActive(nodeId: string): boolean {
    return this.activeNodeId === nodeId;
  }

  protected isCompleted(nodeId: string): boolean {
    return this.completedNodeIds.has(nodeId);
  }

  public ngOnDestroy(): void {
    this.clearTimers();
  }

  private restoreProjects(): void {
    const storage = this.getLocalStorage();
    if (!storage) {
      this.savedProjects = [];
      this.statusMessage = 'Local storage is unavailable. Starting with an empty project list.';
      return;
    }

    let stored: string | null;
    try {
      stored = storage.getItem(this.storageKey);
    } catch {
      this.savedProjects = [];
      this.statusMessage = 'Could not access saved projects. Starting with an empty project list.';
      return;
    }

    if (!stored) {
      return;
    }

    try {
      const parsed = JSON.parse(stored) as StudioProject[];
      this.savedProjects = Array.isArray(parsed)
        ? parsed.filter(
            (entry): entry is StudioProject =>
              !!entry &&
              typeof entry === 'object' &&
              Array.isArray((entry as StudioProject).nodes) &&
              typeof (entry as StudioProject).id === 'string'
          )
        : [];
      if (this.savedProjects.length > 0) {
        this.statusMessage = `Found ${this.savedProjects.length} locally saved project(s).`;
      }
    } catch {
      this.savedProjects = [];
      this.statusMessage = 'Could not parse saved projects. Starting with an empty project list.';
    }
  }

  private persistProjects(): boolean {
    const storage = this.getLocalStorage();
    if (!storage) {
      return false;
    }

    try {
      storage.setItem(this.storageKey, JSON.stringify(this.savedProjects));
      return true;
    } catch {
      return false;
    }
  }

  private createProjectId(): string {
    if (typeof globalThis.crypto?.randomUUID === 'function') {
      return globalThis.crypto.randomUUID();
    }

    return `project_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
  }

  private clearTimers(): void {
    this.timers.forEach((timer) => clearTimeout(timer));
    this.timers = [];
  }

  private getLocalStorage(): Storage | null {
    return typeof globalThis.localStorage === 'undefined' ? null : globalThis.localStorage;
  }

  private cloneNodes(nodes: StudioNode[]): StudioNode[] {
    return nodes.map((node) => ({ ...node }));
  }
}
