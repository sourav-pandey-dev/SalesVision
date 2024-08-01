document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/products')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('product-select');
            data.products.forEach(product => {
                const option = document.createElement('option');
                option.value = product;
                option.textContent = product;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
});

document.getElementById('generate-graphs').addEventListener('click', function () {
    const product = document.getElementById('product-select').value;

    fetch('http://127.0.0.1:5000/forecast', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product: product })
    })
    .then(response => response.json())
    .then(data => {
        updateChart(data.past_sales, data.forecast_mean, data.forecast_conf_int);
    })
    .catch(error => console.error('Error:', error));
});

function updateChart(pastSales, forecastMean, forecastConfInt) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    const labels = pastSales.map(item => item.date).concat(forecastMean.map(item => item.date));
    const pastData = pastSales.map(item => item.sales);
    const forecastData = forecastMean.map(item => item.sales);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Past Sales',
                    data: pastData,
                    borderColor: 'blue',
                    fill: false
                },
                {
                    label: 'Forecast',
                    data: forecastData,
                    borderColor: 'red',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Sales Forecast'
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
