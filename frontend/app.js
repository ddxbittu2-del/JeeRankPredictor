/* =====================================================
   JEE RANK PREDICTOR — FRONTEND APPLICATION (VANILLA JS)
   ===================================================== */

// ===== CONFIG =====
const CONFIG = {
    // Toggle between local dev and production
    USE_LOCAL: false,
    LOCAL_API: 'http://localhost:8080',
    PROD_API: 'https://jee-rank-backend.onrender.com',
};

const API_BASE = CONFIG.USE_LOCAL ? CONFIG.LOCAL_API : CONFIG.PROD_API;

// Debounce utility
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// ===== STATE MANAGEMENT =====
const AppState = {
    currentStep: 1,
    formData: {
        score: 0,
        inputType: 'marks',
        year: 2024,
        category: 'GEN',
        seatPool: 'GN',
        homeState: 'All India',
        instituteTypes: ['All'],
        branches: ['CSE', 'ECE', 'ME', 'CE', 'EE', 'Chemical', 'Metallurgy', 'Physics'],
    },
    predictionResult: null,
    collegesData: [],
    currentPage: 1,
    itemsPerPage: 20,
    sortBy: 'probability',
    sortOrder: 'desc',
    filterType: 'All',
    searchQuery: '',
    whatIfRankDelta: 0,
    selectedColleges: [],
};

// ===== FORM CONTROLLER =====
const FormController = {
    init() {
        this.attachEventListeners();
    },

    attachEventListeners() {
        // Score type toggle
        document.querySelectorAll('#scoreTypeToggle .toggle-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('#scoreTypeToggle .toggle-btn').forEach((b) => b.classList.remove('active'));
                e.target.classList.add('active');
                AppState.formData.inputType = e.target.dataset.type;
                
                // Update input field constraints based on input type
                const scoreInput = document.getElementById('scoreInput');
                const scoreLabel = document.getElementById('scoreLabel');
                
                if (e.target.dataset.type === 'marks') {
                    scoreInput.max = 300;
                    scoreInput.placeholder = 'Enter marks (0-300)';
                    scoreLabel.textContent = '(0-300)';
                } else if (e.target.dataset.type === 'percentile') {
                    scoreInput.max = 100;
                    scoreInput.placeholder = 'Enter percentile (0-100)';
                    scoreLabel.textContent = '(0-100)';
                } else {
                    scoreInput.max = 1000000;
                    scoreInput.placeholder = 'Enter your rank';
                    scoreLabel.textContent = '(Rank)';
                }
                
                // Clear the input and preview when switching
                scoreInput.value = '';
                AppState.formData.score = 0;
                document.getElementById('livePreview').textContent = '';
            });
        });

        // Seat pool toggle
        document.querySelectorAll('#seatPoolToggle .toggle-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('#seatPoolToggle .toggle-btn').forEach((b) => b.classList.remove('active'));
                e.target.classList.add('active');
                AppState.formData.seatPool = e.target.dataset.pool;
            });
        });

        // Institute type selection
        document.querySelectorAll('#instituteTypeToggle .toggle-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const instituteType = e.target.dataset.institute;
                if (instituteType === 'All') {
                    AppState.formData.instituteTypes = ['All'];
                    document.querySelectorAll('#instituteTypeToggle .toggle-btn').forEach((b) => b.classList.remove('active'));
                    e.target.classList.add('active');
                } else {
                    const idx = AppState.formData.instituteTypes.indexOf('All');
                    if (idx > -1) AppState.formData.instituteTypes.splice(idx, 1);

                    if (AppState.formData.instituteTypes.includes(instituteType)) {
                        AppState.formData.instituteTypes = AppState.formData.instituteTypes.filter((t) => t !== instituteType);
                        e.target.classList.remove('active');
                    } else {
                        AppState.formData.instituteTypes.push(instituteType);
                        e.target.classList.add('active');
                    }

                    if (AppState.formData.instituteTypes.length === 0) {
                        AppState.formData.instituteTypes = ['All'];
                    }
                }
                this.updateInstituteTypeUI();
            });
        });

        // Score input with live preview
        document.getElementById('scoreInput').addEventListener('input', (e) => {
            AppState.formData.score = parseFloat(e.target.value) || 0;
            this.updateLivePreview();
        });

        // Year selector
        document.getElementById('yearSelect').addEventListener('change', (e) => {
            AppState.formData.year = parseInt(e.target.value);
        });

        // Category selector
        document.getElementById('categorySelect').addEventListener('change', (e) => {
            AppState.formData.category = e.target.value;
        });

        // State selector
        document.getElementById('stateSelect').addEventListener('change', (e) => {
            AppState.formData.homeState = e.target.value;
        });

        // Filter chips
        document.querySelectorAll('.filter-chip').forEach((chip) => {
            chip.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-chip').forEach((c) => c.classList.remove('active'));
                e.target.classList.add('active');
                AppState.filterType = e.target.dataset.filter;
                AppState.currentPage = 1;
                this.renderCollegesTable();
            });
        });

        // Search box
        document.getElementById('collegeSearch').addEventListener('input', debounce((e) => {
            AppState.searchQuery = e.target.value.toLowerCase();
            AppState.currentPage = 1;
            this.renderCollegesTable();
        }, 300));

        // Sort buttons
        document.getElementById('sortProbability').addEventListener('click', () => {
            if (AppState.sortBy === 'probability') {
                AppState.sortOrder = AppState.sortOrder === 'desc' ? 'asc' : 'desc';
            } else {
                AppState.sortBy = 'probability';
                AppState.sortOrder = 'desc';
            }
            AppState.currentPage = 1;
            this.renderCollegesTable();
        });

        document.getElementById('sortPackage').addEventListener('click', () => {
            if (AppState.sortBy === 'package') {
                AppState.sortOrder = AppState.sortOrder === 'desc' ? 'asc' : 'desc';
            } else {
                AppState.sortBy = 'package';
                AppState.sortOrder = 'desc';
            }
            AppState.currentPage = 1;
            this.renderCollegesTable();
        });

        document.getElementById('sortInstitute').addEventListener('click', () => {
            if (AppState.sortBy === 'institute') {
                AppState.sortOrder = AppState.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                AppState.sortBy = 'institute';
                AppState.sortOrder = 'asc';
            }
            AppState.currentPage = 1;
            this.renderCollegesTable();
        });

        // What-if slider
        document.getElementById('whatIfSlider').addEventListener('input', debounce((e) => {
            const delta = parseInt(e.target.value);
            AppState.whatIfRankDelta = delta;
            document.getElementById('currentRankAdjust').textContent = delta > 0 ? '+' + delta.toLocaleString() : delta.toLocaleString();
            document.getElementById('sliderMinLabel').textContent = Math.max(0, AppState.predictionResult.predicted_rank - 20000).toLocaleString();
            document.getElementById('sliderMaxLabel').textContent = (AppState.predictionResult.predicted_rank + 20000).toLocaleString();
            this.handleWhatIfSlider();
        }, 600));

        // Pagination
        document.getElementById('prevPage').addEventListener('click', () => {
            if (AppState.currentPage > 1) {
                AppState.currentPage--;
                this.renderCollegesTable();
            }
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            AppState.currentPage++;
            this.renderCollegesTable();
        });
    },

    updateInstituteTypeUI() {
        document.querySelectorAll('#instituteTypeToggle .toggle-btn').forEach((btn) => {
            const type = btn.dataset.institute;
            if (AppState.formData.instituteTypes.includes(type) || AppState.formData.instituteTypes.includes('All')) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    },

    updateLivePreview() {
        const { score, inputType, year } = AppState.formData;
        if (score === 0) {
            document.getElementById('livePreview').textContent = '';
            return;
        }

        // Call API for live rank estimate
        API.estimateRank(score, inputType, year).then((data) => {
            if (data) {
                document.getElementById('livePreview').textContent = `Estimated Rank: ~${data.min_rank.toLocaleString()} – ${data.max_rank.toLocaleString()}`;
            }
        });
    },

    showStep(step) {
        document.getElementById('heroSection').style.display = 'none';
        document.getElementById('formSection').style.display = 'block';

        document.querySelectorAll('.step-form').forEach((form) => form.style.display = 'none');
        document.getElementById(`step${step}`).style.display = 'block';

        AppState.currentStep = step;
        this.updateProgressBar();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    handleStepNext(step) {
        if (this.validateStep(step)) {
            if (step === 1) {
                AppState.formData.year = parseInt(document.getElementById('yearSelect').value);
            } else if (step === 2) {
                AppState.formData.category = document.getElementById('categorySelect').value;
                AppState.formData.homeState = document.getElementById('stateSelect').value;
            }
            this.showStep(step + 1);
        } else {
            alert('Please fill all required fields correctly.');
        }
    },

    handleStepBack(step) {
        this.showStep(step - 1);
    },

    validateStep(step) {
        if (step === 1) {
            return AppState.formData.score > 0;
        } else if (step === 2) {
            return AppState.formData.category && AppState.formData.homeState;
        }
        return true;
    },

    handlePredict() {
        // Collect branch preferences
        const branches = [];
        document.querySelectorAll('[name="branch"]:checked').forEach((checkbox) => {
            branches.push(checkbox.value);
        });
        AppState.formData.branches = branches;

        if (branches.length === 0) {
            alert('Please select at least one branch.');
            return;
        }

        Loader.show('Analyzing your profile and predicted rank...');

        // Step 1: Predict rank
        API.predictRank({
            score: AppState.formData.score,
            input_type: AppState.formData.inputType,
            year: AppState.formData.year,
            category: AppState.formData.category,
        })
            .then((rankData) => {
                AppState.predictionResult = rankData;

                // Step 2: Predict colleges
                return API.predictColleges({
                    rank: rankData.predicted_rank,
                    category: AppState.formData.category,
                    seat_pool: AppState.formData.seatPool,
                    home_state: AppState.formData.homeState,
                    institute_types: AppState.formData.instituteTypes,
                    branches: AppState.formData.branches,
                });
            })
            .then((collegesData) => {
                AppState.collegesData = collegesData;
                Loader.hide();
                this.showResults();
            })
            .catch((error) => {
                Loader.hide();
                console.error('Prediction error:', error);
                alert('Error in prediction. Please try again.');
            });
    },

    showResults() {
        document.getElementById('formSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';
        AppState.currentPage = 1;

        ResultsController.renderRankCard(AppState.predictionResult);
        ResultsController.renderGauge(AppState.predictionResult);
        ResultsController.renderCollegesTable();
        ResultsController.renderPackageChart();

        // Load from URL if shared
        ShareController.loadFromURL();

        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    renderCollegesTable() {
        // Filter and search
        let filtered = AppState.collegesData;

        if (AppState.filterType !== 'All') {
            filtered = filtered.filter((c) => c.institute_type === AppState.filterType);
        }

        if (AppState.searchQuery) {
            filtered = filtered.filter((c) =>
                c.institute.toLowerCase().includes(AppState.searchQuery) || c.program.toLowerCase().includes(AppState.searchQuery)
            );
        }

        // Sort
        filtered.sort((a, b) => {
            let aVal, bVal;
            if (AppState.sortBy === 'probability') {
                aVal = a.probability;
                bVal = b.probability;
            } else if (AppState.sortBy === 'package') {
                aVal = a.avg_package_lpa || 0;
                bVal = b.avg_package_lpa || 0;
            } else if (AppState.sortBy === 'institute') {
                aVal = a.institute;
                bVal = b.institute;
            }

            if (typeof aVal === 'string') {
                return AppState.sortOrder === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
            }
            return AppState.sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
        });

        // Paginate
        const totalPages = Math.ceil(filtered.length / AppState.itemsPerPage);
        const start = (AppState.currentPage - 1) * AppState.itemsPerPage;
        const paged = filtered.slice(start, start + AppState.itemsPerPage);

        // Render
        const tbody = document.getElementById('collegesTableBody');
        tbody.innerHTML = '';

        paged.forEach((college, idx) => {
            const row = document.createElement('tr');
            const probClass = college.probability > 0.8 ? 'high' : college.probability > 0.4 ? 'medium' : 'low';
            const probText = (college.probability * 100).toFixed(1) + '%';

            row.innerHTML = `
                <td>${start + idx + 1}</td>
                <td><strong>${college.institute}</strong></td>
                <td>${college.program}</td>
                <td>${college.institute_type}</td>
                <td>${college.quota || 'AI'}</td>
                <td>${college.opening_rank.toLocaleString()}</td>
                <td>${college.closing_rank.toLocaleString()}</td>
                <td><span class="prob-pill ${probClass}">${probText}</span></td>
                <td>${college.avg_package_lpa ? college.avg_package_lpa.toFixed(2) + ' LPA' : 'N/A'}</td>
                <td><button class="expand-btn" onclick="ResultsController.toggleExpandedRow(event, ${start + idx})">▼</button></td>
            `;

            row.addEventListener('click', () => {
                document.querySelectorAll('.data-table tbody tr').forEach((r) => {
                    if (r.dataset.expanded !== 'true') {
                        r.style.backgroundColor = '';
                    }
                });
                if (row.dataset.expanded !== 'true') {
                    row.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                    row.dataset.expanded = 'true';
                }
            });

            tbody.appendChild(row);
        });

        // Update pagination
        document.getElementById('paginationInfo').textContent = `Page ${AppState.currentPage} of ${Math.max(1, totalPages)}`;
        document.getElementById('prevPage').disabled = AppState.currentPage === 1;
        document.getElementById('nextPage').disabled = AppState.currentPage >= totalPages;
    },

    handleWhatIfSlider() {
        const newRank = AppState.predictionResult.predicted_rank + AppState.whatIfRankDelta;

        API.predictColleges({
            rank: newRank,
            category: AppState.formData.category,
            seat_pool: AppState.formData.seatPool,
            home_state: AppState.formData.homeState,
            institute_types: AppState.formData.instituteTypes,
            branches: AppState.formData.branches,
        })
            .then((collegesData) => {
                AppState.collegesData = collegesData;
                AppState.currentPage = 1;
                this.renderCollegesTable();
            });
    },

    resetForm() {
        AppState.currentStep = 1;
        AppState.formData = {
            score: 0,
            inputType: 'marks',
            year: 2024,
            category: 'GEN',
            seatPool: 'GN',
            homeState: 'All India',
            instituteTypes: ['All'],
            branches: ['CSE', 'ECE', 'ME', 'CE', 'EE', 'Chemical', 'Metallurgy', 'Physics'],
        };
        AppState.predictionResult = null;
        AppState.collegesData = [];
        AppState.whatIfRankDelta = 0;

        document.getElementById('scoreInput').value = '';
        document.getElementById('livePreview').textContent = '';
        document.getElementById('yearSelect').value = '2024';
        document.getElementById('categorySelect').value = 'GEN';
        document.getElementById('stateSelect').value = 'All India';
        document.getElementById('whatIfSlider').value = '0';

        this.showStep(1);
    },

    updateProgressBar() {
        const progress = (AppState.currentStep / 3) * 100;
        document.getElementById('progressBar').style.width = progress + '%';
    },
};

// ===== RESULTS CONTROLLER =====
const ResultsController = {
    renderRankCard(data) {
        const rankNumber = document.getElementById('rankNumber');
        const rankSubtext = document.getElementById('rankSubtext');
        const percentileValue = document.getElementById('percentileValue');
        const rangeValue = document.getElementById('rangeValue');
        const rankBadge = document.getElementById('rankBadge');

        rankNumber.textContent = data.predicted_rank.toLocaleString();
        rankSubtext.textContent = 'Based on your inputs and historical data';
        percentileValue.textContent = data.percentile.toFixed(2) + '%';
        rangeValue.textContent = `${data.confidence_range[0].toLocaleString()} – ${data.confidence_range[1].toLocaleString()}`;

        rankBadge.innerHTML = `
            <span><strong>${AppState.formData.score}</strong> ${AppState.formData.inputType}</span> | 
            <span><strong>${AppState.formData.category}</strong></span> | 
            <span><strong>${AppState.formData.seatPool === 'GN' ? 'Gender-Neutral' : 'Female-Only'}</strong></span>
        `;

        // Animate counter
        this.animateCounter(rankNumber, data.predicted_rank, 1500);
    },

    animateCounter(element, targetNumber, duration) {
        const start = 0;
        const increment = targetNumber / (duration / 16);
        let current = start;

        const counter = setInterval(() => {
            current += increment;
            if (current >= targetNumber) {
                current = targetNumber;
                clearInterval(counter);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 16);
    },

    renderGauge(data) {
        const probability = Math.min(data.confidence_range[0] / AppState.predictionResult.predicted_rank, 1);
        const percentage = Math.round(probability * 100);

        document.getElementById('gaugePercentage').textContent = percentage + '%';

        // Animate SVG progress
        const progressPath = document.querySelector('.gauge-progress');
        if (progressPath) {
            const circumference = 220;
            progressPath.style.strokeDashoffset = circumference - (circumference * probability);
        }
    },

    renderCollegesTable() {
        FormController.renderCollegesTable();
    },

    renderPackageChart() {
        // Group by branch and calculate average package
        const branchPackages = {};
        AppState.collegesData.forEach((college) => {
            if (!branchPackages[college.program]) {
                branchPackages[college.program] = { total: 0, count: 0 };
            }
            branchPackages[college.program].total += college.avg_package_lpa || 0;
            branchPackages[college.program].count++;
        });

        // Convert to array and sort
        let branchData = Object.entries(branchPackages)
            .map(([branch, data]) => ({
                branch,
                avgPackage: data.count > 0 ? data.total / data.count : 0,
            }))
            .sort((a, b) => b.avgPackage - a.avgPackage)
            .slice(0, 5);

        // Render chart
        const canvas = document.getElementById('packageChart');
        if (canvas && window.Chart) {
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: branchData.map((d) => d.branch),
                    datasets: [
                        {
                            label: 'Avg Package (LPA)',
                            data: branchData.map((d) => d.avgPackage),
                            backgroundColor: '#ffffff',
                            borderColor: '#ffffff',
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: { color: '#999999' },
                            grid: { color: '#2a2a2a' },
                        },
                        y: {
                            ticks: { color: '#999999' },
                            grid: { display: false },
                        },
                    },
                },
            });
        }
    },

    toggleExpandedRow(e, index) {
        e.preventDefault();
        e.stopPropagation();

        const row = e.target.closest('tr');
        const nextRow = row.nextElementSibling;

        if (nextRow && nextRow.classList.contains('expanded-row')) {
            nextRow.remove();
        } else {
            this.renderExpandedRow(AppState.collegesData[index], row);
        }
    },

    renderExpandedRow(college, insertAfter) {
        const template = document.getElementById('expandedRowTemplate');
        const expandedRow = template.content.cloneNode(true);

        // Populate round data
        if (college.rounds && college.rounds.length > 0) {
            const roundBody = expandedRow.querySelector('#roundTableBody');
            college.rounds.forEach((round, idx) => {
                const tr = document.createElement('tr');
                const nextRound = college.rounds[idx + 1];
                const trend = nextRound ? (nextRound.closing_rank > round.closing_rank ? '↑' : nextRound.closing_rank < round.closing_rank ? '↓' : '→') : '→';

                tr.innerHTML = `
                    <td>${round.round}</td>
                    <td>${round.opening_rank.toLocaleString()}</td>
                    <td>${round.closing_rank.toLocaleString()}</td>
                    <td><span class="trend-icon">${trend}</span></td>
                `;
                roundBody.appendChild(tr);
            });
        }

        // Populate institute info
        expandedRow.querySelector('#instituteLocation').textContent = college.location || 'N/A';
        expandedRow.querySelector('#instituteNIRF').textContent = college.nirf_rank || 'N/A';
        expandedRow.querySelector('#instituteEstablished').textContent = college.established || 'N/A';

        // Insert expanded row
        const tr = document.createElement('tr');
        tr.classList.add('expanded-row');
        tr.appendChild(expandedRow);
        insertAfter.insertAdjacentElement('afterend', tr);
    },
};

// ===== SHARE CONTROLLER =====
const ShareController = {
    generateShareURL() {
        const params = new URLSearchParams({
            score: AppState.formData.score,
            inputType: AppState.formData.inputType,
            year: AppState.formData.year,
            category: AppState.formData.category,
            seatPool: AppState.formData.seatPool,
            homeState: AppState.formData.homeState,
            branches: AppState.formData.branches.join(','),
        });
        return window.location.origin + window.location.pathname + '#' + params.toString();
    },

    shareResult() {
        const url = this.generateShareURL();
        if (navigator.share) {
            navigator.share({
                title: 'JEE Rank Prediction',
                text: 'Check my JEE rank prediction!',
                url: url,
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(url);
            alert('Link copied to clipboard!');
        }
    },

    loadFromURL() {
        const hash = window.location.hash.substring(1);
        if (!hash) return;

        const params = new URLSearchParams(hash);
        if (params.get('score')) {
            AppState.formData.score = parseFloat(params.get('score'));
            AppState.formData.inputType = params.get('inputType') || 'marks';
            AppState.formData.year = parseInt(params.get('year')) || 2024;
            AppState.formData.category = params.get('category') || 'GEN';
            AppState.formData.seatPool = params.get('seatPool') || 'GN';
            AppState.formData.homeState = params.get('homeState') || 'All India';
            const branches = params.get('branches');
            if (branches) {
                AppState.formData.branches = branches.split(',');
            }
        }
    },

    downloadPDF() {
        const element = document.getElementById('rankCard');
        const opt = {
            margin: 10,
            filename: `JEE_Prediction_${AppState.formData.score}_${AppState.formData.category}_${new Date().toLocaleDateString()}.pdf`,
            image: { type: 'png', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' },
        };
        html2pdf().set(opt).from(element).save();
    },
};

// ===== API CONTROLLER =====
const API = {
    async predictRank(payload) {
        try {
            const response = await fetch(`${API_BASE}/api/predict-rank`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!response.ok) throw new Error('API error');
            return await response.json();
        } catch (error) {
            console.error('predictRank error:', error);
            return null;
        }
    },

    async predictColleges(payload) {
        try {
            const response = await fetch(`${API_BASE}/api/predict-colleges`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!response.ok) throw new Error('API error');
            return await response.json();
        } catch (error) {
            console.error('predictColleges error:', error);
            return [];
        }
    },

    async estimateRank(score, inputType, year) {
        try {
            const response = await fetch(`${API_BASE}/api/estimate-rank?score=${score}&input_type=${inputType}&year=${year}`);
            if (!response.ok) return null;
            return await response.json();
        } catch (error) {
            console.error('estimateRank error:', error);
            return null;
        }
    },
};

// ===== LOADER =====
const Loader = {
    show(message = 'Loading...') {
        const overlay = document.getElementById('loaderOverlay');
        document.getElementById('loaderText').textContent = message;
        overlay.classList.add('show');
    },

    hide() {
        const overlay = document.getElementById('loaderOverlay');
        overlay.classList.remove('show');
    },
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    FormController.init();
    FormController.updateProgressBar();

    // Load from URL on page load (for shared links)
    ShareController.loadFromURL();
});
