document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/categories')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('product-select');
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching categories:', error));
});

document.getElementById('generate-graphs').addEventListener('click', function () {
    const category = document.getElementById('product-select').value;

    fetch('http://127.0.0.1:5000/forecast', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ category: category })
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('charts-container');
        container.innerHTML = ''; // Clear previous charts

        // Create a new canvas for the selected category
        const canvas = document.createElement('canvas');
        canvas.id = `chart-${category}`;
        container.appendChild(canvas);

        if (data.error) {
            updateChart([], [], [], canvas.id); // Call with empty arrays if there's an error
        } else {
            updateChart(data.past_sales, data.forecast_mean, data.forecast_conf_int, canvas.id);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const container = document.getElementById('charts-container');
        container.innerHTML = ''; // Clear previous charts

        // Create a new canvas for the selected category
        const canvas = document.createElement('canvas');
        canvas.id = `chart-${category}`;
        container.appendChild(canvas);

        updateChart([], [], [], canvas.id); // Call with empty arrays if there's an error
    });
});

function updateChart(pastSales, forecastMean, forecastConfInt, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const labels = pastSales.map(item => item.date).concat(forecastMean.map(item => item.date));
    const pastData = pastSales.map(item => item.sales);
    const forecastData = forecastMean.map(item => item.sales);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.length > 0 ? labels : ['No data'],
            datasets: [
                {
                    label: 'Past Sales',
                    data: pastData.length > 0 ? pastData : [0],
                    borderColor: 'blue',
                    fill: false
                },
                {
                    label: 'Forecast',
                    data: forecastData.length > 0 ? forecastData : [0],
                    borderColor: 'red',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: `Sales Forecast for ${canvasId.replace('chart-', '')}`
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Units Sold'
                    }
                }
            }
        }
    });
}
