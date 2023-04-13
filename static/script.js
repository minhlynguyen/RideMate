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
    defaultButton = document.getElementById("default-button");
    if(defaultButton.style.border !== "none"){
        defaultButton.style.border = "none";
    }else{
        defaultButton.style.borderBottomStyle = "#33CCCC 2px solid";
    };
    document.getElementById(weatherStat).style.display = "block";
    evt.currentTarget.className += " active";
}