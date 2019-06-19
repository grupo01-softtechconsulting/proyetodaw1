<template>
  <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent max-width="600px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">Nueva Pregunta</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                  <v-text-field label="Tu pregunta*" required></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
            <v-btn color="blue darken-1" flat @click="dialog = false">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
</template>

<script>
import api from '@/services/auth'

export default {
  data: () => ({
    
  }),

  created () {
    
  },

  methods: {
    addQuestion () {
      let jsonData = {
          question_id: id,
          statement: this.answer
        }
        apiQuestion.createQuestion(jsonData).then(res => {
          if (res.status) {
            localStorage.setItem('personId', res.person_id)
            this.dialog = false
          } else {
            this.dialog = false
          }
        })
    },
  }
}
</script>
