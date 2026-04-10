/**
 * Workflow Studio page.
 *
 * This component delivers a user-visible redesign of the existing Angular studio route
 * without replacing the application architecture. The page remains an Angular feature
 * screen and now provides a richer n8n-like operator experience with:
 * - a branded top toolbar,
 * - an actionable node library,
 * - an interactive workflow canvas,
 * - and an inspector/debug panel.
 *
 * The implementation intentionally keeps state local and deterministic so the visual
 * improvements can ship safely before runtime/API wiring is completed.
 */
import { NgClass, NgFor, NgIf } from '@angular/common';
import { Component, OnDestroy } from '@angular/core';

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

@Component({
  imports: [NgFor, NgIf, NgClass],
  templateUrl: './workflow-studio-page.component.html',
  styleUrl: './workflow-studio-page.component.css'
})
export class WorkflowStudioPageComponent implements OnDestroy {
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

  protected readonly nodes: StudioNode[] = [
    { id: 'node_trigger', typeId: 'trigger_http', label: 'New Lead Form', summary: 'POST /api/leads/new', x: 72, y: 128 },
    { id: 'node_ai', typeId: 'process_ai', label: 'Enrich & Score', summary: 'Analyze lead context', x: 384, y: 128 },
    { id: 'node_logic', typeId: 'logic_if', label: 'Is High Quality?', summary: 'Score >= 80', x: 696, y: 128 },
    { id: 'node_db', typeId: 'integration_db', label: 'Save VIP Lead', summary: 'salesforce_leads', x: 1008, y: 48 },
    { id: 'node_email', typeId: 'integration_email', label: 'Nurture Drip', summary: 'template: nurture_1', x: 1008, y: 232 }
  ];

  protected selectedNodeId: string = 'node_ai';
  protected isRunning = false;
  protected activeNodeId: string | null = null;
  protected completedNodeIds = new Set<string>();

  private timers: ReturnType<typeof setTimeout>[] = [];

  protected selectNode(nodeId: string): void {
    this.selectedNodeId = nodeId;
  }

  protected runWorkflow(): void {
    if (this.isRunning) {
      return;
    }

    this.isRunning = true;
    this.activeNodeId = null;
    this.completedNodeIds.clear();

    const sequence = ['node_trigger', 'node_ai', 'node_logic', 'node_db'];
    sequence.forEach((nodeId, index) => {
      const timer = setTimeout(() => {
        this.activeNodeId = nodeId;
        if (index > 0) {
          this.completedNodeIds.add(sequence[index - 1]);
        }

        if (index === sequence.length - 1) {
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
    return (
      this.nodeTypes.find((type) => type.id === typeId) ??
      this.nodeTypes[0]
    );
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

  ngOnDestroy(): void {
    this.clearTimers();
  }

  private clearTimers(): void {
    this.timers.forEach((timer) => clearTimeout(timer));
    this.timers = [];
  }
}
