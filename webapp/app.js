document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const autoFields = document.getElementById('auto-fields');
    const lifeFields = document.getElementById('life-fields');
    const riskForm = document.getElementById('risk-form');
    const resultSection = document.getElementById('result-section');
    const overallGauge = document.getElementById('overall-gauge');
    const overallScoreText = document.getElementById('overall-score');
    const riskFactorsList = document.getElementById('risk-factors');
    const premiumRangeText = document.getElementById('premium-range');
    const timestampText = document.getElementById('timestamp');
    const excalidrawLink = document.getElementById('excalidraw-link');
    const notionLink = document.getElementById('notion-link');

    const notionBtn = document.querySelector('.btn-pill');

    // Notion Button Feedback
    if (notionBtn) {
        notionBtn.addEventListener('click', () => {
            alert('Notion Connectivity: This feature is currently simulating a real MCP connection using your locally stored .actuary-config.json.');
        });
    }

    let currentMode = 'auto';

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            currentMode = btn.dataset.type;
            if (currentMode === 'auto') {
                autoFields.classList.remove('hidden');
                lifeFields.classList.add('hidden');
            } else {
                autoFields.classList.add('hidden');
                lifeFields.classList.remove('hidden');
            }
        });
    });

    // Risk Calculation Simulation
    riskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const age = parseInt(document.getElementById('age').value);
        const data = {
            age: age,
            location: document.getElementById('location').value,
            vehicle: document.getElementById('vehicle').value,
            sex: document.getElementById('sex').value,
            smoker: document.getElementById('smoker').checked
        };

        calculateRisk(data);
    });

    function calculateRisk(data) {
        // Mock calculation logic inspired by the Python backend
        let baseScore = 30;
        let factors = [];
        let premiumLow = 1200;
        let premiumHigh = 1600;

        if (currentMode === 'auto') {
            // Auto specific
            if (data.age < 25) {
                baseScore += 25;
                factors.push("Young driver risk multiplier");
            } else if (data.age > 65) {
                baseScore += 15;
                factors.push("Senior visibility risk factor");
            } else {
                baseScore += 5;
                factors.push("Stable age bracket discount applied");
            }

            if (data.vehicle === 'suv' || data.vehicle === 'truck') {
                baseScore += 12;
                factors.push(`${data.vehicle.toUpperCase()} rollover risk premium`);
                premiumLow += 400;
                premiumHigh += 600;
            }

            factors.push(`${data.location || 'Regional'} safety modifiers applied`);
        } else {
            // Life specific
            if (data.age > 50) {
                baseScore += 30;
                factors.push("Age-related mortality increase");
            } else {
                baseScore += 10;
                factors.push("Young adult health baseline");
            }

            if (data.smoker) {
                baseScore *= 1.6;
                factors.push("Smoker status 1.6x multiplier (CDC)");
                premiumLow *= 2.5;
                premiumHigh *= 3.0;
            }

            if (data.sex === 'male') {
                baseScore += 8;
                factors.push("Statistical male mortality adjustment");
            }
            
            premiumLow = Math.round(premiumLow / 12);
            premiumHigh = Math.round(premiumHigh / 12);
        }

        const finalScore = Math.min(Math.round(baseScore), 100);
        showResults(finalScore, factors, premiumLow, premiumHigh);
    }

    function showResults(score, factors, low, high) {
        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });

        // Update Gauge
        // 283 is the circumference for r=45
        const offset = 283 - (283 * score / 100);
        overallGauge.style.strokeDashoffset = offset;
        
        // Color coding
        if (score < 40) overallGauge.style.stroke = "#10b981";
        else if (score < 75) overallGauge.style.stroke = "#f59e0b";
        else overallGauge.style.stroke = "#ef4444";

        // Animating the score text
        let startScore = 0;
        const interval = setInterval(() => {
            if (startScore >= score) {
                clearInterval(interval);
            } else {
                startScore++;
                overallScoreText.innerText = startScore;
            }
        }, 20);

        // Update list
        riskFactorsList.innerHTML = "";
        factors.forEach(f => {
            const li = document.createElement('li');
            li.innerText = f;
            riskFactorsList.appendChild(li);
        });

        // Update Premium
        const currency = currentMode === 'life' ? '/ Month' : '/ Year';
        premiumRangeText.innerText = `$${low} - $${high}`;
        document.querySelector('.currency').innerText = `CAD ${currency}`;

        // Timestamp
        timestampText.innerText = `Report generated: ${new Date().toLocaleString()}`;

        // Mock Links
        const randomId = Math.floor(Math.random() * 1000000);
        excalidrawLink.href = `https://excalidraw.com/#json=${randomId},mockKey123`;
        notionLink.href = `https://notion.so/Actuary-Report-${randomId}`;
    }
});
