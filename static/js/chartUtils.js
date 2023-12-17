// chartUtils.js
function drawChartWithCsvData(canvas, labels, data) {
    const chartData = {
        labels: labels,
        datasets: [{
            label: 'Dataset from CSV',
            backgroundColor: 'rgba(99, 102, 241, 0.5)',
            borderColor: 'rgb(99, 102, 241)',
            data: data,
            fill: false,
            pointRadius: 5,
            pointHoverRadius: 8,
            showLine: true
        }]
    };

    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',  // X축을 시간으로 설정
                    time: {
                        unit: 'hour',  // 시간 단위를 시간으로 설정
                        displayFormats: {
                            hour: 'YYYY-MM-DD HH:mm:ss'  // 툴팁에 표시되는 시간 형식
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const ctx = canvas.getContext('2d');
    new Chart(ctx, config);
}
