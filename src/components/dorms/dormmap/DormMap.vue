<template>
<v-container grid-list-sm>
  <div :style="mapStyle">
    <l-map :zoom="zoom" :center="center" :style="mapStyle" @update:center="centerUpdate" @update:zoom="zoomUpdate">
      <l-tile-layer :url="url" :attribution="attribution" />
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

<script src="./DormMap.js"></script>

<style lang="scss">
@import "~leaflet/dist/leaflet.css";
</style>
