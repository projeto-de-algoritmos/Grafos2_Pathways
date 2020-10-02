<template>
    <div id="map-renderer">
        
        
        <div class="pa-3 left-side">
            <p>Selecione o ponto de partida e o ponto de chegada.</p>
            <p>Para selecionar o ponto de partida simplesmente clique sobre um nó. Ele ficará verde.</p>
            <p>Para selecionar o ponto de chegada simplesmente clique com o botão de contexto sobre um nó. Ele ficará vermelho.</p>
            <small>O botão de contexto para quem usa mouse é o botão direito do mouse. No caso de macs apenas clique com dois dedos no trackpad</small>
            
            <p v-if="finished"><b>Caminho encontrado! Distância percorrida: {{pathLength}} metros</b></p>

            <v-btn
                block
                color="success"
                v-if="!finished"
                depressed
                @click="confirmSelection">
                Confirmar seleção.
            </v-btn>
            <v-btn
                block
                depressed
                color="primary"
                v-if="finished"
                @click="drawLines">
                Ver todas arestas
            </v-btn>
         </div>
        <l-map
            ref="myMap" 
            @ready="doSomethingOnReady()"
            style="height: 100%; width: 80%"
            :zoom="zoom"
            :center="center"
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
        markers: [],
        startPoint: {
            current: null,
            old: null,
            node: null
        },
        finishPoint: {
            current: null,
            old: null,
            node: null
        },
        hasPath: false,
        nodesAjd: {},
        nextQueue: [],
        finished: false,
        pathLength: 0
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
                this.mountArrayOfAdj()
                this.loading = false
                this.spinning = false
            } catch(error) {
                console.log(error)
                this.spinning = false
                this.overlayMesage = "Erro ao carregar dados da api"
            }
        },
        drawLines() {
            this.edges.map(edge => {
                const from = this.nodes.find(node => node.id === edge.from) 
                const to = this.nodes.find(node => node.id === edge.to)
                
                L.polyline([[from.y, from.x], [to.y, to.x]])
                    .bindPopup(`Tamanho: ${ edge.length }`)
                    .on('mouseover', function (e) {
                        this.openPopup();
                    })
                    .on('mouseout', function (e) {
                        this.closePopup();
                    })
                    .addTo(this.map);
            }, this)
        },
        emptyMapLines() {
            /**
             * Retirado de 
             * https://stackoverflow.com/questions/14585688/clear-all-polylines-from-leaflet-map
             */
            for(let i in this.map._layers) {
                if(this.map._layers[i]._path != undefined) {
                    try {
                        this.map.removeLayer(this.map._layers[i]);
                    }
                    catch(e) {
                        console.log("problem with " + e + this.map._layers[i]);
                    }
                }
            }
        },
        mountArrayOfAdj() {
            this.edges.map(edge => {
                if (this.nodesAjd[edge.from]) {
                    this.nodesAjd[edge.from].push(edge.to)
                }
                else {
                    this.nodesAjd[edge.from] = [edge.to]
                }
            }, this)
        },
        confirmSelection() {
            if(this.startPoint.current.sourceTarget._leaflet_id &&
                this.finishPoint.current.sourceTarget._leaflet_id) {
                

                if (this.startPoint.current.sourceTarget._leaflet_id ===
                this.finishPoint.current.sourceTarget._leaflet_id) {
                    alert("Os pontos de inicio e fim devem ser diferentes!!!")
                }

                else {

                    this.searchDijkstra(this.startPoint.node);
                }
            }
            else {
                alert("Selecione os pontos de inicio e fim!!!")
            }
            
        },
        /**
         * Busca usando o algoritmo de Dijkstra's
         */
        searchDijkstra(initialNode) {
            let localNodes = JSON.parse(JSON.stringify(this.nodes))
            const localNodesHash = {}
            const localEdgesHash = {}
            const setS = {};
            
            localNodes.map(node => {
                setS[node.id] = {
                    cost: node.id === this.startPoint.node.id? 0 :99999,
                    fromNode: undefined
                }

                localNodesHash[node.id] = node
            }, this) 

            this.edges.map(edge => {
                localNodesHash[edge.from + "/" + edge.to] = edge
            })

            localNodes = null

            this.nextQueue = []

            this.exploredNodes = {}
            this.exploredNodes[initialNode.id] = true

            const _this = this
            // =============



            function checaVizinhos(localNode) {
                
                monitoraVizinhos(localNode);

                while(_this.nextQueue.length) {
                    let searchOn = _this.nextQueue.shift()

                    _this.nextQueue = _this.nextQueue.filter(item => item.id != searchOn.id)

                    setS[searchOn.id] = {
                        cost: searchOn.cost,
                        fromNode: searchOn.fromNode
                    }

                    _this.exploredNodes[searchOn.id] = true

                    if (searchOn.id === _this.finishPoint.node.id) {
                        setS[searchOn.id] = {
                            cost: searchOn.cost,
                            fromNode: searchOn.fromNode
                        }
                        _this.hasPath = true
                        console.log(setS[searchOn.id])
                        return;
                    }
                    monitoraVizinhos(searchOn)
                }
            
                alert("Não há caminho entre os nós selecionados")
                return

            }

            function monitoraVizinhos(localNode) {
                if (_this.nodesAjd[localNode.id]) {
                    for (let vizinho of _this.nodesAjd[localNode.id]) {
                        if (!_this.exploredNodes[vizinho]) {
                            vizinho = localNodesHash[vizinho]
                            _this.queuePushAndSort({
                                id: vizinho.id,
                                cost: (localNode.cost || 0) + localNodesHash[localNode.id + "/" + vizinho.id].length,
                                fromNode: localNode.id
                            })
                        }
                    }
                }
            }

            checaVizinhos(initialNode)
            
            console.log(setS[this.finishPoint.node.id])

            
            if (this.hasPath) {
                this.finished = true
                this.doBackTrack(setS)
            }
            // =============
        },
        doBackTrack(setS) {
            let x = 999999
            let id = this.finishPoint.node.id
            this.pathLength = setS[id].cost
            const routes = []

            while(x != 0) {
                routes.push(this.edges.find(edge => edge.from === setS[id].fromNode && edge.to === id))
                
                id = setS[id].fromNode
                
                x = setS[id].cost
            }

            routes.map(edge => {
                const from = this.nodes.find(node => node.id === edge.from) 
                const to = this.nodes.find(node => node.id === edge.to)
                
                L.polyline([[from.y, from.x], [to.y, to.x]], { weight: 6, color: "orange"})
                    .bindPopup(`Tamanho: ${ edge.length }`)
                    .on('mouseover', function (e) {
                        this.openPopup();
                    })
                    .on('mouseout', function (e) {
                        this.closePopup();
                    })
                    .addTo(this.map);
            }, this)

            console.log(setS, routes)
        },
        queuePushAndSort(elem) {
            this.nextQueue.push(elem)
            this.nextQueue.sort(function(a,b)  {
                if (a.cost > b.cost) return 1
                if (a.cost < b.cost) return -1
                return 0
            });
        },
        renderPoints() {
            const _this = this
            this.nodes.map(node => {
                L.circleMarker([node.y, node.x], {radius: 7, color: '#3388ff'} ).addTo(this.map)
                    .on('click', function(item){
                        item.sourceTarget.setStyle({
                            color: "green"
                        })
                        if (_this.startPoint.current) {
                            if (_this.startPoint.current.sourceTarget._leaflet_id == item.sourceTarget._leaflet_id)  return;
                            _this.startPoint.current.sourceTarget.setStyle({ color: '#3388ff' })
                            _this.startPoint.old = _this.startPoint.current
                            _this.startPoint.current = item
                            _this.startPoint.node = node
                        }
                        else {
                           _this.startPoint.current = item 
                           _this.startPoint.node = node
                        }
                        console.log(item)
                    })
                    .on('contextmenu', function(item) {
                       item.sourceTarget.setStyle({
                            color: "red"
                        })
                        if (_this.finishPoint.current) {
                            if (_this.finishPoint.current.sourceTarget._leaflet_id == item.sourceTarget._leaflet_id)  return;
                            _this.finishPoint.current.sourceTarget.setStyle({ color: '#3388ff' })
                            _this.finishPoint.old = _this.finishPoint.current
                            _this.finishPoint.current = item
                            _this.finishPoint.node = node
                        }
                        else {
                           _this.finishPoint.current = item 
                           _this.finishPoint.node = node
                        }
                        console.log(item) 
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