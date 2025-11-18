document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Fetch Dashboard Data
    fetch('/api/dashboard-data')
    .then(response => response.json())
    .then(data => {
        // Update KPIs
        document.getElementById('kpi-customers').innerText = data.kpi.total_customers.toLocaleString();
        document.getElementById('kpi-balance').innerText = "£" + data.kpi.avg_balance.toLocaleString();

        // -- Chart 1: Cluster Distribution --
        const clusterLabels = data.clusters.map(c => `Group ${c.Cluster}`);
        const clusterCounts = data.clusters.map(c => c.Count);
        
        new Chart(document.getElementById('mainClusterChart'), {
            type: 'bar',
            data: {
                labels: clusterLabels,
                datasets: [{
                    label: 'Customers',
                    data: clusterCounts,
                    backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'],
                    borderRadius: 5
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });

        // -- Chart 2: Regions (Doughnut) --
        new Chart(document.getElementById('regionChart'), {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.region),
                datasets: [{
                    data: Object.values(data.region),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });

        // -- Chart 3: Job Classification (Horizontal Bar) --
        new Chart(document.getElementById('jobChart'), {
            type: 'bar',
            data: {
                labels: Object.keys(data.jobs),
                datasets: [{
                    label: 'Count',
                    data: Object.values(data.jobs),
                    backgroundColor: '#858796',
                    indexAxis: 'y'
                }]
            },
            options: {
                indexAxis: 'y',
                plugins: { legend: { display: false } }
            }
        });
    });

    // 2. Handle Predictions
    document.getElementById('predictForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            const resultBox = document.getElementById('result-box');
            const personaText = document.getElementById('persona-text');
            
            resultBox.classList.remove('d-none');
            if(result.error) {
                personaText.innerText = "Error";
                personaText.classList.replace('text-primary', 'text-danger');
            } else {
                personaText.innerText = result.persona;
                personaText.classList.add('text-primary');
            }
        });
    });
});