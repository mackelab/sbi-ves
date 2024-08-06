import {defineStore} from 'pinia';
import {AxiosError} from 'axios';
import Bluebird from 'bluebird';
import {RegisterUserDto} from "src/models/register-user-dto";
import {extend} from "quasar";
import {clearRegisterUser} from "src/models/models";
import {registerUser} from "stores/api";

export const useRegisterStore = defineStore('register', {
  state: () => ({
    user: extend<RegisterUserDto>(true, {}, clearRegisterUser),
    test: 'test',
  }),
  getters: {},
  actions: {
    async registerUser() {
      return Bluebird.resolve(registerUser(this.user))
        .then((res: RegisterUserDto) => {
          console.log('Request successful - User registered')
          console.log(res)
          return res;
        })
        .catch((err: Error | AxiosError) => {
          return Promise.reject(err)
        })
    },
  }
})
