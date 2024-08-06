import { defineStore } from 'pinia';
import axios from 'axios';
import { AxiosError } from 'axios';
import Bluebird from 'bluebird';

export const usePingStore = defineStore('ping', {
  state:() => ({
    pingMessage: 'The Request has not been sent yet' as string,
  }),
  getters:{},
  actions: {
    async pingApi(): Promise<string> {
      const vesbiApi = axios.create({ baseURL: 'http://localhost:5000' });
      return vesbiApi.get('/ping')
        .then( (res) => {
          return res.data;
        })
        .catch( (err) => {
          return err;
        })
    },
    async ping() {
      return Bluebird.resolve(this.pingApi())
        .then( (res :string) => {
          console.log('Request successfull')
          console.log(res)
          this.pingMessage = res;
        })
      .catch((err: Error | AxiosError ) => {
      return Promise.reject(err);
    });
    },
  }
});
