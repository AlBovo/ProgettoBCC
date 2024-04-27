async function getMorningAndAfternoonPercentages() {
    try {
        let csrftoken = document.getElementById('csrf_token');
        csrftoken = csrftoken === null ? "testingvalue" : csrftoken.value;
        const response = await fetch('/admin/stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        });

        if (!response.ok) {
            throw new Error('Errore nella richiesta');
        }

        const data = await response.json();

        return [parseFloat(data.morning), parseFloat(data.afternoon)];
    } catch (error) {
        console.error('Errore durante il recupero delle percentuali di mattina e pomeriggio:', error);
        return null;
    }
}


const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: true,
            text: 'EVENTS',
            font: {
                size: 18,
                weight: 'bold',
            },
            color: '#000'
        },
        legend: {
            position: 'top',
            padding: 20,
            labels: {
                font: {
                    size: 16,
                    weight: 'bold',
                },
                color: '#000'
            }
        }
    }
};

// Dati per il grafico a torta
const pieData = {
    labels: ['Morning', 'Afternoon'],
    datasets: [{
        data: getMorningAndAfternoonPercentages(),
        backgroundColor: ['#006F34', '#95BF74']
    }]
};

// Creazione del grafico a torta
document.addEventListener('DOMContentLoaded', function() {
const pieCtx = document.getElementById('PieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: pieData,
    options: pieOptions
})
});

// Imposta i grafici come responsivi e senza mantenere l'aspetto fisso
const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: true,
            text: 'EVENTS CATEGORY',
            font: {
                size: 18,
                weight: 'bold',
            },
            color: '#000'
        },
        legend: {
            position: 'top',
            labels: {
                font: {
                    size: 16,
                    weight: 'bold',
                },
                color: '#000'
            }
        }
    }
};

// Dati per il grafico a barre
const barData = {
    labels: ['April', 'May', 'June'],
    datasets: [{
        label: 'Consultancy',
        data: [10, 20, 30],
        backgroundColor: '#006F34',
    }, {
        label: 'Loan',
        data: [15, 25, 35],
        backgroundColor: '#95BF74',
    }]
};

// Creazione del grafico a barre
document.addEventListener('DOMContentLoaded', function() {
const barCtx = document.getElementById('LineChart').getContext('2d');
const barChart = new Chart(barCtx, {
    type: 'bar',
    data: barData,
    options: barOptions
})
});
