import Vue from 'vue'
import VueRouter from 'vue-router'
import Stepper from '../views/Stepper.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Stepper',
    component: Stepper
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
