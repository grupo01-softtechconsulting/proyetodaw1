<template>
  <v-app id="profile-user" class="primary">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4 lg4>
            <v-card class="elevation-1 pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <h1 class="flex my-4 primary--text">Perfil de Usuario</h1>
                </div>
                <v-form>
                  <v-text-field
                    v-model="lastName"
                    :error-messages="lastNameErrors"
                    label="Apellidos"
                    append-icon="person"
                    required
                    :disabled="!editActive"
                    type="text"
                    @keyup.enter="editProfile"
                    @input="$v.lastName.$touch()"
                    @blur="$v.lastName.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="firstName"
                    :error-messages="firstNameErrors"
                    label="Nombre(s)"
                    append-icon="person"
                    required
                    :disabled="!editActive"
                    type="text"
                    @keyup.enter="editProfile"
                    @input="$v.firstName.$touch()"
                    @blur="$v.firstName.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="email"
                    :error-messages="emailErrors"
                    label="Correo Electrónico"
                    append-icon="person"
                    required
                    :disabled="!editActive"
                    type="text"
                    @keyup.enter="editProfile"
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn v-if="!editActive" block color="primary" @click="activateEdit" :loading="loadingButton">Editar</v-btn>
                <v-btn v-if="editActive" block color="primary" @click="editProfile" :loading="loadingButton">Giardar Cambios</v-btn>
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
    firstName: { required },
    lastName: { required },
    email: { required, email }
  },

  data: () => ({
    editActive: false,
    loadingButton: false,
    firstName: '',
    lastName: '',
    email: '',
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
    }
  },

  created() {
    api
      .obtainPerson()
      .then(res => {
        this.firstName = res.user.first_name
        this.lastName = res.user.last_name
        this.email = res.user.email
      });
  },
  
  methods: {
    activateEdit() {
      this.editActive = true
    },
    editProfile () {
      this.loadingButton = true
      this.$v.$touch()

      if (!this.$v.firstName.$invalid && !this.$v.lastName.$invalid && !this.$v.email.$invalid) {
        let jsonData = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email
        }
        api.updatePerson(jsonData).then(res => {
          this.editActive = false
          this.loadingButton = false
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
