document.getElementById('attritionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const resultBox = document.getElementById('result-box');
    resultBox.innerHTML = `<div class="spinner-border text-primary" role="status"></div><p class="mt-2">Analyzing...</p>`;

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
        if (result.prediction === "Yes") {
            resultBox.innerHTML = `
                <div class="text-danger mb-3"><i class="fas fa-exclamation-triangle fa-4x"></i></div>
                <h3 class="text-danger fw-bold">High Risk</h3>
                <p class="lead">Attrition Probability: <strong>${result.probability}%</strong></p>
                <div class="alert alert-warning small text-start w-100">
                    <strong>Action Required:</strong> Schedule a 1-on-1 retention meeting. Review compensation and workload.
                </div>
            `;
        } else {
            resultBox.innerHTML = `
                <div class="text-success mb-3"><i class="fas fa-check-circle fa-4x"></i></div>
                <h3 class="text-success fw-bold">Stable</h3>
                <p class="lead">Attrition Probability: <strong>${result.probability}%</strong></p>
                <div class="alert alert-success small text-start w-100">
                    <strong>Status:</strong> Employee is likely to stay. Continue standard engagement programs.
                </div>
            `;
        }
    })
    .catch(error => {
        resultBox.innerHTML = `<p class="text-danger">Error connecting to model.</p>`;
        console.error(error);
    });
});