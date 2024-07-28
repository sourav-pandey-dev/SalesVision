document.getElementById('generate-graphs').addEventListener('click', function () {
    const table = document.getElementById('sales-data');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    
    let products = [];
    let monthlyData = [];
    let totalUnitsSold = [];

    for (let row of rows) {
        let cells = row.getElementsByTagName('td');
        let product = cells[0].innerText;
        let monthly = [];
        for (let i = 1; i <= 12; i++) {
            monthly.push(parseInt(cells[i].innerText));
        }
        products.push(product);
        monthlyData.push(monthly);
        totalUnitsSold.push(parseInt(cells[13].innerText));
    }

    const months = ["Jan-16", "Feb-16", "Mar-16", "Apr-16", "May-16", "Jun-16", "Jul-16", "Aug-16", "Sep-16", "Oct-16", "Nov-16", "Dec-16"];
    
    new Chart(document.getElementById('unitsSoldChart'), {
        type: 'line',
        data: {
            labels: months,
            datasets: products.map((product, i) => ({
                label: product,
                data: monthlyData[i],
                borderColor: getRandomColor(),
                fill: false
            }))
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Units Sold Per Month'
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Month'
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

    new Chart(document.getElementById('totalUnitsSoldChart'), {
        type: 'bar',
        data: {
            labels: products,
            datasets: [{
                label: 'Total Units Sold',
                data: totalUnitsSold,
                backgroundColor: products.map(() => getRandomColor())
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Total Units Sold Per Product/Service'
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Product/Service'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Total Units Sold'
                    }
                }
            }
        }
    });
});

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
