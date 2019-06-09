<template>
  <div>
    <v-toolbar
      color="primary"
      fixed
      dark
      app
      >
      <v-toolbar-title class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="openMenu"></v-toolbar-side-icon>
      </v-toolbar-title>
        <!--<v-text-field
          flat
          solo-inverted
          prepend-icon="search"
          label="Search"
          class="hidden-sm-and-down"
          >
        </v-text-field>-->
        <v-spacer></v-spacer>
        <!--<v-btn icon @click="handleFullScreen()">
          <v-icon>fullscreen</v-icon>
        </v-btn>-->
        <v-menu offset-y origin="center center" :nudge-bottom="10" transition="scale-transition">
          <v-btn icon large flat slot="activator">
            <v-avatar size="30px">
              <img src="@/assets/avatar-img.png" alt="Usuario"/>
            </v-avatar>
          </v-btn>
          <v-list class="pa-0">
            <v-list-tile v-for="(item,index) in items" :to="!item.href ? { name: item.name } : null" @click="doLogout()" ripple="ripple" :disabled="item.disabled" :target="item.target" rel="noopener" :key="index">
              <v-list-tile-action v-if="item.icon">
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-menu>
    </v-toolbar>
  </div>
</template>

<script>
export default {
  data: () => ({
    items: [
      {
        icon: 'exit_to_app',
        title: 'Salir',
        option: 4
      }
    ]
  }),

  methods: {
    doLogout () {
      localStorage.clear()
      window.getApp.$emit('APP_LOGOUT')
    },
    openMenu () {
      window.getApp.$emit('APP_DRAWER_TOGGLED')
    }
  }
}
</script>

<style lang="scss" scoped>
  .card--flex-toolbar {
    margin-top: -64px;
  }
</style>
