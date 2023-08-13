<script setup>
defineEmits([ 'search' ])
</script>

<template>
  <input type="text" placeholder="Enter a username ..." />
</template>

<style scoped>
input {
  flex: 1;
  width: 100%;
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
</style>