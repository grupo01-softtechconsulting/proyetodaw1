import axios from 'axios'
import configService from './config'

const url = configService.apiUrl

const api = {}

axios.defaults.baseURL = url

/** Creates a new question */
api.createQuestion = function (questionData) {
  return axios.post(
    '/question/question-api/',
    { creator: localStorage.getItem('personId'),
      title: questionData['title'],
      statement: questionData['statement']
    },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Updates a question */
api.updateQuestion = function (questionData) {
  return axios.patch(
    '/question/question-api/' + questionData['question_id'].toString() + '/',
    { 
      title: questionData['title'],
      statement: questionData['statement']
    },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Deletes a question */
api.deleteQuestion = function (questionId) {
  return axios.delete(
    '/question/question-api/' + questionId.toString() + '/',
    { },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Gets questions submitted to the platform */
api.getAllQuestionsList = function (filtersData) {
  var dataParams = {};
  if ('last_questions' in filtersData) {
    dataParams['last_questions'] = true
  } else {
    if ('by_tag' in filtersData) {
      dataParams['by_tag'] = true
    } else if ('newest' in filtersData) {
      dataParams['newest'] = true
    } else if ('oldest' in filtersData) {
      dataParams['oldest'] = true
    }
  }
  return axios.get(
    '/question/question-api/',
    dataParams,
    { headers: {
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Gets all questions from a certain person (you or another person) */
api.getSumittedQuestionsList = function (filtersData) {
  var dataParams = {
    person_id: filtersData['person_id']
  }
  if ('last_questions' in filtersData) {
    dataParams['last_questions'] = true
  } else {
    if ('by_tag' in filtersData) {
      dataParams['by_tag'] = true
    } else if ('newest' in filtersData) {
      dataParams['newest'] = true
    } else if ('oldest' in filtersData) {
      dataParams['oldest'] = true
    }
  }
  return axios.get(
    '/question/question-api/',
    dataParams,
    { headers: {
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Gets data of a certain question */
api.getQuestionData = function (questionId) {
  return axios.get(
    '/question/question-api/' + questionId.toString() + '/',
    {},
    { headers: {
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}


/** Gets answers submitted to a certain question */
api.getAnswersList = function (questionId) {
  return axios.get(
    '/question/answer-api/',
    {
      question_id: questionId
    },
    { headers: {
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Creates a new answer */
api.createAnswer = function (answerData) {
  return axios.post(
    '/question/answer-api/',
    { 
      creator: localStorage.getItem('personId'),
      question: answerData['question_id'],
      statement: answerData['statement']
    },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Updates an answer */
api.updateAnswer = function (answerData) {
  return axios.patch(
    '/question/answer-api/' + answerData['answer_id'].toString() + '/',
    { 
      statement: answerData['statement']
    },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

/** Deletes an answer */
api.deleteAnswer = function (answerId) {
  return axios.delete(
    '/question/answer-api/' + answerId.toString() + '/',
    { },
    { headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token')
    } }
  ).then(res => res.data)
}

export default api
