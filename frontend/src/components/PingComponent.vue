<template>
  <div>
   <q-btn :label="pingStore.pingMessage" @click="ping"></q-btn>
  </div>
</template>

<script setup lang="ts">
// import {ref} from 'vue';
// import axios from 'axios';
import {usePingStore} from 'stores/ping';
// import {onMounted} from 'vue';

const pingStore = usePingStore();


function ping() {
  pingStore.ping();
}


</script>
