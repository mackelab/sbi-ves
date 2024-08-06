import {UserDto} from "src/models/user-dto";
import {MeasurementDto} from "src/models/measurement-dto";
import {RegisterUserDto} from "src/models/register-user-dto";
import {InversionDto} from "src/models/inversion-dto";


export interface Credentials {
  username: string;
  password: string;
}

export const clearUser: UserDto = {
  id: null,
  firstName: '',
  lastName: '',
  institution: '',
  username: '',
  email: '',
  password: ''
};


export const clearRegisterUser: RegisterUserDto = {
  id: null,
  firstName: '',
  lastName: '',
  institution: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
};


export const clearMeasurement: MeasurementDto = {
  id: null,
  userId: '',
  location: null,
  measurementDate: null,
  comment: null
}

export const clearInversion: InversionDto = {
  id: null,
  measurementId: undefined,
  location: null
}
