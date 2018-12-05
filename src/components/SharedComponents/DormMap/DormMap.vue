<template>
<v-container grid-list-sm pa-2>
  <div :style="mapStyle">
    <l-map :zoom="zoom" :center="center" :style="mapStyle" @update:center="centerUpdate" @update:zoom="zoomUpdate">
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-marker :lat-lng="marker">
        <l-popup v-if="showParagraph" >
          <div @click="popupClick">
            Tooltip
            <p v-show="showParagraph"></p>
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
