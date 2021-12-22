function initMap() {
    const uluru = { lat: -25.34, lng: 131.36 };
    const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: uluru,
});
const marker = new google.maps.Marker({
  position: uluru,
  map: map,
});

  }