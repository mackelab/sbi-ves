<template>
  <q-page full-width class="col-xs-12 col-sm-6 col-md-8 col-lg-8 col-xl-6">
    <q-card flat full-width>
      <q-card-section class="q-mt-xl">
        <div class="text-h6 text-center"> Register</div>
        <q-form @submit="registerUser">
          <q-input
            class="q-mt-md"
            v-model="registerStore.user.firstName"
            label="First Name"
          />
          <q-input
            class="q-mt-md"
            v-model="registerStore.user.lastName"
            label="Last Name"
          />
          <q-input
            class=" q-mt-md"
            v-model="registerStore.user.institution"
            label="Institution"/>
          <q-input
            class="q-mt-md"
            v-model="registerStore.user.email"
            label="E-mail"
          />
          <q-input
            class="q-mt-md"
            v-model="registerStore.user.username"
            label="Username"
          />
          <q-input
            class="q-mt-md"
            :type="hidePassword ? 'password' : 'text'"
            v-model="registerStore.user.password"
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
          <q-input
            class="q-mt-md"
            :type="hideConfirmationPassword ? 'password' : 'text'"
            v-model="registerStore.user.confirmPassword"
            label="Password"
          >
            <template v-slot:append>
              <q-icon
                :name="hideConfirmationPassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="hideConfirmationPassword = !hideConfirmationPassword"
              />
            </template>
          </q-input>
        </q-form>
      </q-card-section>
      <q-card-actions>
        <q-btn flat :to="'/'">Cancel</q-btn>
        <q-btn flat @click="registerUser">Register</q-btn>
      </q-card-actions>
    </q-card>
  </q-page>
</template>
<script setup lang="ts">

import {ref} from "vue";
import {useRegisterStore} from "stores/register";
import {useRouter} from "vue-router";

const router = useRouter();
const registerStore = useRegisterStore();
const hidePassword = ref(true);
const hideConfirmationPassword = ref(true);


function registerUser() {
  registerStore.registerUser()
    .then(() => {
      router.push('/login')
    })
    .catch(
      (error) => {
        console.log(error)
      })
}

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
