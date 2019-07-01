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
   <v-dialog v-model="dialogAnswer" max-width="600">
      <v-card>
        <v-card-title class="headline">{{ questionSelected.statement }}</v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>  
              <v-flex xs12 sm12>
                <v-textarea
                  v-model="answer"
                  required
                  label="Escriba su respuesta"
                  :error-messages="answerErrors"
                  @input="$v.answer.$touch()"
                  @blur="$v.answer.$touch()"
                ></v-textarea>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-flex row>
            <v-btn v-if="!activeEditAnswer" color="primary darken-1" flat="flat" @click="addAnswerInsert(questionSelected.id)" :loading="loadingSaveAnswer">Guardar respuesta</v-btn>
            <v-btn v-if="activeEditAnswer" color="primary darken-1" flat="flat" @click="updateAnswer()" :loading="loadingSaveAnswer">Actualizar respuesta</v-btn>
            <v-btn color="blank darken-1" flat="flat" @click="cancelAnswer()">Cancelar</v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialogQuestion" max-width="600">
      <v-card>
        <v-card-title v-if="!activeEditQuestion" class="headline">Nueva pregunta</v-card-title>
        <v-card-title v-if="activeEditQuestion" class="headline">Editar pregunta</v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12>
                <v-text-field 
                  label="Titulo"
                  required
                  :error-messages="titleErrors"
                  v-model="title"
                  @input="$v.title.$touch()"
                  @blur="$v.title.$touch()"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12>
                <v-textarea
                  label="Contenido"
                  required
                  :error-messages="contentErrors"
                  v-model="content"
                  @input="$v.content.$touch()"
                  @blur="$v.content.$touch()"></v-textarea>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-flex row>
            <v-btn v-if="!activeEditQuestion" color="primary darken-1" flat="flat" @click="saveQuestion()" :loading="loadingSaveQuestion">Agregar pregunta</v-btn>
            <v-btn v-if="activeEditQuestion" color="primary darken-1" flat="flat" @click="updateQuestion()" :loading="loadingSaveQuestion">Editar pregunta</v-btn>
            <v-btn color="blank darken-1" flat="flat" @click="cancelQuestion()">Cancelar</v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialogConfirmDeleteQuestion" max-width="300">
      <v-card>
        <v-card-title class="headline">Eliminar pregunta</v-card-title>
        <v-card-text>
          <h3>Esta seguro que desea eliminar la pregunta?</h3>
        </v-card-text>
        <v-card-actions>
          <v-flex row>
            <v-btn color="primary darken-1" flat="flat" @click="deleteQuestion()" :loading="loadingDeleteQuestion">Aceptar</v-btn>
            <v-btn color="blank darken-1" flat="flat" @click="cancelDeleteQuestion()">Cancelar</v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import apiQuestion from "@/services/question";

export default {
  mixins: [validationMixin],
  validations: {
    title: { required },
    content: { required },
    answer: { required }
  },
  data: () => ({
    isLoadingpage: false,
    dialogQuestion: false,
    dialogAnswer: false,
    loadingSaveQuestion: false,
    loadingSaveAnswer: false,
    sortItems: ['Más nuevo', 'Más antiguo'],
    valuesItems: [0,1],
    optionsQuestion: ['Editar pregunta', 'Eliminar pregunta'],
    valuesOptionsQuestion: [0,1],
    title: "",
    content: "",
    nextPage: null,
    timeout: null,
    questions: [],
    answers: [],
    idSelected: "",
    showMoreInfo: false,
    answer: "",
    questionSelected: {
      id: null,
      statement: "",
      title: ""
    },
    globalParams: {},
    autorText: '',
    queryUrl: {},
    answerToUpdate: null,
    activeEditAnswer: false,
    activeEditQuestion: false,
    dialogConfirmDeleteQuestion: false,
    loadingDeleteQuestion: false,
    showMyQuestions: false
  }),
  created() {
    this.isLoadingpage = true;
    this.globalParams['last_questions'] = 'true'
    this.loadAjaxQuestions()
  },
  computed: {
    titleErrors() {
      const errors = [];
      if (!this.$v.title.$dirty) return errors;
      !this.$v.title.required &&
        errors.push("Debe poner un titulo a la pregunta");
      return errors;
    },
    contentErrors() {
      const errors = [];
      if (!this.$v.content.$dirty) return errors;
      !this.$v.content.required &&
        errors.push("Debe poner un contenido para la pregunta");
      return errors;
    },
    answerErrors() {
      const errors = [];
      if (!this.$v.answer.$dirty) return errors;
      !this.$v.answer.required && errors.push("Debe escribir una respuesta");
      return errors;
    }
  },
  methods: {

    changeShowMyQuestions () {
      if (this.showMyQuestions) {
        this.queryUrl['my_questions'] = 'true'
      } else {
        delete this.queryUrl['my_questions']
      }
      this.loadAjaxQuestions()
    },

    deleteQuestion() {
      apiQuestion.deleteQuestion(this.questionSelected.id).then(res => {
        this.queryUrl = {}
        this.questionSelected = {
          id: null,
          statement: "",
          title: ''
        };
        this.dialogConfirmDeleteQuestion = false
        this.loadingDeleteQuestion = false;
        this.title = ''
        this.content = ''
        this.loadAjaxQuestions()
      });
    },

    updateQuestion() {
      let dataAjax = {
        question_id: this.questionSelected.id,
        title: this.title,
        statement: this.content
      }
      apiQuestion.updateQuestion(dataAjax).then(res => {
        this.queryUrl = {}
        this.questionSelected = {
          id: null,
          statement: "",
          title: ''
        };
        this.dialogQuestion = false;
        this.loadingSaveQuestion = false;
        this.title = ''
        this.content = ''
        this.loadAjaxQuestions()
      });
    },

    makeActionQuestion(itemQuestion) {
      if (this.valuesOptionsQuestion.indexOf('Editar') != -1) {
        this.$v.$reset();
        this.activeEditQuestion = true
        this.questionSelected.id = itemQuestion.id;
        this.questionSelected.statement = itemQuestion.statement;
        this.questionSelected.title = itemQuestion.title
        this.title = itemQuestion.title
        this.content = itemQuestion.statement
        this.dialogQuestion = true;
      } else {
        this.questionSelected.id = itemQuestion.id;
        this.questionSelected.statement = itemQuestion.statement;
        this.questionSelected.title = itemQuestion.title
        this.dialogConfirmDeleteQuestion = true
      }
    },

    editAnswer (itemQuestion, itemAnswer) {
      this.activeEditAnswer = true
      this.$v.$reset();
      this.questionSelected.id = itemQuestion.id;
      this.questionSelected.statement = itemQuestion.statement;
      this.answerToUpdate = itemAnswer.id
      this.answer = itemAnswer.statement
      this.dialogAnswer = true;
    },

    updateAnswer () {
      let dataAjax = {
        answer_id: this.answerToUpdate,
        statement: this.answer
      }
      apiQuestion.updateAnswer(dataAjax).then(res => {
        this.questionSelected = {
          id: null,
          statement: "",
          title: ''
        };
        window.location.reload()
      });
    },

    checkAutorAnswer (idAutor) {
      if (idAutor == localStorage.getItem('personId')) {
        return true
      }
      return false
    },

    checkAutorQuestion(idAutor) {
      if (idAutor == localStorage.getItem('personId')) {
        return true
      }
      return false
    },

    sortQuestions () {
      delete this.globalParams['last_questions']
      if (this.valuesItems.indexOf('nuevo') != -1) {
        this.globalParams['newest'] = 'true'
        delete this.globalParams['oldest']
        this.queryUrl['order_by'] = 'newest'
        
      } else {
        this.globalParams['oldest'] = 'true'
        delete this.globalParams['newest']
        this.queryUrl['order_by'] = 'oldest'
      }
      this.loadAjaxQuestions()
    },

    searchAutor() {
      let _self = this
      this.isLoadingpage = true
      clearTimeout(this.timeout)
      if (this.autorText.trim() !== "") {
        this.timeout = setTimeout(function() {
          _self.globalParams['autor_text'] = _self.autorText
          _self.queryUrl['search_autor'] = _self.autorText
          _self.loadAjaxQuestions()
        }, 500)
      } else {
        this.timeout = setTimeout(function() {
          delete _self.globalParams['autor_text']
          delete _self.queryUrl['search_autor']
          _self.loadAjaxQuestions()
        }, 500)
      }
    },

    loadAjaxQuestions () {
      //this.isLoadingpage = true;
      this.questions = []
      apiQuestion.getAllQuestionsList(this.queryUrl).then(res => {
        this.questions = res;
        this.$router.push({query: this.queryUrl})
        this.isLoadingpage = false;
      });
    },

    showAnswers (item) {
      item.active_answer = !item.active_answer
      if (item.active_answer) {
        item.list_answers = []
        apiQuestion.getAnswersList(item.id).then(res => {
          item.list_answers = res
        });
      }
    },

    saveQuestion() {
      this.loadingSaveQuestion = true;
      this.$v.$touch();
      if (!this.$v.title.$invalid && !this.$v.content.$invalid) {
        let jsonData = {
          title: this.title,
          statement: this.content
        };
        apiQuestion.createQuestion(jsonData).then(res => {
          this.dialogQuestion = false;
          this.questions = [];
          this.queryUrl = {}
          apiQuestion.getAllQuestionsList(this.queryUrl).then(res => {
            this.questions = res;
            this.$router.push({query: this.queryUrl})
            this.loadingSaveQuestion = false;
            this.isLoadingpage = false;
            this.title = ''
            this.content = ''
          });
        });
      } else {
        this.loadingSaveQuestion = false;
      }
    },

    addQuestion() {
      this.$v.$reset();
      this.activeEditQuestion = false
      this.dialogQuestion = true;
    },

    cancelQuestion() {
      this.title = ''
      this.content = ''
      this.dialogQuestion = false;
    },

    showDialogAnswer(itemSelected) {
      this.activeEditAnswer = false
      this.$v.$reset();
      this.questionSelected.id = itemSelected.id;
      this.questionSelected.statement = itemSelected.statement;
      this.dialogAnswer = true;
    },

    cancelAnswer() {
      this.answer = ''
      this.questionSelected = {
        id: null,
        statement: "",
        title: ''
      };
      this.dialogAnswer = false;
    },

    addAnswerInsert(id) {
      this.loadingSaveAnswer = true;
      this.$v.$touch();
      if (!this.$v.answer.$invalid) {
        let jsonData = {
          question_id: id,
          statement: this.answer
        };
        apiQuestion.createAnswer(jsonData).then(res => {
          this.loadingSaveAnswer = false;
          this.answer = ''
          if (res.status) {
            localStorage.setItem("personId", res.person_id);
            this.dialogAnswer = false;
            
          } else {
            this.dialogAnswer = false;
          }
          window.location.reload()
        });
      } else {
        this.loadingSaveAnswer = false;
      }
    }
  },

  mounted() {
    // this.scroll()
  }
};
</script>