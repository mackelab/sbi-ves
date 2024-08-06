<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="header-outer" style="background-color: #455a64;">
      <q-toolbar class="header-inner q-ma-none q-pa-none">
        <q-toolbar-title class="text-center">
          <q-img src="~/assets/layers.png" width="100px" fit="contain"/>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container class="flex row full-width justify-center"
                      style="padding: 0 !important">
      <router-view/>
    </q-page-container>
  </q-layout>
</template>
<script setup lang="ts">
import {onBeforeMount} from 'vue';

import {useCoreStore} from "stores/core";
import {useRouter} from "vue-router";

const coreStore = useCoreStore();
const router = useRouter();

onBeforeMount(() => {
  if (coreStore.isLoggedIn) {
    router.push({name: 'login'})
  }
})

</script>

<style scoped>

</style>
