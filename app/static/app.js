// TBM Advance Rate Calculator Frontend JavaScript

class TBMCalculator {
    constructor() {
        this.apiUrl = '/api/v1';
        this.examples = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupFormValidation();
        this.loadExamples();
    }

    bindEvents() {
        // Form submission
        document.getElementById('calculationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculateAdvanceRate();
        });

        // Example button
        document.getElementById('exampleBtn').addEventListener('click', () => {
            this.showExampleModal();
        });

        // Modal close
        document.getElementById('closeModal').addEventListener('click', () => {
            this.hideExampleModal();
        });

        // Soil type change handler
        document.getElementById('soil_type').addEventListener('change', (e) => {
            this.handleSoilTypeChange(e.target.value);
        });

        // Click outside modal to close
        document.getElementById('exampleModal').addEventListener('click', (e) => {
            if (e.target.id === 'exampleModal') {
                this.hideExampleModal();
            }
        });
    }

    setupFormValidation() {
        // Add real-time validation feedback
        const inputs = document.querySelectorAll('input[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateInput(input);
            });
        });
    }

    validateInput(input) {
        const isValid = input.checkValidity();
        if (isValid) {
            input.classList.remove('border-red-500');
            input.classList.add('border-green-500');
        } else {
            input.classList.remove('border-green-500');
            input.classList.add('border-red-500');
        }
    }

    handleSoilTypeChange(soilType) {
        const ucsField = document.getElementById('ucs_field');
        const rqdField = document.getElementById('rqd_field');
        const ucsInput = document.getElementById('ucs');
        const rqdInput = document.getElementById('rqd');

        if (soilType.includes('rock')) {
            ucsField.classList.remove('hidden');
            rqdField.classList.remove('hidden');
            ucsInput.required = true;
            rqdInput.required = true;
        } else {
            ucsField.classList.add('hidden');
            rqdField.classList.add('hidden');
            ucsInput.required = false;
            rqdInput.required = false;
            ucsInput.value = '';
            rqdInput.value = '';
        }
    }

    async loadExamples() {
        try {
            const response = await fetch(`${this.apiUrl}/examples`);
            const data = await response.json();
            this.examples = data.examples;
        } catch (error) {
            console.error('Failed to load examples:', error);
        }
    }

    showExampleModal() {
        const modal = document.getElementById('exampleModal');
        const exampleList = document.getElementById('exampleList');
        
        exampleList.innerHTML = '';
        
        this.examples.forEach((example, index) => {
            const exampleDiv = document.createElement('div');
            exampleDiv.className = 'border border-gray-200 rounded-lg p-4 cursor-pointer hover:bg-gray-50 transition duration-200';
            exampleDiv.innerHTML = `
                <h4 class="font-medium text-gray-800">${example.name}</h4>
                <p class="text-sm text-gray-600 mt-1">${example.description}</p>
                <div class="text-xs text-gray-500 mt-2">
                    <span class="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded mr-2">
                        ${example.parameters.tbm_diameter}m TBM
                    </span>
                    <span class="inline-block bg-green-100 text-green-800 px-2 py-1 rounded mr-2">
                        ${example.parameters.tbm_type.toUpperCase()}
                    </span>
                    <span class="inline-block bg-purple-100 text-purple-800 px-2 py-1 rounded">
                        ${example.parameters.soil_type.replace('_', ' ')}
                    </span>
                </div>
            `;
            
            exampleDiv.addEventListener('click', () => {
                this.loadExample(example.parameters);
                this.hideExampleModal();
            });
            
            exampleList.appendChild(exampleDiv);
        });
        
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    hideExampleModal() {
        const modal = document.getElementById('exampleModal');
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }

    loadExample(parameters) {
        // Fill form with example parameters
        Object.keys(parameters).forEach(key => {
            const input = document.getElementById(key);
            if (input) {
                input.value = parameters[key];
                if (key === 'soil_type') {
                    this.handleSoilTypeChange(parameters[key]);
                }
            }
        });
    }

    async calculateAdvanceRate() {
        this.showLoading();
        
        try {
            const formData = this.getFormData();
            
            const response = await fetch(`${this.apiUrl}/calculate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Calculation failed');
            }

            const result = await response.json();
            this.displayResults(result);
            
        } catch (error) {
            console.error('Calculation error:', error);
            this.showError(error.message);
        }
    }

    getFormData() {
        const formData = {};
        const form = document.getElementById('calculationForm');
        const formDataObj = new FormData(form);
        
        for (let [key, value] of formDataObj.entries()) {
            // Convert numeric fields
            if (['tbm_diameter', 'cutterhead_power', 'cutterhead_speed', 'thrust_force', 
                 'chamber_pressure', 'depth', 'water_pressure', 'temperature', 'ucs', 'rqd'].includes(key)) {
                formData[key] = value ? parseFloat(value) : null;
            } else {
                formData[key] = value;
            }
        }
        
        // Remove null values for optional fields
        Object.keys(formData).forEach(key => {
            if (formData[key] === null || formData[key] === '') {
                delete formData[key];
            }
        });
        
        return formData;
    }

    showLoading() {
        document.getElementById('loadingState').classList.remove('hidden');
        document.getElementById('resultsContainer').classList.add('hidden');
        document.getElementById('errorState').classList.add('hidden');
        
        // Disable calculate button
        const btn = document.getElementById('calculateBtn');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Calculating...';
    }

    displayResults(result) {
        // Hide loading and error states
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('errorState').classList.add('hidden');
        document.getElementById('resultsContainer').classList.remove('hidden');
        
        // Update main metrics
        document.getElementById('advanceRate').textContent = result.advance_rate;
        document.getElementById('dailyAdvance').textContent = result.daily_advance;
        document.getElementById('penetrationRate').textContent = result.penetration_rate;
        document.getElementById('specificEnergy').textContent = result.specific_energy;
        document.getElementById('confidence').textContent = (result.confidence_score * 100).toFixed(0) + '%';
        
        // Update risk assessment
        this.displayRiskAssessment(result.risk_factors);
        
        // Update recommendations
        this.displayRecommendations(result.risk_factors.recommendations);
        
        // Re-enable calculate button
        const btn = document.getElementById('calculateBtn');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-calculator mr-2"></i>Calculate Advance Rate';
    }

    displayRiskAssessment(riskFactors) {
        const riskContainer = document.getElementById('riskAssessment');
        const riskContent = document.getElementById('riskContent');
        
        const riskLevel = riskFactors.overall_risk_level;
        const risks = riskFactors.risks;
        
        // Set risk level styling
        riskContainer.className = `p-4 rounded-lg risk-${riskLevel}`;
        
        let riskHtml = `
            <div class="flex items-center justify-between mb-2">
                <span class="font-medium capitalize">${riskLevel} Risk Level</span>
                <span class="text-sm">
                    ${this.getRiskIcon(riskLevel)}
                </span>
            </div>
        `;
        
        if (Object.keys(risks).length > 0) {
            riskHtml += '<div class="space-y-2">';
            Object.values(risks).forEach(risk => {
                riskHtml += `
                    <div class="text-sm">
                        <span class="font-medium">${risk.level.toUpperCase()}:</span>
                        ${risk.description}
                    </div>
                `;
            });
            riskHtml += '</div>';
        } else {
            riskHtml += '<div class="text-sm">No significant risk factors identified.</div>';
        }
        
        riskContent.innerHTML = riskHtml;
    }

    displayRecommendations(recommendations) {
        const recommendationsList = document.getElementById('recommendationsList');
        
        if (recommendations.length > 0) {
            let html = '<ul class="space-y-1 text-sm">';
            recommendations.forEach(rec => {
                html += `<li class="flex items-start"><i class="fas fa-check-circle text-blue-600 mr-2 mt-0.5"></i>${rec}</li>`;
            });
            html += '</ul>';
            recommendationsList.innerHTML = html;
        } else {
            recommendationsList.innerHTML = '<p class="text-sm">No specific recommendations at this time.</p>';
        }
    }

    getRiskIcon(riskLevel) {
        switch (riskLevel) {
            case 'low':
                return '<i class="fas fa-check-circle text-green-600"></i>';
            case 'medium':
                return '<i class="fas fa-exclamation-triangle text-yellow-600"></i>';
            case 'high':
                return '<i class="fas fa-exclamation-circle text-red-600"></i>';
            default:
                return '<i class="fas fa-question-circle text-gray-600"></i>';
        }
    }

    showError(message) {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultsContainer').classList.add('hidden');
        document.getElementById('errorState').classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
        
        // Re-enable calculate button
        const btn = document.getElementById('calculateBtn');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-calculator mr-2"></i>Calculate Advance Rate';
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TBMCalculator();
});