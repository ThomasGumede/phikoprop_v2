$(function () {
  var LocsA = [
    {
      lat: -31.6091556,
      lon: 28.799608333333335,
      title: "Nowethu House",
      html: [
        '<div class="map-product-item">',
        '<a href="#"><img src="./assets/img/product/1.png" alt="#"></a>',
        '<h5 class="ltn__map-product-title"><a href="#">Nowethu House</a></h5>',
        '<h5 class="ltn__map-product-price">R1,200/month.</h5>',
        '<p class="ltn__map-product-info"><span>3 Bed</span><span>3 Bath</span><span>1220 ft<sup>2</sup></span></p>',
        '<p class="ltn__map-product-location"><i class="flaticon-pin"></i>22 Gerald Street, Ikhwezi Township, Umthatha, EC</span>',
        "</div>",
      ].join(""),
      // icon: "../assets/img/icons/map-marker-2.png",
      animation: google.maps.Animation.BOUNCE,
    },
    {
      lat: -31.566502,
      lon: 28.878021,
      title: "St Patricks Private Hostel",
      html: [
        '<div class="map-product-item">',
        '<a href="#"><img src="./assets/img/product/2.png" alt="#"></a>',
        '<h5 class="ltn__map-product-title"><a href="#">St Patricks Private Hostel</a></h5>',
        '<h5 class="ltn__map-product-price">R1,200/month.</h5>',
        '<p class="ltn__map-product-info"><span>3 Bed</span><span>3 Bath</span><span>1220 ft<sup>2</sup></span></p>',
        '<p class="ltn__map-product-location"><i class="flaticon-pin"></i>Zitatele Administration Area, Gxulu Location, Libode, EC</span>',
        "</div>",
      ].join(""),
      // icon: "../assets/img/icons/map-marker-2.png",
      animation: google.maps.Animation.BOUNCE,
    },
  ];
  new Maplace({
    locations: LocsA,
    show_markers: true,
    controls_on_map: true,
    map_options: {
      zoom: 13,
      scrollwheel: false,
      stopover: true,
    },
    stroke_options: {
      strokeColor: "#f10",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#f10",
      fillOpacity: 0.4,
    },
  }).Load();
});
