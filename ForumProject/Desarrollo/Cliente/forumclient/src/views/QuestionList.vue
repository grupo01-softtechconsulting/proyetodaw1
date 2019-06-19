<template>
  <div id="list-questions">
    <v-layout row pb-2>
      <v-flex xs12 sm8 offset-sm2>
        <v-card class="card--flex-toolbar">
          <v-toolbar card prominent>
            <v-toolbar-title class="subheading">Listado de Preguntas</v-toolbar-title>
          </v-toolbar>

          <v-divider></v-divider>

          <v-card-text v-if="questions.length > 0" style="height: auto;">
            <!--<v-layout row wrap>
              <v-flex>
                <v-text-field
                  v-model="searchText"
                  solo
                  label="Buscar paciente"
                  prepend-inner-icon="search"
                  @keyup="searchPatientData"
                ></v-text-field>
              </v-flex>
            </v-layout> -->
            <template v-if="isLoadingpage">
              <div class="text-xs-center">
                <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
              </div>
            </template>
            <template v-for="item in questions">
              <v-card v-show="!isLoadingpage" :key="item.id">
                <v-card-title primary-title>
                  <div>
                    <div
                      class="headline"
                    >{{ item.title }}</div>
                    <span class="grey--text">Fecha de realización: {{ item.creation_date }}</span>
                    <br>
                    <span>{{ item.statement }}</span>
                  </div>
                </v-card-title>
                <v-card-actions>
                   <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on }">
          <v-btn dark v-on="on" flat color="primary" @click="addAnswer(item.creator.id)">Responder pregunta</v-btn>
      </template>

      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          {{ item.statement }}
        </v-card-title>

       <v-flex>
        <v-textarea
          v-model="answer"
          solo
          name="input-7-4"
          label="Ingrese respuesta"
        ></v-textarea>
      </v-flex>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="addAnswerInsert(item.creator.id)"
          >
            Responder
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
                  <v-btn flat color="primary" @click="addQuestion(item.creator.id)">Nueva pregunta</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </template>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import apiQuestion from "@/services/question"

export default {
  data: () => ({
    isLoadingpage: false,
    nextPage: null,
    timeout: null,
    questions: [],
    idSelected: "",
    showMoreInfo: false,
    dialog: false,
    answer: ''
  }),
  created() {
    this.isLoadingpage = true
    apiQuestion
      .getAllQuestionsList({})
      .then(res => {
        this.questions = res
        this.isLoadingpage = false
      });
  },
  methods: {
    addQuestion () {
    },
    addAnswer () {
     

    },
    addAnswerInsert(id){

        let jsonData = {
          question_id: id,
          statement: this.answer
        }
        apiQuestion.createAnswer(jsonData).then(res => {
          if (res.status) {
            localStorage.setItem('personId', res.person_id)
            this.dialog = false
          } else {
            this.dialog = false
          }
        })

    }
  },
  mounted () {
    // this.scroll()
  }
};
</script>
