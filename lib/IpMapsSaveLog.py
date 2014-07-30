#coding=utf-8
__author__ = 'DM_'
def SaveLog(log):
    LogFilePath="IpMaps.html"
    LogFile = open(LogFilePath,'a')
    LogContent = """
    <html>
      <head>
        <style>
        body { font-family: Helvetica; }
        .map-content h3 { margin: 0; padding: 5px 0 0 0; }
        </style>
        <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=true"></script>
        <script>
        // Set the Map variable
            var map;
            function initialize() {
                var myOptions = {
                zoom: 5,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var MessAge="[%s]"
                       //使用eval解析,但是这个不安全，推荐JSON.parse解析,懒得下包了
                var all=eval(MessAge);
            var infoWindow = new google.maps.InfoWindow;
            map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
            // Set the center of the map
            var latitude=30.35;
            var longitude=114.17;
            var pos = new google.maps.LatLng(latitude, longitude);
            map.setCenter(pos);
            function infoCallback(infowindow, marker) {
                return function() {
                infowindow.open(map, marker);
            };
       }
       function setMarkers(map, all) {
        for (var i in all) {
                var ip 	    = all[i].Ip;
                var organization = all[i].organization;
                var lat 	= all[i].Latitude;
                var lng 	= all[i].Longitude;
                //当位于同一坐标是显示
                for(var j=0;j<i;j++){
                if((all[j].Latitude == lat)||(all[j].Longitude == lng)){
                ip=ip+'<br/>'+all[j].Ip;
                }
                }
                var latlngset;
                latlngset = new google.maps.LatLng(lat, lng);
                var marker = new google.maps.Marker({
                  map: map,
                  title: organization,
                  position: latlngset
                });
                var content = '<div class="map-content"><h3>'+ ip+ '<br/>' + '</h3>' + organization + '<br />' + '<br/>'+'纬度：' +lat + '<br/>'+' 经度：'  + lng + '</div>';
                var infowindow = new google.maps.InfoWindow();
                  infowindow.setContent(content);
                  google.maps.event.addListener(
                    marker,
                    'click',
                    infoCallback(infowindow, marker)
                  );
              }
            }
            // Set all markers in the all variable
            setMarkers(map, all);
          };
          // Initializes the Google Map
          google.maps.event.addDomListener(window, 'load', initialize);
        </script>
      </head>
      <body>
        <div id="map_canvas" style="height: 500px; width: 800px;"></div>
      </body>
    </html>
    """ % log
    LogFile.write(LogContent)