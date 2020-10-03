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
                block
                color="success mb-3"
                depressed
                @click="searchByCoordinates">
                Confirmar seleção
            </v-btn>
            <v-btn
                block
                color="primary"
                depressed
                @click="getCurrentLocation">
                Pegar localização atual
            </v-btn>
        </div>
        <l-map
            @ready="doSomethingOnReady()"
            ref="myMap" 
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
import L, { latLngBounds, latLng, Icon } from "leaflet";

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
                lat: 0,
                lng: 0
            },
            bounds: null,
            topLat: 0, 
            bottomLat: 0,
            rigthLog: 0,
            leftLog: 0,
            map: undefined
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
        updateMap({ latitude, longitude }) {
            const latlnh = latLng(latitude, longitude)
            this.map.setZoom(16)
            this.map.setView(latlnh)
        },
        async searchByCoordinates() {
            if (this.zoom >= 16 && this.zoom <= 19) {
                if (this.topLat) {
                    this.$emit('areaSelected', {
                        top: this.topLat, 
                        bottom: this.bottomLat,
                        right: this.rigthLog,
                        left:  this.leftLog,
                    })
                }
                else {
                    alert("Selecione uma área válida no mapa")
                }
            }
            else {
                alert("Zoom incorreto, usar nível entre 16 e 19!!!!")
            }
        },
        doSomethingOnReady() {
            this.map = this.$refs.myMap.mapObject
        },
        getCurrentLocation() {
            const _this = this
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position, err) => {
                    if (err) {
                        alert(err)
                    }
                    else {
                        _this.updateMap(position.coords)
                    }
                });
            } else {
                alert("Geolocation is not supported by this browser.");
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