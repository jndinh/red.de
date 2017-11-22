class _mapControl
{
    constructor()
    {
        this.map=new google.maps.Map(document.querySelector(".map"),{
            center:{lat:38.682,lng:-77.344},
            zoom:8
        });

        this.direction=new google.maps.DirectionsService();

        this.menu=document.querySelector(".menu-bar");

        this.menuSet();
        this.mapButtons();
    }

    menuSet()
    {
        var expandMenuButton=this.menu.querySelector(".expand");
        this.menu.querySelector(".minimise").addEventListener("click",(e)=>{
            this.menu.classList.remove("expanded");
            this.menu.classList.add("hidden");
            this.menuShow.classList.remove("hidden");
            expandMenuButton.innerText="additional information";
        });

        this.menu.querySelector(".test1").addEventListener("click",(e)=>{
            this.loadGeoJsonTest();
        });

        this.menu.querySelector(".maximise").addEventListener("click",(e)=>{

        });

        expandMenuButton.addEventListener("click",(e)=>{
            if (!this.menu.classList.contains("expanded"))
            {
                this.menu.classList.add("expanded");
                expandMenuButton.innerText="minimise additional information";
            }

            else
            {
                this.menu.classList.remove("expanded");
                expandMenuButton.innerText="additional information";
            }
        });
    }

    mapButtons()
    {
        this.menuShow=document.createElement("div");
        this.menuShow.classList.add("menu-show","hidden");
        this.menuShow.innerHTML="▴";

        this.menuShow.addEventListener("click",(e)=>{
            this.menu.classList.remove("hidden");
            this.menuShow.classList.add("hidden");
        });

        this.map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(this.menuShow);
    }

    //draw a polyline from a coordinate to another, following
    //roads by using the direction api
    roadLineDrawtest()
    {
        this.direction.route({
            origin:{lng:-78,lat:39.137},
            destination:{lat:39.281,lng:-76.60},
            travelMode:google.maps.TravelMode.DRIVING
        },(r,s)=>{
            var pathPoints=r.routes[0].overview_path;
            var path=new google.maps.Polyline({
                path:pathPoints
            });

            path.setMap(this.map);
        });
    }

    //load geojson from a file and alternate colouring
    //between red and blue
    loadGeoJsonTest()
    {
        this.map.data.loadGeoJson("md-district.geojson");

        var mapcolorCount=1;

        this.map.data.setStyle((f)=>{
            var color="red";

            if (mapcolorCount%2)
            {
                color="blue";
            }

            mapcolorCount++;

            return {fillColor:color,strokeColor:color,strokeWeight:1};
        });

        var infowindow=new google.maps.InfoWindow({
            content:`<table class="info-table"><tbody><tr><td>sample</td><td>data</td></tr><tr><td>sample</td><td>data</td></tr><tr><td>sample</td><td>data</td></tr></tbody></table>`
        });

        this.map.data.addListener("click",(e)=>{
            // console.log(e.latLng.lat());
            // console.log(e.latLng.lng());

            infowindow.setPosition(e.latLng);
            infowindow.open(this.map);
        });
    }

    loadTracs()
    {
        var kml=new google.maps.KmlLayer({
            map:this.map,
            url:"https://raw.githubusercontent.com/khang4/wahlkreisstest/master/tracs/cb_2016_24_tract_500k.kml"
        });

        // var r=new XMLHttpRequest();

        // r.open("GET","tracs/cb_2016_24_tract_500k.kml");

        // r.responseType="document";
        // r.onreadystatechange=()=>{
        //     if (r.readyState==4)
        //     {
        //         var geodata=toGeoJSON.kml(r.response);
        //         console.log(geodata);
        //         this.map.data.addGeoJson(geodata);
        //     }
        // };

        // r.send();
    }
}