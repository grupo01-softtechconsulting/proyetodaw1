<template>
  <v-navigation-drawer
    :mini-variant.sync="mini"
    fixed
    app
    :dark="$vuetify.dark"
    v-model="drawer"
    >
    <v-toolbar color="primary darken-1" dark>
      <img src="@/assets/avatar-img.png" height="36" alt="Predictor Web">
      <v-toolbar-title class="ml-0 pl-3">
        <span class="hidden-sm-and-down">Foro Web</span>
      </v-toolbar-title>
    </v-toolbar>
      <v-list dense expand>
        <template v-for="item in items">
          <v-list-tile v-if="item.name!=='login'"
            :to="!item.href ? { name: item.name } : null"
            :href="item.href"
            ripple="ripple"
            :disabled="item.disabled"
            :key="item.name"
          >
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-else
            :key="item.name"
            @click="doLogout()"
          >
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
  </v-navigation-drawer>
</template>

<script>
import api from '@/services/auth'

export default {
  data: () => ({
    mini: false,
    drawer: false,
    items: [
      { title: 'Perfil', icon: 'assignment', component: 'profile', name: 'profile' },
      { title: 'Listado de Preguntas', icon: 'list_alt', component: 'question-list', name: 'question-list' }
    ]
  }),

  created () {
    if (localStorage.getItem('rValue') == 1) {
      this.items = [
        { title: 'Perfil', icon: 'assignment', component: 'profile', name: 'profile' },
        { title: 'Listado de Preguntas', icon: 'list_alt', component: 'question-list', name: 'question-list' }
      ]
    } else {
      this.items = [
        { title: 'Perfil', icon: 'assignment', component: 'profile', name: 'profile' },
        { title: 'Listado de Preguntas', icon: 'list_alt', component: 'question-list', name: 'question-list' }
      ]
    }
    window.getApp.$on('APP_DRAWER_TOGGLED', () => {
      this.drawer = (!this.drawer)
    })
  },

  methods: {
    /*doLogout () {
      api.logout(localStorage.getItem('personId'))
        .then(res => {
          if (res.status) {
            localStorage.clear()
            window.getApp.$emit('APP_LOGOUT')
          }
        })
    }*/
  }
}
</script>
