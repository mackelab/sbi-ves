import {defineStore} from 'pinia';
import {AxiosError} from 'axios';
import Bluebird from 'bluebird';
import {UserDto} from "src/models/user-dto";
import {extend} from "quasar";
import {clearUser} from "src/models/models";
import {getUserById, getUsers, postUser} from "stores/api";

export const useUserStore = defineStore('user', {
  state: () => ({
    userList: [] as UserDto[],
    editUser: extend<UserDto>(true, {}, clearUser),
  }),
  getters: {},
  actions: {
    async fetchUser(userId: string) {
      return Bluebird.resolve(getUserById(userId))
        .then((res: UserDto) => {
          console.log('Request successful - Load user')
          console.log(res)
          this.editUser = res
        })
        .catch((err: Error | AxiosError) => {
          return Promise.reject(err)
        })
    },

    async fetchAllUsers() {
      return Bluebird.resolve(getUsers())
        .then((res: UserDto[]) => {
          console.log('Request successful - Load all users')
          console.log(res)
          this.userList = res;
        })
        .catch((err: Error | AxiosError) => {
          return Promise.reject(err)
        })
    },

    async saveUser() {
      return Bluebird.resolve(postUser(this.editUser))
        .then((res: UserDto) => {
          console.log('Request successful - Save user')
          console.log(res)
          this.editUser = res;
          return res;
        })
        .catch((err: Error | AxiosError) => {
          return Promise.reject(err)
        })
    },
  }
})
