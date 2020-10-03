<template>
    <v-app>
        <v-app-bar
        app
        dense
        color="primary"
        dark>
        <div class="d-flex align-center">
            <v-icon class="mr-2">mdi-map-marker-distance</v-icon>
            <h2>PathWays</h2>
        </div>

        <v-spacer></v-spacer>
        </v-app-bar>

        <v-main>
            <Stepper/>
        </v-main>
    </v-app>
</template>

<script>
import Stepper from './views/Stepper';

export default {
    name: 'App',

    components: {
        Stepper,
    },

    data: () => ({
        //
    }),
};
</script>
