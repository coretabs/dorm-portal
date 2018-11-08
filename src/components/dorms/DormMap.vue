<template>
  <v-container grid-list-sm>
    <div :style="mapStyle">
      <l-map
        :zoom="zoom"
        :center="center"
        :style="mapStyle"
        @update:center="centerUpdate"
        @update:zoom="zoomUpdate">
        <l-tile-layer
          :url="url"
          :attribution="attribution"/>
        <l-marker :lat-lng="marker">
          <l-popup>
            <div @click="popupClick">
              I am a tooltip
              <p v-show="showParagraph">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque sed pretium nisl, ut sagittis sapien. Sed vel sollicitudin nisi. Donec finibus semper metus id malesuada.
              </p>
            </div>
          </l-popup>
        </l-marker>
      </l-map>
    </div>
  </v-container>
</template>

<script>
  import "leaflet/dist/leaflet.css";
  import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';
  import L from 'leaflet';
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
  });
  export default {
    name: 'DormMap',
    components: {
      LMap,
      LTileLayer,
      LMarker,
      LPopup
    },
    props:{
      'longitude': Number,
      'latitude' : Number
    },
    data: function (){
      return{
       roomsLeft: 7,
        zoom: 15,
        center: L.latLng(this.longitude, this.latitude),
        url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        marker: L.latLng(this.longitude, this.latitude),
        currentZoom: 10,
        currentCenter: L.latLng(this.longitude, this.latitude),
        showParagraph: false,
        mapStyle: {
          height: '400px'
        }
      }
    },
    methods: {
      zoomUpdate (zoom) {
        this.currentZoom = zoom;
      },
      centerUpdate (center) {
        this.currentCenter = center;
      },
      showLongText () {
        this.showParagraph = !this.showParagraph;
      },
      popupClick () {
        alert('Popup Click!');
      }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';
@import "~leaflet/dist/leaflet.css";
</style>