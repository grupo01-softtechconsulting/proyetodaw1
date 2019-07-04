<template>
  <div id="appRoot">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <template v-if="!$route.meta.isPublic">
      <v-app id="inspire" class="app">
        <comp-drawer class="app--drawer"/>
        <comp-toolbar class="app--toolbar"/>
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
    <pw-snackbar
      :snackbarOptions="snackbarOptions"
    />
  </div>
</template>

<script>
import PwSnackbar from '@/components/Snackbar.vue'
import CompDrawer from '@/components/Toolbar.vue'
import CompToolbar from '@/components/Drawer.vue'
import AppEvents from '@/event'

export default {
  name: 'App',
  components: {
    CompToolbar,
    CompDrawer,
    PwSnackbar
  },
  data () {
    return {
      snackbarOptions: {
        show: false,
        text: ''
      }
    }
  },
  created () {
    AppEvents.forEach(item => {
      this.$on(item.name, item.callback)
    })
    window.getApp = this
  }
}
</script>

<style lang="stylus" scoped>
  .setting-fab
    top:50%!important;
    right:0;
    border-radius:0;
  .page-wrapper
    min-height:calc(100vh - 64px - 50px - 81px );
</style>
