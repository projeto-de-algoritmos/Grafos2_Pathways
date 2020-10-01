<template>
    <div id="map-container">
        <div class="pa-3 left-side">

            <v-text-field
                readonly
                v-model="zoom"
                label="Nível de zoom" />
            <v-text-field
                readonly
                v-model="topLat"
                label="Norte" />
            <v-text-field
                readonly
                v-model="bottomLat"
                label="Sul" />
            <v-text-field
                readonly
                v-model="rigthLog"
                label="Leste" />
            <v-text-field
                readonly
                v-model="leftLog"
                label="Oeste" />

            <v-btn
                color="primary"
                depressed
                @click="searchByCoordinates">
                Selecionar área
            </v-btn>
        </div>
        <l-map
            style="height: 100%; width: 80%"
            :zoom="zoom"
            :center="center"
            @update:zoom="zoomUpdated"
            @update:center="centerUpdated"
            @update:bounds="boundsUpdated">
            <l-tile-layer :url="url"></l-tile-layer>
        </l-map>
    </div>
</template>
<script>
import axios from "axios";
import 'leaflet/dist/leaflet.css';
import { LMap, LTileLayer } from 'vue2-leaflet';

export default {
    components: {
        LMap,
        LTileLayer,
    },
    data () {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 16,
            center: {
                lat: (-15.817726838705601 + -15.832694018132468)/2,
                lng: (-48.06909458456959 + -48.05246488867724)/2
            },
            bounds: null,
            topLat: -15.817726838705601, 
            bottomLat: -15.832694018132468,
            rigthLog: -48.06909458456959,
            leftLog: -48.05246488867724,
        };
    },
    methods: {
        zoomUpdated (zoom) {
            this.zoom = zoom;
        },
        centerUpdated (center) {
            this.center = center;
        },
        boundsUpdated (bounds) {
            this.bounds = bounds;
        },
        async searchByCoordinates() {
            if (this.zoom >= 16 && this.zoom <= 19) {
                this.$emit('areaSelected', {
                    top: this.topLat, 
                    bottom: this.bottomLat,
                    right: this.rigthLog,
                    left:  this.leftLog,
                })
            }
            else {
                alert("Zoom incorreto, usar nível entre 16 e 19!!!!")
            }
        }
    },
    watch: {
        bounds: function(val) {
            this.topLat = val._northEast.lat
            this.leftLog = val._northEast.lng
            this.bottomLat = val._southWest.lat
            this.rigthLog = val._southWest.lng
        }
    }
}
</script>

<style lang="scss">
#map-container {
    height: calc(100vh - 150px);
    display: flex;

    .left-side {
        width: 20%;
        min-width: 250px;
    }

    .vue2leaflet-map {
        z-index: 0;
    }
}
</style>