<template>
  <router-view/>
</template>

<script setup lang="ts">
import {useCoreStore} from "stores/core";
import {onBeforeMount} from "vue";

const coreStore = useCoreStore();

onBeforeMount(async () => {
  if (coreStore.lastError) {
    coreStore.lastError = null;
  }
});

defineOptions({
  name: 'App'
});
</script>
