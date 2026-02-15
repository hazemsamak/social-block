
// Initial load
document.addEventListener('DOMContentLoaded', () => {
    updateStatus();

    // Initialize Socket.io
    const socket = io({
        reconnection: true,
        reconnectionAttempts: Infinity,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000,
    });

    socket.on('connect', () => {
        console.log('Connected to server via WebSocket');
        updateStatus(); // Refresh status on every connection/reconnection
    });

    socket.on('status_change', (data) => {
        console.log('Received status update:', data);
        applyStatusUI(data.status);
    });

    // Handle visibility changes (e.g., coming back to the tab on mobile)
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            console.log('Tab became visible - refreshing status');
            updateStatus();
        }
    });
});

function applyStatusUI(status) {
    const statusDisplay = document.getElementById('status-display');
    const mainBtn = document.getElementById('main-action-btn');
    const btnText = document.getElementById('btn-text');

    // Remove old classes
    statusDisplay.classList.remove('status-blocked', 'status-unblocked');

    if (status === 'Blocked') {
        statusDisplay.textContent = 'BLOCKED';
        statusDisplay.classList.add('status-blocked');
        btnText.innerHTML = '<i class="fas fa-unlock"></i> Unblock Access';
        mainBtn.setAttribute('data-action', 'unblock');
    } else {
        statusDisplay.textContent = 'UNBLOCKED';
        statusDisplay.classList.add('status-unblocked');
        btnText.innerHTML = '<i class="fas fa-lock"></i> Block Access';
        mainBtn.setAttribute('data-action', 'block');
    }
}

async function updateStatus() {
    try {
        const response = await fetch('/api/v1/social/status');

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        const data = await response.json();
        applyStatusUI(data.status);
    } catch (error) {
        console.error('Error fetching status:', error);
        document.getElementById('status-display').textContent = 'ERROR';
    }
}

async function toggleStatus() {
    const mainBtn = document.getElementById('main-action-btn');
    const btnText = document.getElementById('btn-text');
    const loader = document.getElementById('btn-loader');
    const action = mainBtn.getAttribute('data-action');

    if (!action) return;

    // UI Loading State
    btnText.style.display = 'none';
    loader.style.display = 'block';
    mainBtn.disabled = true;

    try {
        const response = await fetch('/api/v1/social/toggle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: action }),
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        const data = await response.json();

        if (!data.success) {
            alert('Failed to toggle status');
        }
        // Note: UI update is handled by Socket.io listener
    } catch (error) {
        console.error('Error toggling status:', error);
        alert('An error occurred');
    } finally {
        btnText.style.display = 'block';
        loader.style.display = 'none';
        mainBtn.disabled = false;
    }
}
