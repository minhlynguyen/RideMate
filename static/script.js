function closeSide() {
    document.getElementById('side-bar').style.height = '40px';
    document.getElementById('close-icon').style.display = 'none';
}

map.addListener('mousemove', function (event) {
    var pixelOffset = map.getProjection().fromLatLngToPoint(event.latLng);
    pixelOffset.x += 10;
    pixelOffset.y -= 10;
    var newLatLng = map.getProjection().fromPointToLatLng(pixelOffset);
    hoverInfo.setPosition(newLatLng);
});

