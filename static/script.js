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

function calculateWeeklyAverage_bikes(data) {
    const weeklyData = [[0, 0, 0, 0, 0, 0, 0]];
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    let currentWeek = weeklyData[0];
    let count = 0;
    let dayIndex = 0;

    for (let i = 0; i < data.length; i++) {
        const [dateString, availability] = data[i];
        const date = new Date(dateString);
        const dayOfWeek = daysOfWeek[date.getDay()];

        if (dayOfWeek === 'Sun' && count > 0) {
            currentWeek[dayIndex] /= count;
            currentWeek = [0, 0, 0, 0, 0, 0, 0];
            weeklyData.push(currentWeek);
            count = 0;
            dayIndex = 0;
        }

        currentWeek[dayIndex] += availability[0];
        count++;
        dayIndex++;
        dayIndex %= 7;
    }

    if (count > 0) {
        currentWeek[dayIndex] /= count;
    }

    return weeklyData.slice(1);
}

function calculateWeeklyAverage_bike_stands(data) {
    const weeklyData = [[0, 0, 0, 0, 0, 0, 0]];
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    let currentWeek = weeklyData[0];
    let count = 0;
    let dayIndex = 0;

    for (let i = 0; i < data.length; i++) {
        const [dateString, availability] = data[i];
        const date = new Date(dateString);
        const dayOfWeek = daysOfWeek[date.getDay()];

        if (dayOfWeek === 'Sun' && count > 0) {
            currentWeek[dayIndex] /= count;
            currentWeek = [0, 0, 0, 0, 0, 0, 0];
            weeklyData.push(currentWeek);
            count = 0;
            dayIndex = 0;
        }

    currentWeek[dayIndex] += availability[1];
    count++;
    dayIndex++;
    dayIndex %= 7;
    }

    if (count > 0) {
        currentWeek[dayIndex] /= count;
    }

    

    return weeklyData.slice(1);
}
