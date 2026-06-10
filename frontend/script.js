// Web Attendance Tracker - Frontend JavaScript

const API_URL = 'http://localhost:8000/api';
let currentFilters = {};

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    loadAttendanceRecords();
    setupEventListeners();
    setTodayDate();
    updateStatistics();
});

// Set today's date as default
function setTodayDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', switchTab);
    });
    
    // Form submission
    document.getElementById('attendanceForm').addEventListener('submit', handleFormSubmit);
    
    // Filter inputs
    document.getElementById('filterStudent').addEventListener('input', handleFilterChange);
    document.getElementById('filterClass').addEventListener('input', handleFilterChange);
    document.getElementById('filterDate').addEventListener('input', handleFilterChange);
    document.getElementById('filterStatus').addEventListener('change', handleFilterChange);
    
    // Reset filters
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
    
    // Edit modal
    document.getElementById('editForm').addEventListener('submit', handleEditSubmit);
    document.getElementById('closeModal').addEventListener('click', closeEditModal);
    document.getElementById('cancelEdit').addEventListener('click', closeEditModal);
}

// Switch tabs
function switchTab(e) {
    const tabName = e.target.dataset.tab;
    
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Deactivate all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    e.target.classList.add('active');
    
    // Load predictions if predictions tab
    if (tabName === 'predictions') {
        loadPredictions();
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        student_name: document.getElementById('studentName').value,
        class_name: document.getElementById('className').value,
        date: document.getElementById('date').value,
        status: document.getElementById('status').value,
        time_in: document.getElementById('timeIn').value || null,
        time_out: document.getElementById('timeOut').value || null,
        notes: document.getElementById('notes').value || null
    };
    
    try {
        const response = await fetch(`${API_URL}/attendance`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to add attendance record');
        }
        
        showNotification('Record added successfully!', 'success');
        document.getElementById('attendanceForm').reset();
        setTodayDate();
        loadAttendanceRecords();
        updateStatistics();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error adding record: ' + error.message, 'error');
    }
}

// Load attendance records
async function loadAttendanceRecords() {
    try {
        let url = `${API_URL}/attendance?skip=0&limit=100`;
        
        // Add filters
        if (currentFilters.student_name) {
            url += `&student_name=${encodeURIComponent(currentFilters.student_name)}`;
        }
        if (currentFilters.class_name) {
            url += `&class_name=${encodeURIComponent(currentFilters.class_name)}`;
        }
        if (currentFilters.date) {
            url += `&date=${currentFilters.date}`;
        }
        if (currentFilters.status) {
            url += `&status=${currentFilters.status}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to load records');
        }
        
        const records = await response.json();
        displayRecords(records);
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error loading records: ' + error.message, 'error');
    }
}

// Display records in table
function displayRecords(records) {
    const tableBody = document.getElementById('tableBody');
    
    if (records.length === 0) {
        tableBody.innerHTML = '<tr class="empty-row"><td colspan="8">No records found.</td></tr>';
        return;
    }
    
    tableBody.innerHTML = records.map(record => `
        <tr>
            <td>${record.id}</td>
            <td>${record.student_name}</td>
            <td>${record.class_name}</td>
            <td>${record.date}</td>
            <td><span class="status-badge ${record.status}">${record.status}</span></td>
            <td>${record.time_in || '-'}</td>
            <td>${record.time_out || '-'}</td>
            <td>
                <div class="actions">
                    <button class="btn btn-info" onclick="openEditModal(${record.id})">✏️ Edit</button>
                    <button class="btn btn-danger" onclick="deleteRecord(${record.id})">🗑️ Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Update statistics
async function updateStatistics() {
    try {
        let url = `${API_URL}/attendance/stats`;
        
        // Add filters
        if (currentFilters.class_name) {
            url += `?class_name=${encodeURIComponent(currentFilters.class_name)}`;
        }
        if (currentFilters.date) {
            url += (url.includes('?') ? '&' : '?') + `date=${currentFilters.date}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }
        
        const stats = await response.json();
        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statPresent').textContent = stats.present;
        document.getElementById('statAbsent').textContent = stats.absent;
        document.getElementById('statRate').textContent = stats.attendance_rate + '%';
    } catch (error) {
        console.error('Error updating statistics:', error);
    }
}

// Handle filter changes
function handleFilterChange() {
    currentFilters.student_name = document.getElementById('filterStudent').value;
    currentFilters.class_name = document.getElementById('filterClass').value;
    currentFilters.date = document.getElementById('filterDate').value;
    currentFilters.status = document.getElementById('filterStatus').value;
    
    loadAttendanceRecords();
    updateStatistics();
}

// Reset filters
function resetFilters() {
    document.getElementById('filterStudent').value = '';
    document.getElementById('filterClass').value = '';
    document.getElementById('filterDate').value = '';
    document.getElementById('filterStatus').value = '';
    
    currentFilters = {};
    loadAttendanceRecords();
    updateStatistics();
    showNotification('Filters reset', 'success');
}

// Load predictions
async function loadPredictions() {
    try {
        const response = await fetch(`${API_URL}/predict?days_ahead=7`);
        if (!response.ok) {
            throw new Error('Failed to load predictions');
        }
        
        const predictions = await response.json();
        displayPredictions(predictions);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('predictionsContainer').innerHTML = 
            '<p>AI predictions not available yet. Add more attendance records to train the model.</p>';
    }
}

// Display predictions
function displayPredictions(predictions) {
    const container = document.getElementById('predictionsContainer');
    
    if (predictions.length === 0) {
        container.innerHTML = '<p>No predictions available yet.</p>';
        return;
    }
    
    container.innerHTML = predictions.map(pred => `
        <div class="prediction-card">
            <h4>${pred.student_name}</h4>
            <p><strong>Date:</strong> ${pred.predicted_date}</p>
            <p><strong>Prediction:</strong> <span class="status-badge ${pred.predicted_status}">${pred.predicted_status}</span></p>
            <div class="prediction-confidence">
                Confidence: ${(pred.confidence * 100).toFixed(1)}%
            </div>
            ${pred.reason ? `<p><strong>Reason:</strong> ${pred.reason}</p>` : ''}
        </div>
    `).join('');
}

// Open edit modal
async function openEditModal(id) {
    try {
        const response = await fetch(`${API_URL}/attendance/${id}`);
        if (!response.ok) {
            throw new Error('Failed to load record');
        }
        
        const record = await response.json();
        
        document.getElementById('editId').value = record.id;
        document.getElementById('editStudentName').value = record.student_name;
        document.getElementById('editClassName').value = record.class_name;
        document.getElementById('editDate').value = record.date;
        document.getElementById('editStatus').value = record.status;
        document.getElementById('editTimeIn').value = record.time_in || '';
        document.getElementById('editTimeOut').value = record.time_out || '';
        
        document.getElementById('editModal').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error loading record: ' + error.message, 'error');
    }
}

// Close edit modal
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Handle edit submission
async function handleEditSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('editId').value;
    const formData = {
        student_name: document.getElementById('editStudentName').value,
        class_name: document.getElementById('editClassName').value,
        date: document.getElementById('editDate').value,
        status: document.getElementById('editStatus').value,
        time_in: document.getElementById('editTimeIn').value || null,
        time_out: document.getElementById('editTimeOut').value || null
    };
    
    try {
        const response = await fetch(`${API_URL}/attendance/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update record');
        }
        
        showNotification('Record updated successfully!', 'success');
        closeEditModal();
        loadAttendanceRecords();
        updateStatistics();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error updating record: ' + error.message, 'error');
    }
}

// Delete record
async function deleteRecord(id) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/attendance/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete record');
        }
        
        showNotification('Record deleted successfully!', 'success');
        loadAttendanceRecords();
        updateStatistics();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error deleting record: ' + error.message, 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification show ${type}`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeEditModal();
    }
});
