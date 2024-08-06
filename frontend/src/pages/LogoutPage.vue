<template>
  <div/>
</template>
<script setup lang="ts">
import {onMounted} from "vue";
import {useCoreStore} from "stores/core";
import {useRouter} from "vue-router";
import {useUserStore} from "stores/user";

const coreStore = useCoreStore();
const userStore = useUserStore();
const router = useRouter();

onMounted(async () => {
  await router.push({
    name: 'login',
  });

  coreStore.$reset()
  userStore.$reset()

})
</script>
<style lang="scss">
:root {
  --header-inner-height: 100px;
  --header-outer-height: clamp(var(--header-inner-height), 20vh, 220px);
  --header-height-difference: calc(var(--header-outer-height) - var(--header-inner-height));
}

.header-outer {
  position: sticky;
  z-index: 1000;
  height: var(--header-outer-height);
  top: calc(var(--header-height-difference) * -1);
}

.header-inner {
  height: var(--header-inner-height);
  position: sticky;
  top: calc(var(--header-height-difference) - 40px);
}
</style>
