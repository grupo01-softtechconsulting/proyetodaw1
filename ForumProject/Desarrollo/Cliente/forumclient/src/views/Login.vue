<template>
  <v-app id="login" class="primary">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4 lg4>
            <v-card class="elevation-1 pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <h1 class="flex my-4 primary--text">Iniciar sesión</h1>
                </div>
                <v-form>
                  <v-text-field
                    v-model="email"
                    :error-messages="emailErrors"
                    label="Correo Electrónico"
                    append-icon="person"
                    required
                    type="text"
                    @keyup.enter="register"
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :error-messages="passwordErrors"
                    :append-icon="showLeftMenu ? 'visibility' : 'visibility_off'"
                    :type="showLeftMenu ? 'text' : 'password'"
                    label="Contraseña"
                    class="input-group--focused"
                    @keyup.enter="login"
                    @click:append="showLeftMenu = !showLeftMenu"
                    required
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="primary" @click="login" :loading="loadingButton">Ingresar</v-btn>
                <v-btn block color="primary" @click="registrar" :loading="loadingButton">Registrarme</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
import api from '@/services/auth'

export default {
  mixins: [validationMixin],
  validations: {
    email: { required, email },
    password: { required }
  },

  data: () => ({
    loadingButton: false,
    email: '',
    password: '',
    showLeftMenu: false
  }),

  computed: {
    emailErrors () {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email &&
        errors.push('Debe ingresar un correo electrónico válido')
      !this.$v.email.required && errors.push('Ingrese un correo electrónico')
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.required && errors.push('Ingrese una contraseña')
      return errors
    }
  },

  methods: {
    login () {
      this.loadingButton = true
      this.$v.$touch()

      if (!this.$v.email.$invalid && !this.$v.password.$invalid) {
        let jsonData = {
          username: this.email,
          password: this.password
        }
        api.authenticate(jsonData).then(res => {
          if (res.status) {
            localStorage.setItem('personId', res.person_id)
            this.$router.push({ name: "profile" })
          } else {
            this.loadingButton = false
          }
        })
      } else {
        this.loadingButton = false
      }
    },
    registrar () {
       this.$router.push({ name: "register" })
    },
    clear () {
      this.$v.$reset()
      this.email = ''
      this.password = ''
    }
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
