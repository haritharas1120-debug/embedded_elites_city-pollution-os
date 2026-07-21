// ===========================================
// SMART CITY GOVERNANCE DASHBOARD
// Part 1
// ===========================================

let aqiChart = null;
let pollutionChart = null;
let map = null;
let markers = [];

// ===========================================
// LOAD DATA FROM GOVERNANCE API
// ===========================================

async function loadData() {

    try {

        const response = await fetch("http://127.0.0.1:8000/governance");

        const data = await response.json();

        if (data.message) {

            alert(data.message);
            return;

        }

        //--------------------------------------
        // KPI CARDS
        //--------------------------------------

        document.getElementById("avgAQI").innerText =
            data.average_aqi;

        document.getElementById("highestAQI").innerText =
            data.highest_predicted_aqi;

        document.getElementById("improvement").innerText =
            data.improvement + "%";

        document.getElementById("confidence").innerText =
            data.confidence + "%";

        document.getElementById("riskZones").innerText =
            data.high_risk_zones;

        document.getElementById("targetZone").innerText =
            data.target_zone;

        document.getElementById("priority").innerText =
            data.priority;

        //--------------------------------------
        // ALERT BANNER
        //--------------------------------------

        document.getElementById("alert").innerHTML =
            "<b>" + data.alert + "</b>";

        const banner = document.getElementById("liveAlert");

        if (data.alert === "Red") {

            banner.innerHTML = "🔴 CRITICAL AIR QUALITY ALERT";
            banner.style.background = "#dc2626";

        }

        else if (data.alert === "Orange") {

            banner.innerHTML = "🟠 HIGH AIR POLLUTION";
            banner.style.background = "#ea580c";

        }

        else if (data.alert === "Yellow") {

            banner.innerHTML = "🟡 MODERATE AIR POLLUTION";
            banner.style.background = "#ca8a04";

        }

        else {

            banner.innerHTML = "🟢 AIR QUALITY NORMAL";
            banner.style.background = "#16a34a";

        }

        //--------------------------------------
        // AQI TABLE
        //--------------------------------------

        let table = "";

        data.zones.forEach(zone => {

            let cls = "moderate";

            if (zone.risk_level === "High")
                cls = "poor";

            if (zone.risk_level === "Very High")
                cls = "verypoor";

            table += `

            <tr>

                <td>${zone.sub_zone_id}</td>

                <td>${zone.baseline_aqi}</td>

                <td>${zone.predicted_aqi}</td>

                <td class="${cls}">
                    ${zone.risk_level}
                </td>

            </tr>

            `;

        });

        document.getElementById("aqiTable").innerHTML = table;

        //--------------------------------------
        // DEPARTMENTS
        //--------------------------------------

        let dept = "";

        data.departments.forEach(item => {

            dept += `<li>${item}</li>`;

        });

        document.getElementById("departments").innerHTML = dept;

        //--------------------------------------
        // INSPECTION
        //--------------------------------------

        document.getElementById("inspection").innerText =
            data.inspection_schedule;

        //--------------------------------------
        // GOVERNANCE DECISION
        //--------------------------------------

        document.getElementById("decision").innerHTML =

            "<b>Target Zone:</b> " +

            data.target_zone +

            "<br><br><b>Priority:</b> " +

            data.priority +

            "<br><br><b>Highest AQI:</b> " +

            data.highest_predicted_aqi +

            "<br><br><b>Departments:</b> " +

            data.departments.join(", ") +

            "<br><br><b>Inspection:</b> " +

            data.inspection_schedule +

            "<br><br><b>Recommendation:</b> Immediate intervention and continuous AQI monitoring.";

        //--------------------------------------
        // DAILY REPORT
        //--------------------------------------

        document.getElementById("report").innerHTML =

            "Average AQI improved by <b>" +

            data.improvement +

            "%</b> after implementing optimized traffic policies. " +

            "Highest pollution detected in <b>" +

            data.target_zone +

            "</b>. " +

            "Priority Level: <b>" +

            data.priority +

            "</b>.";

        //--------------------------------------
        // NEXT FUNCTIONS
        //--------------------------------------

        createAQIChart(data);

        createPollutionChart(data);

        updateMap(data);

        updateInspectionQueue(data);

    }

    catch(error){

        console.log(error);

        alert("Cannot connect to Governance Backend.");

    }

}
// ===========================================
// AQI COMPARISON CHART
// ===========================================

function createAQIChart(data){

    const ctx = document.getElementById("aqiChart");

    if(aqiChart){
        aqiChart.destroy();
    }

    aqiChart = new Chart(ctx,{

        type:"bar",

        data:{

            labels:["Average AQI","Highest AQI"],

            datasets:[{

                label:"AQI",

                data:[
                    data.average_aqi,
                    data.highest_predicted_aqi
                ]

            }]

        },

        options:{

            responsive:true,

            plugins:{
                legend:{
                    display:false
                }
            }

        }

    });

}


// ===========================================
// POLLUTION LEVEL CHART
// ===========================================

function createPollutionChart(data){

    const ctx = document.getElementById("pollutionChart");

    if(pollutionChart){
        pollutionChart.destroy();
    }

    let labels=[];
    let values=[];

    data.zones.forEach(zone=>{

        labels.push(zone.sub_zone_id);

        values.push(zone.predicted_aqi);

    });

    pollutionChart=new Chart(ctx,{

        type:"line",

        data:{

            labels:labels,

            datasets:[{

                label:"Predicted AQI",

                data:values,

                fill:false

            }]

        },

        options:{

            responsive:true

        }

    });

}



// ===========================================
// LEAFLET MAP
// ===========================================

function updateMap(data){

    if(!map){

        map=L.map("map").setView([13.05,80.25],11);

        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution:"© OpenStreetMap"
            }
        ).addTo(map);

    }

    markers.forEach(marker=>{

        map.removeLayer(marker);

    });

    markers=[];

    data.zones.forEach(zone=>{

        let color="green";

        if(zone.risk_level==="Poor")
            color="orange";

        if(zone.risk_level==="Very Poor")
            color="red";

        const icon=L.divIcon({

            html:`<div style="
            background:${color};
            width:18px;
            height:18px;
            border-radius:50%;
            border:2px solid white;
            "></div>`,

            className:""

        });

        const marker=L.marker(

            [zone.lat,zone.lng],

            {icon:icon}

        ).addTo(map);

        marker.bindPopup(

            "<b>"+zone.sub_zone_id+"</b><br>" +

            "Baseline AQI : "+zone.baseline_aqi+"<br>"+

            "Predicted AQI : "+zone.predicted_aqi+"<br>"+

            "Risk : "+zone.risk_level

        );

        markers.push(marker);

    });

}



// ===========================================
// INSPECTION QUEUE
// ===========================================


function updateInspectionQueue(data){

    let html="";

    data.zones.forEach(zone=>{

        let priority="Low";

        let status="Scheduled";

        // --- UPDATED: Changed "Very Poor" to "Very High" ---
        if(zone.risk_level==="Very High"){

            priority="Critical";

            status="Immediate";

        }

        // --- UPDATED: Changed "Poor" to "High" ---
        else if(zone.risk_level==="High"){

            priority="High";

            status="Within 24 Hours";

        }

        // This is the fallback that was incorrectly triggering before
        else{

            priority="Normal";

            status="Monitoring";

        }

        html+=`

        <tr>

            <td>${zone.sub_zone_id}</td>

            <td>${zone.risk_level}</td>

            <td>${priority}</td>

            <td>${status}</td>

        </tr>

        `;

    });

    document.getElementById("inspectionTable").innerHTML=html;

}


// ===========================================
// AUTO REFRESH
// ===========================================

loadData();

setInterval(loadData,5000);