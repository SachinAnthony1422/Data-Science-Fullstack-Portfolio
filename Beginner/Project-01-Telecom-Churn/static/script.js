// Circle configuration
const circle = document.querySelector('.progress-ring__circle');
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = circumference;

function setProgress(percent) {
    const offset = circumference - (percent / 100) * circumference;
    circle.style.strokeDashoffset = offset;
}

document.getElementById('churnForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // UI Transitions
    document.getElementById('initial-view').classList.add('d-none');
    document.getElementById('result-view').classList.add('d-none');
    document.getElementById('loading-view').classList.remove('d-none');

    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Hide loading
        document.getElementById('loading-view').classList.add('d-none');
        document.getElementById('result-view').classList.remove('d-none');

        // Parse probability
        let prob = parseFloat(result.probability);
        
        // Animate numbers
        document.getElementById('prob-text').innerText = prob + "%";
        
        // Animate Gauge
        setTimeout(() => setProgress(prob), 100); // Small delay for CSS animation

        // Update Badge & Colors
        const badge = document.getElementById('prediction-badge');
        const recText = document.getElementById('recommendation-text');
        
        if (result.prediction === "Yes") {
            // High Risk Styling
            circle.style.stroke = "#dc3545"; // Red
            badge.className = "badge bg-danger px-4 py-2 rounded-pill mb-3 fs-6";
            badge.innerText = "⚠️ High Churn Risk";
            
            // Smart Recommendations (Basic Logic)
            if (data.Contract === "Month-to-month") {
                recText.innerText = "User is on a monthly contract. Suggest upgrading to a 1-year plan with a 10% discount to improve retention.";
            } else if (data.TechSupport === "No") {
                recText.innerText = "User lacks Tech Support. Offer a free Tech Support trial to increase value perception.";
            } else {
                recText.innerText = "Customer is at high risk. Initiate a retention call immediately.";
            }

        } else {
            // Low Risk Styling
            circle.style.stroke = "#198754"; // Green
            badge.className = "badge bg-success px-4 py-2 rounded-pill mb-3 fs-6";
            badge.innerText = "✅ Low Churn Risk";
            recText.innerText = "Customer is stable. Consider cross-selling new services like Streaming TV or Device Protection.";
        }
    })
    .catch(error => {
        alert("Error connecting to server.");
        console.error(error);
        document.getElementById('loading-view').classList.add('d-none');
        document.getElementById('initial-view').classList.remove('d-none');
    });
});