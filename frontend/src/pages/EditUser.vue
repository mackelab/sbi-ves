<template>
  <q-page padding>
    <edit-wrapper>
      <template #header>
        <q-item :clickable="false" class="text-h6 q-pl-none text-grey-10">
          <q-item-section>
            Edit Personal Data
          </q-item-section>
        </q-item>
      </template>

      <q-card flat square class="overflow-auto q-mt-md">
        <q-card-section class="col-6 col-xl-6 q-px-lg q-mt-md">
          <q-input
            class="q-mt-md"
            v-model="userStore.editUser.firstName"
            label="First Name"
          />
          <q-input
            class="q-mt-md"
            v-model="userStore.editUser.lastName"
            label="Last Name"
          />
          <q-input
            class=" q-mt-md"
            v-model="userStore.editUser.institution"
            label="Institution"/>
          <q-input
            class="q-mt-md"
            v-model="userStore.editUser.email"
            label="E-mail"
          />
          <q-input
            class="q-mt-md"
            v-model="userStore.editUser.username"
            label="Username"
          />
        </q-card-section>
        <q-card-actions>
          <q-btn flat :to="'/home'">Cancel</q-btn>
          <q-btn flat @click="saveUser">Save</q-btn>
        </q-card-actions>
      </q-card>
    </edit-wrapper>
  </q-page>
</template>
<script setup lang="ts">
import {useCoreStore} from "stores/core";


import {onMounted} from 'vue';
import {useUserStore} from 'stores/user';
import EditWrapper from 'components/EditWrapper.vue';
import {clearUser} from "src/models/models";

const userStore = useUserStore();
const coreStore = useCoreStore();

function saveUser() {
  userStore.saveUser()
}

onMounted(() => {
  if (!!coreStore.user.id) {
    userStore.fetchUser(coreStore.user.id)
  } else {
    userStore.editUser = clearUser;
  }
})
</script>
<style scoped>

</style>
