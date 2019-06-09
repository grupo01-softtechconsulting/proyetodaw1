export default [
  {
    name: 'APP_LOGOUT',
    callback: function (e) {
      this.$router.replace({ path: '/login' })
    }
  }
]
