const API_URL = 'http://localhost:8000';

// DOM Elements
const fetchBtn = document.getElementById('fetchBtn');
const refreshBtn = document.getElementById('refreshBtn');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const hazardousFilter = document.getElementById('hazardousFilter');
const asteroidTableBody = document.getElementById('asteroidTableBody');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const detailModal = document.getElementById('detailModal');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');
const closeModal = document.querySelector('.close');

// Set default dates (today and 7 days from now)
const today = new Date().toISOString().split('T')[0];
const weekFromNow = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
startDateInput.value = today;
endDateInput.value = weekFromNow;

// Event Listeners
fetchBtn.addEventListener('click', fetchFromNASA);
refreshBtn.addEventListener('click', loadAsteroids);
hazardousFilter.addEventListener('change', loadAsteroids);
closeModal.addEventListener('click', () => detailModal.classList.add('hidden'));

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === detailModal) {
        detailModal.classList.add('hidden');
    }
});

// API Functions
async function fetchFromNASA() {
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    
    if (!startDate || !endDate) {
        showError('Please select both start and end dates');
        return;
    }
    if (startDate > endDate) {
        showError('Start date must be before end date');
        return;
    }
    
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch(`${API_URL}/asteroids/fetch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_date: startDate,
                end_date: endDate
            })
        });
        
        if (!response.ok) throw new Error('Failed to fetch from NASA');
        
        const asteroids = await response.json();
        alert(`Fetched ${asteroids.length} asteroids from NASA`);
        loadAsteroids();
    } catch (error) {
        showError('Error fetching from NASA: ' + error.message);
    } finally {
        showLoading(false);
    }
}

async function loadAsteroids() {
    showLoading(true);
    hideError();
    
    try {
        let url = `${API_URL}/asteroids`;
        
        if (hazardousFilter.checked) {
            url = `${API_URL}/asteroids/filter/hazardous`;
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to load asteroids');
        
        const asteroids = await response.json();
        displayAsteroids(asteroids);
    } catch (error) {
        showError('Error loading asteroids: ' + error.message);
    } finally {
        showLoading(false);
    }
}

async function deleteAsteroid(id) {
    if (!confirm('Are you sure you want to delete this asteroid?')) return;
    
    try {
        const response = await fetch(`${API_URL}/asteroids/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete asteroid');
        
        loadAsteroids();
    } catch (error) {
        showError('Error deleting asteroid: ' + error.message);
    }
}

async function showAsteroidDetails(id) {
    try {
        const response = await fetch(`${API_URL}/asteroids/${id}`);
        if (!response.ok) throw new Error('Failed to load asteroid details');
        
        const asteroid = await response.json();
        
        modalTitle.textContent = asteroid.name;
        modalBody.innerHTML = `
            <p><strong>NASA JPL URL:</strong> ${asteroid.nasa_jpl_url ? `<a href="${asteroid.nasa_jpl_url}" target="_blank" rel="noopener">${asteroid.nasa_jpl_url}</a>` : 'N/A'}</p>
            <p><strong>Absolute Magnitude:</strong> ${formatMagnitude(asteroid.absolute_magnitude)}</p>
            <p><strong>Estimated Diameter:</strong> ${formatDiameter(asteroid)} km</p>
            <p><strong>Close Approach Date:</strong> ${asteroid.close_approach_date_full || asteroid.close_approach_date}</p>
            <p><strong>Relative Velocity:</strong> ${formatVelocity(asteroid.relative_velocity)} km/s</p>
            <p><strong>Miss Distance:</strong> ${formatDistance(asteroid.miss_distance)} km</p>
            <p><strong>Potentially Hazardous:</strong> ${asteroid.is_potentially_hazardous ? 'Yes' : 'No'}</p>
            <p><strong>Orbiting Body:</strong> ${asteroid.orbiting_body || 'Unknown'}</p>
            <p><strong>Last Updated:</strong> ${new Date(asteroid.updated_at).toLocaleString()}</p>
        `;
        
        detailModal.classList.remove('hidden');
    } catch (error) {
        showError('Error loading details: ' + error.message);
    }
}

// Display Functions
function displayAsteroids(asteroids) {
    asteroidTableBody.innerHTML = '';
    
    if (asteroids.length === 0) {
        asteroidTableBody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No asteroids found. Try fetching data from NASA.</td></tr>';
        return;
    }
    
    asteroids.forEach(asteroid => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${asteroid.name}</td>
            <td>${formatDiameter(asteroid)}</td>
            <td>${formatVelocity(asteroid.relative_velocity)}</td>
            <td>${formatDistance(asteroid.miss_distance)}</td>
            <td>${asteroid.close_approach_date}</td>
            <td><span class="hazard-badge ${asteroid.is_potentially_hazardous ? 'hazard-yes' : 'hazard-no'}">
                ${asteroid.is_potentially_hazardous ? 'YES' : 'NO'}
            </span></td>
            <td>
                <button onclick="showAsteroidDetails(${asteroid.id})">Details</button>
                <button onclick="deleteAsteroid(${asteroid.id})" style="background: #ef4444;">Delete</button>
            </td>
        `;
        asteroidTableBody.appendChild(row);
    });
}

function showLoading(show) {
    loading.classList.toggle('hidden', !show);
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

function formatDiameter(asteroid) {
    const min = Number.isFinite(asteroid.estimated_diameter_min) ? asteroid.estimated_diameter_min : null;
    const max = Number.isFinite(asteroid.estimated_diameter_max) ? asteroid.estimated_diameter_max : null;

    if (min === null || max === null) {
        return 'N/A';
    }

    return `${min.toFixed(3)} - ${max.toFixed(3)}`;
}

function formatVelocity(value) {
    if (!Number.isFinite(value)) return 'N/A';
    return Number(value).toFixed(2);
}

function formatDistance(value) {
    if (!Number.isFinite(value)) return 'N/A';
    return Number(value)
        .toFixed(0)
        .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function formatMagnitude(value) {
    if (!Number.isFinite(value)) return 'N/A';
    return Number(value).toFixed(2);
}

// Load asteroids on page load
loadAsteroids();