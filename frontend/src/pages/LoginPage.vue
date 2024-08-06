<template>
  <q-page class="col-xs-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
    <q-card flat full-width>
      <q-card-section class="q-mt-xl">
        <div class="text-h6 text-center"> Login</div>
        <q-form @submit="login">
          <q-input
            class="q-mt-md"
            v-model="username"
            label="Username"
          />
          <q-input
            class="q-mt-md"
            :type="hidePassword ? 'password' : 'text'"
            v-model="password"
            label="Password"
          >
            <template v-slot:append>
              <q-icon
                :name="hidePassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="hidePassword = !hidePassword"
              />
            </template>
          </q-input>
        </q-form>
      </q-card-section>
      <q-card-actions vertical alging="center" class="justify-center q-mt-lg q-mb-lg">
        <q-btn class="q-mt-sm q-mb-sm" @click="login"> Login</q-btn>
        <q-btn class="q-mt-sm q-mb-sm" :to="'/register'"> Register</q-btn>
      </q-card-actions>
    </q-card>
  </q-page>
</template>
<script setup lang="ts">

import {ref} from "vue";
import {useCoreStore} from "stores/core";
import {useRouter} from "vue-router";


const router = useRouter();
const coreStore = useCoreStore();

let username = ref('');
let password = ref('');
let loading = ref(false);
let hidePassword = ref(true);


const login = async function (): Promise<void> {
  loading.value = true;
  await coreStore
    .login({
      username: username.value,
      password: password.value,
    })
    .then(async (loginSuccess: boolean) => {
      if (loginSuccess) {
        await redirectToNextPage();
      }
      loading.value = false;
    });
};

const redirectToNextPage = async function (): Promise<void> {
  let redirectUrl = router.currentRoute.value.query.redirectUrl as string | undefined;
  if (
    redirectUrl &&
    redirectUrl.startsWith('/') &&
    !redirectUrl.startsWith('/login') &&
    !redirectUrl.startsWith('/logout')
  ) {
    await router.push(redirectUrl);
  } else {
    await router.push({name: 'home'});
  }
};

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
