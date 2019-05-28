import axios from 'axios'
import configService from './config'

const url = configService.apiUrl

const api = {}

axios.defaults.baseURL = url

api.authenticate = function (loginData) {
  return axios.post(
    '/login-api/',
    { username: loginData['username'],
      password: loginData['password']
    },
    { headers: {
      'Content-Type': 'application/json'
    } }
  )
    .then(res => res.data)
}

api.authenticate = function (userData) {
  return axios.post(
    '/register-api/',
    { first_name: userData['first_name'],
      last_name: userData['last_name'],
      email: userData['email'],
      username: userData['username'],
      password: userData['password']
    },
    { headers: {
      'Content-Type': 'application/json'
    } }
  )
    .then(res => res.data)
}

export default api
