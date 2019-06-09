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
                  <v-btn flat color="primary" @click="addQuestion(item.creator.id)">Nueva pregunta</v-btn>
                  <v-btn flat color="primary" @click="addAnswer(item.creator.id)">Responder pregunta</v-btn>
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
    showMoreInfo: false
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

    }
  },
  mounted () {
    // this.scroll()
  }
};
</script>
