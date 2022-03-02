import {MarkerClusterer} from "@googlemap/markerclusterer"

let map,infoWin

function initialiseMap(){
    // Obtains a static map
    map=new google.maps.Map(document.getElementById("map"),{
        center:{lat:50.735,lng:-3.534},
        zoom:15,
        styles:[
            {elementType:"geometry",stylers:[{color:"#242f3e"}]},
            {elementType: "labels.text.stroke",stylers:[{color: "#242f3e"}]},
            {elementType: "labels.text.fill",stylers: [{color: "#746855"}]},
            {
                featureType:"administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{color: "#d59563"}],
            },
            {
              featureType: "poi",
              elementType: "labels.text.fill",
              stylers: [{color: "#d59563"}]
            },
            {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{color: "#263c3f"}],
            },
            {
               featureType: "poi.park",
               elementType: "labels.text.fill",
               stylers: [{color: "#6b9a76"}]
            },
            {
                featureType: "road",
                elementType: "geometry",
                stylers: [{color: "#38414e"}],
            },
            {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{color: "#212a37"}]
            },
            {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{color: "#9ca5b3"}],
            },
            {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{color: "#746855"}],
            },
            {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{color: "#1f2835"}]
            },
            {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{color: "#f3d19c"}]
            },
            {
                featureType: "transit",
                elementType: "geometry",
                stylers: [{color: "#2f3948"}]
            },
            {
                featureType: "transit.station",
                elementType: "labels.text.fill",
                stylers: [{color: "#d59563"}]
            },
            {
                featureType: "water",
                elementType: "geometry",
                stylers: [{color: "#17263c"}]
            },
            {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{color: "#515c6d"}],
            },
            {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{color: "#17263c"}]
            },
        ],
    });
    infoWin=new google.maps.InfoWindow();

    // Creating a button that shows the current location
    const currentLocation= document.createElement("button");
    currentLocation.textContent="Get current location";
    currentLocation.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(currentLocation);

    // Anon function that finds the location
    currentLocation.addEventListener("click",() =>{
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition((position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                const marker = new google.maps.Marker({
                  position: pos,
                      map: map,
                });
            },
                () => {
                handleLocationError(true,infoWin,map.getCenter());
            }
            );
        }else{
            // Browser does not
            handleLocationError(false,infoWin,map.getCenter());
        }
    });

    const markers= locations.map((position,i) => {
        const marker=new google.maps.Marker({
            position
        });
        marker.addListener("click",() =>{
            infoWin.open(map,marker);
        });
        return marker;
    });

    new MarkerClusterer({markers,map});
}

const locations=[];//add the locations from text file in here

function handleLocationError(browserHasGeolocation, infoWin, pos){
    infoWin.setPosition(pos);
    infoWin.setContent(
        browserHasGeolocation
        ? "Error:  The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation"
    );
    infoWin.open(map);
}