<template>
  <div id="appRoot">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <template v-if="!$route.meta.isPublic">
      <v-app id="inspire" class="app">
        <v-content>
          <!-- Page Header -->
          <!-- Content -->
          <div class="page-wrapper">
            <router-view></router-view>
    </div>
           <!-- App Footer -->
        </v-content>
        <!-- Go to top -->
      </v-app>
    </template>
    <template v-else>
      <transition>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </transition>
    </template>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  },
  data () {
    return {
    }
  },
  created () {
  }
}
</script>

<style lang="scss">
</style>
