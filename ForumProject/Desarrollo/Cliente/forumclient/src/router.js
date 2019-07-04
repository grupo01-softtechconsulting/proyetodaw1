import Vue from 'vue'
import Router from 'vue-router'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import QuestionList from './views/QuestionList.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login,
    meta: { isPublic: true }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { isPublic: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { isPublic: false }
  },
  {
    path: '/question-list',
    name: 'question-list',
    component: QuestionList,
    meta: { isPublic: false }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
  }
]

Vue.use(Router)

const isAuthenticated = function () {
  return true
}

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.meta.isPublic && !isAuthenticated()) {
    localStorage.clear()
    return next({ name: 'login' })
  }

  return next()
})

router.afterEach((to, from) => {
  // Loading
})

export default router
