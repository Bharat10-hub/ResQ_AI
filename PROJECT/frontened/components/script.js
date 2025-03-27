fetch("http://localhost:5000/classify", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: "Help me!" })
})
.then(response => response.json())
.then(data => console.log("Prediction response:", data))
.catch(error => console.error("Error:", error));

const nameId = document.getElementById("nameTag");
const goTo = document.getElementById("goToMap");
const homeButton = document.getElementById("home");
const map = L.map('map').setView([20.5937, 78.9629], 5);
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("map").style.display = "none";  // Hide map initially
    homeButton.style.display = "none";  // Hide home button initially
    nameId.style.display = "block";  // Show nameTag
    goTo.style.display = "block";  // Show goTo button
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const citiesDatabase = {
    "delhi": { lat: 28.6139, lon: 77.2090 },
    "mumbai": { lat: 19.0760, lon: 72.8777 },
    "bangalore": { lat: 12.9716, lon: 77.5946 },
    "kolkata": { lat: 22.5726, lon: 88.3639 },
    "chennai": { lat: 13.0827, lon: 80.2707 },
    "hyderabad": { lat: 17.3850, lon: 78.4867 },
    "ahmedabad": { lat: 23.0225, lon: 72.5714 },
    "pune": { lat: 18.5204, lon: 73.8567 },
    "jaipur": { lat: 26.9124, lon: 75.7873 },
    "lucknow": { lat: 26.8467, lon: 80.9462 }
};

function submitMessage() {
    const text = document.getElementById("message").value.toLowerCase().trim();
    if (!text) return alert("Please enter a message.");

    showLoading();

    fetch("http://localhost:5000/classify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();

        let isSOS = data.prediction === 1;
        let isSafe = data.prediction === 0;

        document.getElementById("input-section").style.display = "none";
        document.getElementById("map").style.display = "block";

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const { latitude, longitude } = position.coords;
                addMarker(latitude, longitude, text, isSOS, isSafe);

                if (isSOS) {
                    sendSOSAlert(text, latitude, longitude);
                }
            }, (error) => {
                console.error("Geolocation error:", error);
            }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 });
        } else {
            alert("Geolocation is not supported by your browser.");
        }

        nameId.style.display = "none";
        goTo.style.display = "none";
        homeButton.style.display = "block";
    })
    .catch(error => {
        console.error("Error:", error);
        hideLoading();
        alert("Error processing your message.");
    });
}

function sendSOSAlert(message, lat, lon) {
    fetch("http://localhost:5000/send_sos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: `SOS ALERT! ${message} Location: (${lat}, ${lon})`,
            recipient: "+9198XXXXXXXX"  // Change this to actual recipient number
        })
    })
    .then(response => response.json())
    .then(data => console.log("SOS Sent:", data))
    .catch(error => console.error("Error sending SOS:", error));
}

function addMarker(lat, lon, message, isSOS, isSafe) {
    let markerColor = isSOS ? 'red' : isSafe ? 'green' : 'blue';

    let marker = L.circleMarker([lat, lon], {
        color: markerColor,
        radius: 8,
        fillOpacity: 1
    }).addTo(map);

    const statusMessage = isSOS ? "🚨 SOS ALERT" : isSafe ? "✅ Safe Status" : "📍 Location Marker";
    marker.bindPopup(`<b>${statusMessage}</b><br>${message}`).openPopup();

    map.flyTo([lat, lon], isSOS ? 16 : 14);

    if (isSOS) {
        blinkMarker(marker);
    }
}

function blinkMarker(marker) {
    let visible = true;
    const blinkInterval = setInterval(() => {
        visible = !visible;
        marker.setStyle({ fillOpacity: visible ? 1 : 0 });
    }, 500);

    setTimeout(() => clearInterval(blinkInterval), 20000);
}

function showLoading() {
    document.getElementById("loadingMessage").style.display = "block";
}

function hideLoading() {
    document.getElementById("loadingMessage").style.display = "none";
}

goTo.addEventListener('click', () => {
    document.getElementById("input-section").style.display = "none";
    document.getElementById("map").style.display = "block";
    nameId.style.display = "none";
    goTo.style.display = "none";
    homeButton.style.display = "block";
});

homeButton.addEventListener('click', () => {
    homeButton.style.display = "none";
    document.getElementById("map").style.display = "none";
    document.getElementById("input-section").style.display = "block";
    nameId.style.display = "block";
    goTo.style.display = "block";
});
