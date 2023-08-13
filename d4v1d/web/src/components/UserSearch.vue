<script setup>
import { ref } from 'vue'

const emit = defineEmits([ 'search' ])
const username = ref('')

const doSearch = () => {
  if (!username.value.trim()) return
  emit('search', username.value)
}

const handleInput = e => {
  if (e.keyCode === 13) doSearch()
}
</script>

<template>
  <div>
    <input @keyup="handleInput" v-model="username" type="text" placeholder="Enter a username ..." />
    <button @click="doSearch">
      asdf
    </button>
  </div>
</template>

<style scoped>
div {
  flex: 1;
  width: 100%;
  display: flex;
  justify-content: stretch;
  align-items: stretch;
}

input {
  flex: 1;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  padding: 1em;
  border: none;
  font-family: inherit;
  font-size: 1em;
}

input:focus {
  outline: none;
}

button {
  background-color: var(--vt-c-accent);
  color: var(--vt-c-text-dark-1);
}
</style>