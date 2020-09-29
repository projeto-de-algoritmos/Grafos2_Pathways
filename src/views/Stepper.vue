<template>
    <v-stepper
        v-model="stepperStep"
        vertical>
        <v-stepper-step
            :complete="stepperStep > 1"
            step="1">
            Select an app
            <small>Summarize if needed</small>
        </v-stepper-step>

        <v-stepper-content step="1">
            <MapSearcher/>
        </v-stepper-content>

        <v-stepper-step
            :complete="stepperStep > 2"
            step="2">
            Configure analytics for this app
        </v-stepper-step>

        <v-stepper-content step="2">
            <v-card
                color="grey lighten-1"
                class="mb-12"
                height="200px"
            ></v-card>
            <v-btn
                color="primary"
                @click="stepperStep = 3">
                Continue
            </v-btn>
            <v-btn text>
                Cancel
            </v-btn>
        </v-stepper-content>
    </v-stepper>
</template>

<script>
import MapSearcher from "./maps/MapSearcher"

export default {
    data: () => ({
        stepperStep: 1
    }),
    components: {
        MapSearcher
    }
}
</script>