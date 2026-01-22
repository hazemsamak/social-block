
async function updateStatus() {
    const statusDisplay = document.getElementById('status-display');
    const mainBtn = document.getElementById('main-action-btn');
    const btnText = document.getElementById('btn-text');

    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        // Remove old classes
        statusDisplay.classList.remove('status-blocked', 'status-unblocked');

        if (data.status === 'Blocked') {
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
    } catch (error) {
        console.error('Error fetching status:', error);
        statusDisplay.textContent = 'ERROR';
    }
}

async function toggleStatus() {
    const mainBtn = document.getElementById('main-action-btn');
    const btnText = document.getElementById('btn-text');
    const loader = document.getElementById('btn-loader');
    const action = mainBtn.getAttribute('data-action');

    if (!action) return; // Wait for initial status load

    // UI Loading State
    btnText.style.display = 'none';
    loader.style.display = 'block';
    mainBtn.disabled = true;

    try {
        const response = await fetch('/api/toggle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: action }),
        });

        const data = await response.json();

        if (data.success) {
            await updateStatus(); // Refresh UI with new state
        } else {
            alert('Failed to toggle status');
        }
    } catch (error) {
        console.error('Error toggling status:', error);
        alert('An error occurred');
    } finally {
        btnText.style.display = 'block';
        loader.style.display = 'none';
        mainBtn.disabled = false;
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', updateStatus);
