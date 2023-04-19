function closeSide() {
    document.getElementById('side-bar').style.height = '40px';
    document.getElementById('close-icon').style.display = 'none';
}

function closeSideRight(){
    document.getElementById('side-bar-right').style.display = 'none';
}


function openWeather(evt, weatherStat) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(weatherStat).style.display = "block";
    evt.currentTarget.className += " active";
}

function openChart(evt, availabilityStat) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("average-chart");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("charttablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(availabilityStat).style.display = "flex";
    evt.currentTarget.className += " active";
}

function weatherUrl(lat,lng){
    var weatherUrl = "https://api.open-meteo.com/v1/forecast?latitude="+lat+
    "&longitude="+lng+
    "&hourly=temperature_2m,precipitation_probability,weathercode,windspeed_10m"+
    "&daily=weathercode,temperature_2m_max,temperature_2m_min"+
    "&current_weather=true&timeformat=unixtime&timezone=Europe/London";
    return weatherUrl;
}
// Make a request to the Open Meteo API to get the weather
function currentWeather(lat,lng){
    // Extract the current weather from the JSON object
    fetch(weatherUrl(lat,lng))
    .then(response => response.json())
    .then(data => data.current_weather) 
    .then(data => {
        //User weather code to show the corresponding image
        var weatherCode = data.weathercode;
        console.log("Weather Code: " + weatherCode);
        var weatherCodeOut ='<img src="../static/weather/' + weatherCode + '.png" height="30">';
        document.getElementById('weather-icon').innerHTML = weatherCodeOut;

        //Show weather text (temperature, windspeed)
        var temperature = data.temperature;
        var windSpeed = data.windspeed;
        console.log("Temperature: " + temperature);
        var weatherTextOut = '<p>Temperature: '+temperature+'&#8451;</p>'+
                            '<p>Windspeed: '+windSpeed+' km/h</p>';
        document.getElementById('weather-text').innerHTML = weatherTextOut;
    }); 
}

// Draw chart of Temperature, Precipitation, And Windspeed
function drawTemperature(lat,lng) {
    // const data = await getWeather();
    fetch(weatherUrl(lat,lng))
    .then(response => response.json())
    .then(data => data.hourly) 
    .then(data => {
        // Get times from API
        var times = data.time;

        // Get temperature, precipitation, and windspeed
        var temperatures = data.temperature_2m;
        var precipitations = data.precipitation_probability;
        var windspeeds = data.windspeed_10m;

        // Headings for data to pass into google chart
        var tempChartData = [['Time','Temperature']];
        var preciChartData = [['Time','Precipitation']];
        var windChartData = [['Time','Wind Speed']];
        
        // Only show future data
        for(var i = 0; i < times.length; i++){
            if(times[i] >= Math.floor(Date.now() / 1000)){
                const timeToDate = new Date(times[i] * 1000); // convert Unix timestamp to milliseconds and create Date object
                // Add temperature to the temperature data array
                var tempdatapoint = [timeToDate,temperatures[i]];
                tempChartData.push(tempdatapoint);
                // Add precipitation to the precipitations data array
                var precidatapoint = [timeToDate,precipitations[i]];
                preciChartData.push(precidatapoint);
                // Add windspeed to the windspeed data array
                var winddatapoint = [timeToDate,windspeeds[i]];
                windChartData.push(winddatapoint);
            }
        }

        // Create google data tables from 3 data arrays
        var tempData = google.visualization.arrayToDataTable(tempChartData);
        var preciData = google.visualization.arrayToDataTable(preciChartData);
        var windData = google.visualization.arrayToDataTable(windChartData);

        // Format the charts
        var options = {
            chartArea: {
                width: '85%'
            },
            hAxis: {
                viewWindow: {
                    min: new Date(Date.now()),
                    max: new Date(Date.now()+24*60*60*1000)
                },
                gridlines: {
                    count: -1,
                    units: {
                        days: {format: ['MMM dd']},
                        hours: {format: ['HH:mm', 'ha']},
                        },
                    color: '#fff'
                },
                baselineColor:'#fff'
            },
            vAxis: {
                minValue: 0,
                gridlines: {
                    color: '#fff'
                },
            },
            width:350,
            height:150,
            legend: 'none',
            series: {
                0: { color: '#FF4500' }
            }
        };

        // Draw the charts
        var tempChart = new google.visualization.AreaChart(document.getElementById('temperature-chart'));
        tempChart.draw(tempData, options);

        var preciChart = new google.visualization.ColumnChart(document.getElementById('precipitation-chart'));
        preciChart.draw(preciData, options);

        var windChart = new google.visualization.LineChart(document.getElementById('wind-chart'));
        windChart.draw(windData, options);
    });                         
} 

// Draw daily average chart of availability
function drawDaily(station){
    url = "/daily/"+station;
    let loader = `<div class="load-chart"><div class="spinner"></div></div>`;
    document.getElementById('daily-average').innerHTML = loader;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        var dayAverageData = [['Day of week', 'Average available bikes', 'Average free stands']];
        for (var i = 0; i < data.length; i++){
            var datapoint = [data[i]['day_name'],data[i]['avg_bikes'],data[i]['avg_stands']];
            dayAverageData.push(datapoint);
        }
        console.log(dayAverageData);                        
        var dayData = google.visualization.arrayToDataTable(dayAverageData);

        var options = {
            chartArea: {
                width: '85%'
            },
            width: 350,
            height: 200,
            seriesType: 'bars',
            legend: {
                position: 'top', 
                maxLines: 2,
                textStyle: {fontSize: 9}},
            series: {
                0: { color: '#003fff'},
                1: { color: '#00ffff' }        
            },
            vAxis: {
                minValue: 0,
                gridlines: {
                    color: '#fff'
                }
            },
        };

    var dayChart = new google.visualization.ComboChart(document.getElementById('daily-average'));
    dayChart.draw(dayData, options);
    })
}

// Draw daily average chart of availability
function drawHourly(station){
    url = "/hourly/"+station;
    let loader = `<div class="load-chart"><div class="spinner"></div></div>`;
    document.getElementById('hourly-average').innerHTML = loader;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        var hourAverageData = [['Hour', 'Average available bikes on '+data[0]['day_name'] +'s', 'Average free stands on ' + data[0]['day_name'] +'s']];
        for (var i = 0; i < data.length; i++){
            var datapoint = [data[i]['hour'],data[i]['avg_bikes'],data[i]['avg_stands']];
            hourAverageData.push(datapoint);
        }
        console.log(hourAverageData);                        
        var hourData = google.visualization.arrayToDataTable(hourAverageData);

        var options = {
            chartArea: {
                width: '85%'
            },
            isStacked: "true",
            width: 350,
            height: 200,
            seriesType: 'bars',
            legend: {
                position: 'top', 
                maxLines: 2, 
                textStyle: {fontSize: 9}},
            series: {
                0: { color: '#003fff'},
                1: { color: '#00ffff' }        
            },
            vAxis: {
                minValue: 0,
                gridlines: {
                    color: 'transparent'
                }

            },
            hAxis:{
                baselineColor: 'transparent',
                title: 'Hour of day'
            }
        };

    var hourChart = new google.visualization.ComboChart(document.getElementById('hourly-average'));
    hourChart.draw(hourData, options);
    })
}
