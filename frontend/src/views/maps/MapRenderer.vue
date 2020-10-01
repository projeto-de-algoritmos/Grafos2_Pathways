<template>
    <div id="map-renderer">
         <div class="pa-3 left-side">
            TODO
         </div>
        <l-map
            ref="myMap" 
            @ready="doSomethingOnReady()"
            style="height: 100%; width: 80%"
            :zoom="zoom"
            :center="center"
            :max-bounds="limits"
            @update:zoom="zoomUpdated"
            @update:center="centerUpdated">
            <l-tile-layer :url="url"></l-tile-layer>
        </l-map>
        <v-overlay 
            absolute
            :value="loading">
            <div class="d-flex flex-column align-center">
                <v-progress-circular v-if="spinning" indeterminate size="64"></v-progress-circular>
                <h2>{{ overlayMesage }}</h2>
            </div>
        </v-overlay>
    </div>
</template>

<script>
import axios from "axios";
import 'leaflet/dist/leaflet.css';
import L, { latLngBounds, latLng, Icon } from "leaflet";

import { LMap, LTileLayer } from 'vue2-leaflet';

export default {
    components: {
        LMap,
        LTileLayer,
    },
    props: {
        coordinates: {
            type: Object,
            default: () => ({
                left: 0, 
                right: 0, 
                top: 0, 
                bottom:0
            })
        }
    },
    computed: {
        topCord() {
            return this.coordinates.top
        },
        limits() {
            return latLngBounds([
                [this.coordinates.top, this.coordinates.left],
                [this.coordinates.bottom, this.coordinates.right]
            ])
        }
    },
    data: () => ({
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        center: {
            lat: 0,
            lng: 0
        },
        client: axios.create({ baseURL: "http://0.0.0.0:8001/graph"}),
        zoom: 1,
        map: undefined,
        nodes: [],
        edges: [],
        overlayMesage: "Carregando dados da api...",
        loading: false,
        spinning: false,
        markers: []
    }),
    methods: {
        centerUpdated (center) {
            this.center = center;
        },
        zoomUpdated (zoom) {
            this.zoom = zoom;
        },
        updateMap() {
            const coordinates = [(this.coordinates.top + this.coordinates.bottom) / 2, (this.coordinates.left + this.coordinates.right) / 2]
            const latlnh = latLng(...coordinates)
            this.map.setZoom(15)
            this.map.setView(latlnh)
        },
        emptyMap() {
            this.center = {
                lat:0,
                lng: 0
            }
        },
        doSomethingOnReady() {
            this.map = this.$refs.myMap.mapObject
        },
        async searchGraphData() {
            this.loading = true
            this.spinning = true
            try {
                const response = await this.client.get(
                    `/?top=${this.coordinates.top}&bottom=${this.coordinates.bottom}&right=${this.coordinates.right}&left=${this.coordinates.left}`
                )
    
                this.nodes = response.data.nodes
                this.edges = response.data.edges
                this.updateMap()
                this.renderPoints()
                this.loading = false
                this.spinning = false
            } catch(error) {
                console.log(error)
                this.spinning = false
                this.overlayMesage = "Erro ao carregar dados da api"
            }
        },
        renderPoints() {
            
            this.nodes.map(node => {
                L.circleMarker([node.y, node.x], {radius: 7}).addTo(this.map).on('click', function(){
                    console.log("click")
                });
            })
        }
    },
    watch: {
        topCord: function(val, old) {
            if (old === 0) {
                this.emptyMap()
                this.searchGraphData()
            }
        }
    },
    mounted() {
        delete Icon.Default.prototype._getIconUrl;
        Icon.Default.mergeOptions({
            iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
            iconUrl: require('leaflet/dist/images/marker-icon.png'),
            shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        });
    }
}
</script>

<style lang="scss">
#map-renderer {
    height: calc(100vh - 150px);
    display: flex;
    position: relative;

    .left-side {
        width: 20%;
        min-width: 250px;
    }

    .vue2leaflet-map {
        z-index: 0;
    }
}
</style>