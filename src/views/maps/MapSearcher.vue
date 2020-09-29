<template>
    <div id="map-container">
        <div class="info" style="width: 20%">
            <span>Center: {{ center }}</span>
            <span>Zoom: {{ zoom }}</span>
            <span>Bounds: {{ bounds }}</span>

            <v-btn
                @click="searchByCoordinates">
                Realizar busca com o endereço da região atual
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
            zoom: 3,
            center: [47.413220, -1.219482],
            bounds: null,
            client: axios.create({ baseURL: "https://www.openstreetmap.org/api/0.6/"}),
            valuesToSearch: {
                topLat: 0, 
                bottomLat: 0,
                rigthLog: 0,
                leftLog: 0,
            }
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
                const response = await this.client.get("map.json?bbox=" +
                    this.valuesToSearch.rigthLog + "%2C" +
                    this.valuesToSearch.bottomLat + "%2C" +
                    this.valuesToSearch.leftLog + "%2C" +
                    this.valuesToSearch.topLat)
    
                console.log(response);
            }
            else {
                alert("Zoom incorreto, usar nível entre 16 e 19!!!!")
            }
        }
    },
    watch: {
        bounds: function(val) {
            this.valuesToSearch.topLat = val._northEast.lat
            this.valuesToSearch.leftLog = val._northEast.lng
            this.valuesToSearch.bottomLat = val._southWest.lat
            this.valuesToSearch.rigthLog = val._southWest.lng
            console.log(this.valuesToSearch, val)
        }
    }
}
</script>

<style lang="scss">
#map-container {
    height: calc(100vh - 100px);
    display: flex;

    .vue2leaflet-map {
        z-index: 10;
    }
}
</style>