<template>
  <div id="list-questions">
    <v-layout row pb-2>
      <v-flex xs12 sm8 offset-sm2>
        <v-card class="card--flex-toolbar">
          <v-toolbar card prominent>
            <v-toolbar-title class="subheading">Listado de Preguntas<v-btn flat color="primary" @click="addQuestion()">Nueva pregunta</v-btn></v-toolbar-title>
          </v-toolbar>

          <v-divider></v-divider>

          <v-card-text style="height: auto;">
            <v-layout row wrap>
              <v-flex>
                <v-text-field
                  v-model="autorText"
                  solo
                  label="Buscar por autor"
                  prepend-inner-icon="search"
                  @keyup="searchAutor"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout  v-if="!isLoadingpage && questions.length > 0" row wrap>
              <v-flex xs6 sm6 d-flex>
                <v-select
                  :items="sortItems"
                  label="Ordenar por"
                  v-model="valuesItems"
                  @change="sortQuestions"
                ></v-select>
              </v-flex>
              <v-flex xs6 sm6 d-flex>
                <v-switch
                  v-model="showMyQuestions"
                  label="Mis preguntas"
                  @change="changeShowMyQuestions"
                ></v-switch>
              </v-flex>
            </v-layout>
            <template v-if="isLoadingpage">
              <div class="text-xs-center">
                <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
              </div>
            </template>
            <div v-if="!isLoadingpage && questions.length > 0">
              <template v-for="item in questions">
                <v-card v-show="!isLoadingpage" :key="item.id">
                  <v-card-title primary-title>
                    <div>
                      <div class="headline">{{ item.title }}</div>
                      <span class="grey--text">Fecha de realización: {{ item.creation_date }}</span>
                      <br>
                      <span class="grey--text">Autor: {{ item.creator.user.first_name }} {{ item.creator.user.last_name }}</span>
                      <br>
                      <span>{{ item.statement }}</span>
                      <br>
                      <span v-if="item.edit_date" class="grey--text">Ultima edicion: {{ item.edit_date }}</span>
                    </div>
                  </v-card-title>

                  <v-card-actions>
                    <v-btn flat color="primary" @click="showDialogAnswer(item)">Responder pregunta</v-btn>
                    <v-overflow-btn
                      v-if="checkAutorQuestion(item.creator.id)"
                      :items="optionsQuestion"
                      v-model="valuesOptionsQuestion"
                      @change="makeActionQuestion(item)"
                      label="Opciones"
                    ></v-overflow-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      @click="showAnswers(item)"
                    >
                      <v-icon>{{ item.active_answer ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                    </v-btn>
                  </v-card-actions>
                  <v-slide-y-transition>
                    <v-card-text v-show="item.active_answer">
                      <div v-if="item.list_answers.length > 0">
                        <span>Listado de respuestas:</span>
                        <template v-for="answerItem in item.list_answers">
                          <v-card :key="answerItem.id">
                            <v-card-title primary-title>
                              <div>
                                <v-btn small flat color="primary" v-if="checkAutorAnswer(answerItem.creator.id)" @click="editAnswer(item, answerItem)">Editar respuesta</v-btn>
                                <h5>Autor: {{ answerItem.creator.user.first_name }} {{ answerItem.creator.user.last_name }}</h5>
                                <span class="grey--text">Fecha de realización: {{ answerItem.creation_date }}</span>
                                <br>
                                <span>{{ answerItem.statement }}</span>
                              </div>
                            </v-card-title>
                          </v-card>
                        </template>
                      </div>
                      <div v-if="item.list_answers.length == 0">
                        <h4>No hay respuestas que mostrar</h4>
                      </div>
                    </v-card-text>
                  </v-slide-y-transition>
                </v-card>
              </template>
            </div>
            <div v-if="!isLoadingpage && questions.length == 0">
              <h2>No hay preguntas que mostrar</h2>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-dialog v-model="dialogQuestion" max-width="290">
      <v-card>
        <v-card-title class="headline">Nueva pregunta</v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12>
                <v-text-field
                  label="Titulo"
                  required
                  v-model="title"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12>
                <v-text-field
                  label="Contenido"
                  required
                  v-model="content"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary darken-1" flat="flat" @click="saveQuestion(1)">Agregar pregunta</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import apiQuestion from "@/services/question"

export default {
  data: () => ({
    isLoadingpage: false,
    dialogQuestion: false,
    title: '',
    content: '',
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
    saveQuestion () {
      let jsonData = {
          title: this.title,
          statement: this.content
        }
        apiQuestion.createQuestion(jsonData).then(res => {
            this.dialogQuestion = false
            this.questions = []
            apiQuestion
            .getAllQuestionsList({})
            .then(res => {
              this.questions = res
              this.isLoadingpage = false
            });
        })
    },

    addQuestion() {
      this.dialogQuestion = true
    },

    addAnswer () {


    },
    addAnswerInsert(id){

        let jsonData = {
          question_id: id,
          statement: this.content
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
