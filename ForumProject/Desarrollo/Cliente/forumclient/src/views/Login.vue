<template>
  <v-app id="login" class="primary">
    <v-content>
      <v-container fluid fill-height>
        <h3>Este es el login, agregar html aqui :v</h3>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import authApi from '@/services/auth'

export default {
  name: 'login',
  components: {
  }
}
</script>

<style lang="scss" scoped>
  #login {
    height: 50%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    content: "";
    z-index: 0;
  }
</style>
