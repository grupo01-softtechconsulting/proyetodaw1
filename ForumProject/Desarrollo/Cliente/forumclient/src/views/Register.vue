<template>
  <v-app id="register" class="primary">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4 lg4>
            <v-card class="elevation-1 pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <h1 class="flex my-4 primary--text">Nuevo Usuario</h1>
                </div>
                <v-form>
                  <v-text-field
                    v-model="lastName"
                    :error-messages="lastNameErrors"
                    label="Apellidos"
                    append-icon="person"
                    required
                    type="text"
                    @keyup.enter="register"
                    @input="$v.lastName.$touch()"
                    @blur="$v.lastName.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="firstName"
                    :error-messages="firstNameErrors"
                    label="Nombre(s)"
                    append-icon="person"
                    required
                    type="text"
                    @keyup.enter="register"
                    @input="$v.firstName.$touch()"
                    @blur="$v.firstName.$touch()"
                  ></v-text-field>
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
                    v-model="username"
                    :error-messages="usernameErrors"
                    label="Usuario"
                    append-icon="person"
                    required
                    type="text"
                    @keyup.enter="register"
                    @input="$v.username.$touch()"
                    @blur="$v.username.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :error-messages="passwordErrors"
                    :append-icon="showLeftMenu ? 'visibility' : 'visibility_off'"
                    :type="showLeftMenu ? 'text' : 'password'"
                    label="Contraseña"
                    class="input-group--focused"
                    @keyup.enter="register"
                    @click:append="showLeftMenu = !showLeftMenu"
                    required
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="primary" @click="register" :loading="loadingButton">Registrar</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <CustomSnackbar
      :snackbarOptions="snackbarOptions"
    />
  </v-app>
</template>

<script>
import CustomSnackbar from '@/components/Snackbar.vue'
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
import api from '@/services/auth'

export default {
  mixins: [validationMixin],
  validations: {
    firstName: { required },
    lastName: { required },
    email: { required, email },
    username: { required },
    password: { required }
  },

  components: {
    CustomSnackbar
  },

  data: () => ({
    loadingButton: false,
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    snackbarOptions: { show: false, text: '' },
    showLeftMenu: false
  }),

  computed: {
    firstNameErrors () {
      const errors = []
      if (!this.$v.firstName.$dirty) return errors
      !this.$v.firstName.required && errors.push('Ingrese un nombre')
      return errors
    },
    lastNameErrors () {
      const errors = []
      if (!this.$v.lastName.$dirty) return errors
      !this.$v.lastName.required && errors.push('Ingrese los apellidos')
      return errors
    },
    emailErrors () {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email &&
        errors.push('Debe ingresar un correo electrónico válido')
      !this.$v.email.required && errors.push('Ingrese un correo electrónico')
      return errors
    },
    usernameErrors () {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.required && errors.push('Ingrese un usuario')
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
    register () {
      this.loadingButton = true
      this.$v.$touch()

      if (!this.$v.firstName.$invalid && !this.$v.lastName.$invalid && !this.$v.email.$invalid && !this.$v.username.$invalid && !this.$v.password.$invalid) {
        let jsonData = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          username: this.username,
          password: this.password
        }
        api.register(jsonData).then(res => {
          if (res.status == false) {
            this.loadingButton = false
            this.snackbarOptions.show = true
            this.snackbarOptions.text = 'Ha ingresado un correo inválido'
          } else {
            localStorage.setItem('personId', res.person_id)
            this.$router.push({ name: "profile" })
          }
          /*if (res.status) {
            localStorage.setItem('personId', res.person_id)
            this.$router.push({ name: "profile" })
          } else {
            this.loadingButton = false
          }*/
        })
      } else {
        this.loadingButton = false
      }
    },
    clear () {
      this.$v.$reset()
      this.firstName = ''
      this.lastName = ''
      this.email = ''
      this.username = ''
      this.password = ''
    }
  }
}
</script>

<style lang="scss" scoped>
  #register {
    height: 50%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    content: "";
    z-index: 0;
  }
</style>