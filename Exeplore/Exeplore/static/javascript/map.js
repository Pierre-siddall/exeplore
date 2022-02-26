let map,infoWin,marker

function initialiseMap(){
    // Obtains a static map
    map=new google.maps.Map(document.getElementById("map"),{
        center:{lat:50.735,lng:-3.534},
        zoom:6,
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
                infoWin.setPosition(pos);
                infoWin.setContent("Location Found.");
                infoWin.open(map);
                map.setCenter(pos);
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
}

function handleLocationError(browserHasGeolocation, infoWin, pos){
    infoWin.setPosition(pos);
    infoWin.setContent(
        browserHasGeolocation
        ? "Error:  The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation"
    );
    infoWin.open(map);
}