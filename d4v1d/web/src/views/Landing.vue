<script setup>
import UserSearch from '../components/UserSearch.vue';

const handleSearch = username => {
  console.log(username)
}
</script>

<template>
  <main>
    <img src="@/assets/logo-cropped.png" />
    <div class="search">
      <UserSearch @search="handleSearch" />
    </div>
  </main>
</template>

<style>
body {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60vw;
  padding: 2em;
  user-select: none;
}

img {
  width: 15vh;
  height: 15vh;
  margin-bottom: 1.5em;
}

.search {
  width: 100%;
}

@media only screen and (max-width: 600px) {
  main {
    width: 100vw;
  }
}
</style>