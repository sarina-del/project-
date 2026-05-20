const API_BASE = ""; // Same Flask app. Use "http://127.0.0.1:5000" if frontend is hosted separately.

async function analyseInformation() {
    const text = document.getElementById("claimText").value;
    const resultBox = document.getElementById("misinformationResult");

    resultBox.innerHTML = `<h3>Analysis Result</h3><p class="empty-state">Analysing...</p>`;

    try {
        const response = await fetch(`${API_BASE}/api/check-misinformation`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();
        displayMisinformationResult(data);
    } catch (error) {
        // Fallback demo result if backend is not running
        const fallback = {
            score: 55,
            label: "Needs Verification",
            reasons: [
                "Demo mode: backend could not be reached.",
                "The claim should be checked against reliable sources."
            ],
            suggestions: [
                "Start the Flask backend using: python app.py",
                "Check trusted sources before sharing the information."
            ]
        };
        displayMisinformationResult(fallback);
    }
}

function displayMisinformationResult(data) {
    const resultBox = document.getElementById("misinformationResult");
    const statusClass = getStatusClass(data.label);

    resultBox.innerHTML = `
        <h3>Analysis Result</h3>
        <div class="score-box">
            <div class="score-number">${data.score}/100</div>
            <span class="status-label ${statusClass}">${data.label}</span>
        </div>
        <div class="result-section">
            <h4>Key Reasons</h4>
            <ul>${toList(data.reasons)}</ul>
        </div>
        <div class="result-section">
            <h4>Suggested Verification Steps</h4>
            <ul>${toList(data.suggestions)}</ul>
        </div>
    `;
}

async function summarisePolicy() {
    const policy = document.getElementById("policyText").value;
    const resultBox = document.getElementById("privacyResult");

    resultBox.innerHTML = `<h3>Policy Summary</h3><p class="empty-state">Summarising...</p>`;

    try {
        const response = await fetch(`${API_BASE}/api/summarise-policy`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ policy: policy })
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();
        displayPrivacyResult(data);
    } catch (error) {
        // Fallback demo result if backend is not running
        const fallback = {
            summary: "Demo mode: backend could not be reached. This is a sample simplified privacy summary.",
            data_collected: ["Name", "Email address", "Location data"],
            risks: ["Data may be shared with third-party services."],
            rights: ["User may request data deletion."],
            risk_level: "Medium Risk"
        };
        displayPrivacyResult(fallback);
    }
}

function displayPrivacyResult(data) {
    const resultBox = document.getElementById("privacyResult");
    const statusClass = getStatusClass(data.risk_level);

    resultBox.innerHTML = `
        <h3>Policy Summary</h3>
        <div class="score-box">
            <p>${data.summary}</p>
            <span class="status-label ${statusClass}">${data.risk_level}</span>
        </div>
        <div class="result-section">
            <h4>Data Collected</h4>
            <ul>${toList(data.data_collected)}</ul>
        </div>
        <div class="result-section">
            <h4>Possible Risks</h4>
            <ul>${toList(data.risks)}</ul>
        </div>
        <div class="result-section">
            <h4>User Rights</h4>
            <ul>${toList(data.rights)}</ul>
        </div>
    `;
}

function toList(items) {
    return items.map(item => `<li>${item}</li>`).join("");
}

function getStatusClass(label) {
    if (!label) return "";
    const lower = label.toLowerCase();

    if (lower.includes("high") || lower.includes("misleading")) {
        return "status-danger";
    }

    if (lower.includes("medium") || lower.includes("needs")) {
        return "status-warning";
    }

    return "";
}

async function fetchData() {
    try {
        const response = await fetch('/api/data'); // Points directly to api/index.py
        const data = await response.json();
        document.getElementById('output').innerText = data.message;
    } catch (error) {
        console.error("Failed to fetch:", error);
    }
}
fetchData();
