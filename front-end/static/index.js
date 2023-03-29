function addMarkers(stations) {
    for (const station of stations) {
    //console.log(station);
        var marker = new google.maps.Marker({
            position: {
            lat: station.position_lat,
            lng: station.position_lng,
            },
        map: map,
        title: station.name,
        station_number: station.number,
    });
    }
}

function getStations() {
    fetch("/stations")
    .then((response) => response.json())
    .then((data) => {
    console.log("fetch response", typeof data);
    addMarkers(data)
});
}

// Initialize and add the map
function initMap(){
    const dublin = {lat: 53.35014, lng: -6.266255};
    // The map, centered at Dublin
    map = new goole.maps.Map(document.getElementById("map"),{
        zoom:14,
        center:dublin,
    });
    getStations();
}

function getWeather(){
    fetch('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,precipitation_probability,weathercode,windspeed_10m&current_weather=true')
    .then(res => {
        return res.json();
    })
    .then(data => {
        data.forEach(cw => {
            const markup = `${cw.current_weather}`;
            document.querySelector('cw').insertAdjacentElement('beforeend',markup)
        });
    })
    .catch(error => console.log(error));
}
var map = null;
window.initMap = initMap;