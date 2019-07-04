<template>
  <v-snackbar
    v-model="snackbarOptions.show"
    :bottom="y === 'bottom'"
    :left="x === 'left'"
    :multi-line="mode === 'multi-line'"
    :right="x === 'right'"
    :timeout="timeout"
    :top="y === 'top'"
    :vertical="mode === 'vertical'"
  >
    {{ snackbarOptions.text }}
    <v-btn color="primary" flat @click="snackbarOptions.show = false">Cerrar</v-btn>
  </v-snackbar>
</template>

<script>
export default {
  props: {
    snackbarOptions: {
      show: false,
      text: ''
    }
  },

  data: () => ({
    //snackbar: false,
    y: "top",
    x: null,
    mode: "",
    timeout: 3000,
    //text: "Hello, I'm a snackbar"
  })
};
</script>