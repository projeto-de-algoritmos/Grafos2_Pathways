<template>
    <v-stepper
        v-model="stepperStep"
        vertical>
        <v-stepper-step
            :complete="stepperStep > 1"
            step="1">
            Selecione a área
            <small>O nível de zoom deve estar entre 16 e 18</small>
        </v-stepper-step>

        <v-stepper-content step="1">
            <MapSearcher
                @areaSelected="areaSelected"/>
        </v-stepper-content>

        <v-stepper-step
            :complete="stepperStep > 2"
            step="2">
            Selecionar pontos
        </v-stepper-step>

        <v-stepper-content 
            eager
            step="2">
            <MapRenderer 
                :coordinates="coordinates" />
        </v-stepper-content>
    </v-stepper>
</template>

<script>
import MapSearcher from "./maps/MapSearcher"
import MapRenderer from "./maps/MapRenderer"

export default {
    data: () => ({
        stepperStep: 1,
        coordinates: {
            left: 0, 
            right: 0, 
            top: 0, 
            bottom:0
        }
    }),
    components: {
        MapSearcher,
        MapRenderer
    },
    methods: {
        areaSelected({ left, right, top, bottom }) {
            this.stepperStep++
            this.coordinates = {
                left, right, top, bottom
            }

        }
    }
}
</script>