import {AxiosError} from 'axios';
import {api} from 'boot/axios';
import {Credentials} from "src/models/models";
import {UserDto} from "src/models/user-dto";
import {RegisterUserDto} from "src/models/register-user-dto";
import {MeasurementDto} from "src/models/measurement-dto";


// --- Base functions --------------------------------------------------------------------------------------------------

export function setJWT(jwt: string) {
  ((api.defaults.headers.common)['Authorization'] as string) = `Bearer ${jwt}`;
}

export function clearJWT() {
  delete (api.defaults.headers as never)['common']['Authorization'];
}

// --- Auth ------------------------------------------------------------------------------------------------------------
export async function loginUser(credentials: Credentials): Promise<string> {
  return api
    .post('/auth/login', {
      ...credentials,
    })
    .then((res) => {
      console.log('res', res)
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      // TODO: better to send token as header in the response -> send token in header in the backend
      //return res.headers.authorization as string;
      return res.data['token']
    })
    .catch((err: Error | AxiosError) => {
      return Promise.reject(err)
    })
}


// --- User ------------------------------------------------------------------------------------------------------------

export async function getUserById(userId: string): Promise<UserDto> {
  return api.get(`/users/${userId}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}

export async function getUsers(): Promise<UserDto[]> {
  return api.get('/users')
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}


export async function postUser(userDto: UserDto) {
  return api
    .post('/users', userDto)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}

// --- Registration ---- -----------------------------------------------------------------------------------------------
export async function registerUser(registerUserDto: RegisterUserDto) {
  return api.post('/register', registerUserDto)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}


// --- Measurements ----------------------------------------------------------------------------------------------------

export async function postMeasurement(measurementDto: MeasurementDto, file: File) {
  const formData = new FormData();
  formData.append('file', file, file.name);
  formData.append('measurement', JSON.stringify(measurementDto));

  return api
    .post('/measurements', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}


export async function invertMeasurement(measurementId: string, modelType: string) {
  return api.get(`/measurements/${measurementId}/inversion/${modelType}`, {responseType: 'blob'})
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      return err;
    })
}
