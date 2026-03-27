/**
 * MagnetarPrometheus MVP UI Shell Controller
 *
 * This script provides the interactivity for the static HTML shell.
 * It manages view routing, DOM population, and simulates backend interactions.
 * All data is currently mocked; future iterations will replace this with real HTTP API calls.
 */

/**
 * Mock Data Structure: Workflows
 * Represents registered workflows that would normally be fetched from the backend schema.
 * @type {Array<Object>}
 */
const mockWorkflows = [
    { id: 'wf-001', name: 'Email Triage', description: 'Classifies and routes incoming support emails.', version: '1.2.0', status: 'active' },
    { id: 'wf-002', name: 'Data Processing', description: 'ETL pipeline for nightly data sync.', version: '0.9.1', status: 'draft' },
    { id: 'wf-003', name: 'Weekly Report', description: 'Generates and distributes weekly metrics.', version: '2.0.1', status: 'active' }
];

/**
 * Mock Data Structure: Runs History
 * Represents historical executions. The structure maps to what the backend `RunContext`
 * and summary API endpoints would eventually return.
 * @type {Array<Object>}
 */
const mockRuns = [
    { id: 'run-8f72', workflowId: 'wf-001', workflowName: 'Email Triage', status: 'success', startTime: '2026-04-12T08:30:00Z', duration: '45s' },
    { id: 'run-3a1b', workflowId: 'wf-002', workflowName: 'Data Processing', status: 'failed', startTime: '2026-04-11T23:00:00Z', duration: '12m' },
    { id: 'run-9c4d', workflowId: 'wf-001', workflowName: 'Email Triage', status: 'success', startTime: '2026-04-11T08:30:00Z', duration: '42s' },
    { id: 'run-2e5f', workflowId: 'wf-003', workflowName: 'Weekly Report', status: 'success', startTime: '2026-04-10T09:00:00Z', duration: '3m' },
];

/**
 * Mock Data Structure: Detailed Run Logs
 * Key-value mapping of run IDs to their simulated execution console output.
 * Demonstrates how step-by-step evaluator and module execution logs are rendered.
 * @type {Object.<string, string>}
 */
const mockRunDetails = {
    'run-8f72': `[INFO] Starting workflow execution: Email Triage
[INFO] Loading dependencies...
[INFO] Executing step: extract_content
[INFO] Output: {"subject": "Need help with login", "body": "..."}
[INFO] Executing step: classify_intent
[INFO] Intent classified as: support_request
[INFO] Evaluating branch condition: intent == 'support_request' -> true
[INFO] Executing step: route_to_support
[INFO] Successfully routed to support queue.
[INFO] Workflow completed successfully.
Result: {
  "status": "success",
  "final_context": {
    "intent": "support_request",
    "routed": true
  }
}`,
    'run-3a1b': `[INFO] Starting workflow execution: Data Processing
[INFO] Executing step: fetch_data
[ERROR] Connection timeout to source database.
[ERROR] Workflow failed.
Result: {
  "status": "error",
  "error_message": "Connection timeout"
}`
};

// DOM Elements
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view');
const viewTitle = document.getElementById('current-view-title');
const dashboardActivityList = document.getElementById('dashboard-activity-list');
const workflowsTableBody = document.getElementById('workflows-table-body');
const runsHistoryList = document.getElementById('runs-history-list');
const runDetailsTitle = document.getElementById('run-details-title');
const runMetadata = document.getElementById('run-metadata');
const runConsoleOutput = document.getElementById('run-console-output').querySelector('code');

// Modal Elements
const runExampleBtn = document.getElementById('run-example-btn');
const runModal = document.getElementById('run-modal');
const closeBtn = document.querySelector('.close-btn');
const modalCloseBtn = document.getElementById('modal-close-btn');
const modalViewRunBtn = document.getElementById('modal-view-run-btn');
const modalExecutionStatus = document.getElementById('modal-execution-status');
const modalConsoleOutput = document.getElementById('modal-console-output').querySelector('code');

/**
 * Formats an ISO 8601 date string into a user-friendly locale string.
 * @param {string} dateString - The raw date string to format.
 * @returns {string} The localized date and time.
 */
const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
};

/**
 * Generates HTML for a standardized status badge component.
 * @param {string} status - The status text (e.g., 'active', 'success', 'failed').
 * @returns {string} The raw HTML string for the badge.
 */
const getStatusBadge = (status) => {
    return `<span class="status-badge ${status}">${status.toUpperCase()}</span>`;
};

/**
 * Navigation / View Router Controller
 * Listens for clicks on the sidebar items and toggles the visibility
 * of the main `<section>` views by updating the `active` CSS class.
 */
navItems.forEach(item => {
    item.addEventListener('click', () => {
        // Update active nav
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');

        // Update view
        const targetViewId = item.getAttribute('data-target');
        views.forEach(view => {
            if (view.id === targetViewId) {
                view.classList.add('active');
                viewTitle.textContent = item.textContent.trim();
            } else {
                view.classList.remove('active');
            }
        });
    });
});

/**
 * Renders the Recent Activity list on the Dashboard view.
 * Slices the mockRuns array to show only the most recent items.
 */
const populateDashboard = () => {
    dashboardActivityList.innerHTML = '';
    mockRuns.slice(0, 3).forEach(run => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${run.workflowName}</strong> run ${run.id} finished with status ${getStatusBadge(run.status)}
            <span class="activity-time">${formatDate(run.startTime)}</span>
        `;
        dashboardActivityList.appendChild(li);
    });
};

/**
 * Renders the rows inside the Workflows table view.
 * Populates name, description, status badges, and stub action buttons.
 */
const populateWorkflows = () => {
    workflowsTableBody.innerHTML = '';
    mockWorkflows.forEach(wf => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${wf.name}</strong><br><small class="text-muted">${wf.id}</small></td>
            <td>${wf.description}</td>
            <td>${wf.version}</td>
            <td>${getStatusBadge(wf.status)}</td>
            <td>
                <button class="secondary-btn" onclick="alert('Graph View Not Implemented Yet')">View Graph</button>
            </td>
        `;
        workflowsTableBody.appendChild(tr);
    });
};

/**
 * Renders the Runs view console.
 * This creates a selectable list of past runs on the left.
 * Clicking a run triggers `displayRunDetails` to show its logs and metadata on the right.
 */
const populateRuns = () => {
    runsHistoryList.innerHTML = '';
    mockRuns.forEach((run, index) => {
        const li = document.createElement('li');
        li.className = `run-item ${index === 0 ? 'selected' : ''}`;
        li.dataset.runId = run.id;
        li.innerHTML = `
            <div class="run-item-header">
                <span class="run-item-id">${run.id}</span>
                ${getStatusBadge(run.status)}
            </div>
            <div class="run-item-workflow">${run.workflowName}</div>
            <div class="run-item-time">${formatDate(run.startTime)}</div>
        `;

        li.addEventListener('click', () => {
            document.querySelectorAll('.run-item').forEach(el => el.classList.remove('selected'));
            li.classList.add('selected');
            displayRunDetails(run);
        });

        runsHistoryList.appendChild(li);
    });

    // Display details for first run initially
    if (mockRuns.length > 0) {
        displayRunDetails(mockRuns[0]);
    }
};

/**
 * Updates the right-hand panel of the Runs view with detailed metadata and logs
 * for the currently selected run. Simulates network loading latency for realism.
 * @param {Object} run - The specific run object payload.
 */
const displayRunDetails = (run) => {
    runDetailsTitle.textContent = `Run: ${run.id} - ${run.workflowName}`;
    runMetadata.innerHTML = `
        <div class="metadata-item">Status: <span>${run.status.toUpperCase()}</span></div>
        <div class="metadata-item">Started: <span>${formatDate(run.startTime)}</span></div>
        <div class="metadata-item">Duration: <span>${run.duration}</span></div>
    `;

    // Simulate loading logs
    runConsoleOutput.textContent = 'Fetching logs...';
    setTimeout(() => {
        runConsoleOutput.textContent = mockRunDetails[run.id] || '[INFO] No logs available for this run.';
    }, 300);
};

/**
 * Run Execution Simulator (Modal Logic)
 *
 * Demonstrates a user-facing interactive flow for triggering a workflow execution.
 * Instead of waiting for a single batch response, it simulates streaming console
 * output to demonstrate step-by-step progression and evaluator routing.
 */
const openModal = () => {
    runModal.classList.add('active');
    modalExecutionStatus.innerHTML = '<span class="spinner"></span> Executing: Email Triage Example...';
    modalConsoleOutput.textContent = '[INFO] Starting workflow engine...\\n[INFO] Loading dependencies...';
    modalViewRunBtn.disabled = true;

    // Simulate execution sequence
    setTimeout(() => {
        modalConsoleOutput.textContent += '\\n[INFO] Executing step: extract_content';
    }, 1000);

    setTimeout(() => {
        modalConsoleOutput.textContent += '\\n[INFO] Output: {"subject": "Test", "body": "Hello"}';
        modalConsoleOutput.textContent += '\\n[INFO] Executing step: classify_intent';
    }, 2000);

    setTimeout(() => {
        modalConsoleOutput.textContent += '\\n[INFO] Intent classified as: general_inquiry';
        modalConsoleOutput.textContent += '\\n[INFO] Workflow completed successfully.';
        modalConsoleOutput.textContent += '\\n\\nResult: {\\n  "status": "success",\\n  "final_context": {\\n    "intent": "general_inquiry"\\n  }\\n}';

        modalExecutionStatus.innerHTML = '<span style="color: var(--success-color);">✓ Execution Complete</span>';
        modalViewRunBtn.disabled = false;
    }, 3500);
};

const closeModal = () => {
    runModal.classList.remove('active');
};

runExampleBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
modalCloseBtn.addEventListener('click', closeModal);

modalViewRunBtn.addEventListener('click', () => {
    closeModal();
    // Navigate to Runs view
    navItems[2].click();
    // In a real app, we'd add the new run to the mock data and select it
});

// Initialize
/**
 * Application Entrypoint
 * Bootstraps the mock data into the DOM upon initial page load.
 */
const init = () => {
    populateDashboard();
    populateWorkflows();
    populateRuns();
};

// Run init
init();
