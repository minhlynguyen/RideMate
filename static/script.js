function closeSide() {
    document.getElementById('side-bar').style.height = '40px';
    document.getElementById('close-icon').style.display = 'none';
}

<<<<<<< HEAD
map.addListener('mousemove', function (event) {
    var pixelOffset = map.getProjection().fromLatLngToPoint(event.latLng);
    pixelOffset.x += 10;
    pixelOffset.y -= 10;
    var newLatLng = map.getProjection().fromPointToLatLng(pixelOffset);
    hoverInfo.setPosition(newLatLng);
});

=======
function closeSideRight(){
    document.getElementById('side-bar-right').style.width = '0px';
}

//map.addListener('mousemove', function (event) {
//    var pixelOffset = map.getProjection().fromLatLngToPoint(event.latLng);
//    pixelOffset.x += 10;
//    pixelOffset.y -= 10;
//   var newLatLng = map.getProjection().fromPointToLatLng(pixelOffset);
//   hoverInfo.setPosition(newLatLng);
//});
>>>>>>> main
