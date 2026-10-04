// =====================================================
// TRAFFIC GRAPH
// =====================================================

const ctx =
    document
        .getElementById("trafficChart")
        .getContext("2d");


const trafficChart = new Chart(ctx, {

    type: "line",

    data: {

        labels: [],

        datasets: [{

            label: "Vehicles",

            data: [],

            tension: 0.4,

            fill: true

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        animation: false,

        scales: {

            y: {

                beginAtZero: true,

                title: {

                    display: true,

                    text: "Vehicle Count"

                }

            },

            x: {

                title: {

                    display: true,

                    text: "Time"

                }

            }

        }

    }

});


// =====================================================
// UPDATE DASHBOARD
// =====================================================

async function updateTraffic() {

    try {

        const response =
            await fetch("/traffic");


        const data =
            await response.json();


        // Vehicle count

        document
            .getElementById("count")
            .innerText = data.count;


        // Traffic status

        document
            .getElementById("status")
            .innerText = data.status;


        // Green signal

        document
            .getElementById("green")
            .innerText =
                data.green + " sec";


        // Vehicle types

        document
            .getElementById("cars")
            .innerText = data.cars;


        document
            .getElementById("motorcycles")
            .innerText =
                data.motorcycles;


        document
            .getElementById("buses")
            .innerText = data.buses;


        document
            .getElementById("trucks")
            .innerText =
                data.trucks;


        // =================================================
        // SIMPLE AI PREDICTION
        // =================================================

        let prediction = "LOW";

        if (data.count >= 30) {

            prediction = "HIGH TRAFFIC EXPECTED";

        }

        else if (data.count >= 10) {

            prediction = "MODERATE TRAFFIC";

        }

        else {

            prediction = "LOW TRAFFIC";

        }


        document
            .getElementById("prediction")
            .innerText = prediction;


        // =================================================
        // UPDATE GRAPH
        // =================================================

        const currentTime =
            new Date().toLocaleTimeString();


        trafficChart.data.labels.push(
            currentTime
        );


        trafficChart.data.datasets[0]
            .data.push(data.count);


        // Keep only last 20 points

        if (
            trafficChart.data.labels.length > 20
        ) {

            trafficChart.data.labels.shift();

            trafficChart.data.datasets[0]
                .data.shift();

        }


        trafficChart.update();


    }

    catch (error) {

        console.error(
            "Error getting traffic data:",
            error
        );

    }

}


// =====================================================
// UPDATE EVERY SECOND
// =====================================================

setInterval(
    updateTraffic,
    1000
);


// Initial update

updateTraffic();