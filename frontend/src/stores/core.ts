import {defineStore} from 'pinia';
import Bluebird from "bluebird";
import {AxiosError} from "axios";
import {clearUser, Credentials} from "src/models/models";
import {extend} from "quasar";
import {UserDto} from "src/models/user-dto";
import {parseJwt} from "src/utils/jwt-utils";
import {getUserById, loginUser, setJWT} from "stores/api";

export const useCoreStore = defineStore('core', {
  persist: true,

  state: () => ({
    user: extend<UserDto>(true, {}, clearUser),
    token: null as string | null,
    lastError: null as string | null,
    lastNotification: null as string | null,
    loginProcessActive: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isLoggedIn: (state) => !state.loginProcessActive && !!state.token && !!state.user,
  },
  actions: {
    apiSetup(): void {
      // set the token(s) from the persisted coreStore in the Axios API config and create Cookie(s) for the token(s)
      if (this.token) {
        this.setToken(this.token);
      }
    },

    async login(payload: Credentials): Promise<boolean> {
      this.loginProcessActive = true;
      return Bluebird.resolve(loginUser(payload))
        .then(async (token) => {
          console.log("token", token)
          if (token) {
            await this.afterLogin(token);

            // Finish login process
            this.loginProcessActive = false;
            return true;
          } else {
            console.log('No Token provided!!')
            this.loginProcessActive = false;
            return false;
          }
        })
        .catch((err: Error | AxiosError) => {
          this.loginProcessActive = false;
          return Promise.reject(err)
        });
    },


    async afterLogin(token: string): Promise<boolean> {
      // Set token in store, cookie, axios api, etc.
      this.setToken(token);

      // Parse token and set basic user details from token
      const parsedToken = parseJwt(token);
      console.log("parsedToken", parsedToken)
      this.user = <UserDto>{
        id: parsedToken.id,
        email: parsedToken.email,
        username: parsedToken.username
        // role: parsedToken.role,
      };

      // Load full User from backend
      await getUserById(parsedToken.id).then((userDto: UserDto) => {
        console.log("getUserById - userDto", userDto);
        this.user = userDto;
      });
      return Promise.resolve(true);
    },


    setToken(token: string) {
      // Set JWT token in store
      this.token = token;
      // Set JWT token in a token cookie
      //  https://quasar.dev/quasar-plugins/cookies
      // Cookies.set(this.cookie.name.jwt, token, this.cookie.config);
      // Set token in Axios API
      setJWT(token);
    },

  }
});
