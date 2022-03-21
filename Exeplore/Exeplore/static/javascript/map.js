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

    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    const markers = locations.map((position, i) => {
        const label = labels[i % labels.length];
        const marker = new google.maps.Marker({
            position,
            label,
        });

        marker.addListener("click", () =>{
            infoWin.setContent(label);
            infoWin.open(map, marker)
        });
        return marker;
    });

    new markerClusterer.MarkerClusterer({map, markers});
}

const locations=[
    {lat:50.7301170101061000,lng:-3.5383565018628900},
    {lat:50.7366487330100000,lng:-3.5315847865197300},
    {lat:50.7359321311997000,lng:-3.5298901558339000},
    {lat:50.7345784882646000,lng:-3.5253861865198100},
    {lat:50.7327868120471000,lng:-3.5387446460414500},
    {lat:50.7367816341360000,lng:-3.5405752539837200},
    {lat:50.7352010093475000,lng:-3.5297033172056600},
    {lat:50.7353092764875000,lng:-3.5343119172056300},

    {lat:50.7081815675764000,lng:-3.5145627055640000},
    {lat:50.7359622940061000,lng:-3.5352563441912200},
    {lat:50.7318715411691000,lng:-3.4555328000127400},
    {lat:50.7350145254719000,lng:-3.5341425576840500},
    {lat:50.7354553005249000,lng:-3.5335763029516000},
    {lat:50.7367625312911000,lng:-3.5351047730269300},
    {lat:50.7355434339421000,lng:-3.5344923576840400},
    {lat:50.7229577349012000,lng:-3.5164691797134300},

    {lat:50.7374907641183000,lng:-3.5324874386968900},
    {lat:50.7374907641183000,lng:-3.5324874386968900},
    {lat:50.7368357014819000,lng:-3.5355662576839900},
    {lat:50.7343927094060000,lng:-3.5267426858362900},
    {lat:50.7365161531500000,lng:-3.5371355441912100},
    {lat:50.7386444055044000,lng:-3.5310831055628200},
    {lat:50.7362317443094000,lng:-3.5336353153554800},
    {lat:50.7298986752142000,lng:-3.5430074441914600},

    {lat:50.7378236691039000,lng:-3.5317157135053000},
    {lat:50.7411723431120000,lng:-3.5446690460411500},
    {lat:50.7326300031845000,lng:-3.5379013441913400},
    {lat:50.7337674906160000,lng:-3.5277812269982600},
    {lat:50.7375276695759000,lng:-3.5334938730268900},
    {lat:50.7341530894979000,lng:-3.5251494595342100},
    {lat:50.7369416101351000,lng:-3.5346012288482600},
    {lat:50.7337175247897000,lng:-3.5346524135054600},

    {lat:50.7366882934601000,lng:-3.5357844116552100},
    {lat:50.6948672688725000,lng:-3.5006900010216400},
    {lat:50.7354088632732000,lng:-3.5350555595341800},
    {lat:50.7334414634020000,lng:-3.5340790306985400},
    {lat:50.7337778245536000,lng:-3.5267341018627700},
    {lat:50.1710711410228000,lng:-5.1238210748986600},
    {lat:50.7363050244582000,lng:-3.5360503460413300},
    {lat:50.7372423799792000,lng:-3.5360369441911800},

    {lat:50.7341324559981000,lng:-3.5350498153555600},
    {lat:50.7358837942223000,lng:-3.5381765306984300},
    {lat:50.7361598347821000,lng:-3.5383019595341500},
    {lat:50.7191654768761000,lng:-3.5094625883705400},
    {lat:50.7333266293869000,lng:-3.5352071288483800},
    {lat:50.7222397837978000,lng:-3.5159975541410200},
    {lat:50.7334657196695000,lng:-3.5363111748771700},
    {lat:50.7378061092579000,lng:-3.5369703539836800},

    {lat:50.7357715334461000,lng:-3.5307894135053800},
    {lat:50.7353602763323000,lng:-3.5324047595341800},
    {lat:50.7302777364584000,lng:-3.5386598306986300},
    {lat:50.2631454162705000,lng:-5.1006423307165100},
    {lat:50.6922821074384000,lng:-3.4739613018643300},
    {lat:50.7234266682295000,lng:-3.5154184558343700},
    {lat:50.7332476857700000,lng:-3.5365448883699900},
    {lat:50.7360392742651000,lng:-3.5299788595341500},
]; 

function handleLocationError(browserHasGeolocation, infoWin, pos){
    infoWin.setPosition(pos);
    infoWin.setContent(
        browserHasGeolocation
        ? "Error:  The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation"
    );
    infoWin.open(map);
}