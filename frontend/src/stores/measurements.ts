import {defineStore} from "pinia";
import {extend} from "quasar";
import {MeasurementDto} from "src/models/measurement-dto";
import {clearInversion, clearMeasurement} from "src/models/models";
import Bluebird from "bluebird";
import {AxiosError} from "axios";
import {useCoreStore} from "stores/core";
import {invertMeasurement, postMeasurement} from "stores/api";
import {InversionDto} from "src/models/inversion-dto";


export const useMeasurementStore = defineStore('measurement', {
  state: () => ({
    editMeasurement: extend<MeasurementDto>(true, {}, clearMeasurement),
    file: null as File | null,
    inversion: extend<InversionDto>(true, {}, clearInversion),
    imageUrlPoly: '' as string,
    imageUrlStep: '' as string
  }),
  getters: {},
  actions: {
    async saveMeasurement() {
      const coreStore = useCoreStore();
      if (coreStore.user.id) {
        this.editMeasurement.userId = coreStore.user.id;
      }
      if (!!this.file) {
        return Bluebird.resolve(postMeasurement(this.editMeasurement, this.file))
          .then((res: MeasurementDto) => {
            console.log('Request successful - Save measurement')
            console.log(res)
            this.editMeasurement = res;
            return res;
          })
          .catch((err: Error | AxiosError) => {
            return Promise.reject(err)
          })
      }
    },

    async invertData(modelType: string) {
      const measurementId = !!this.editMeasurement.id ? this.editMeasurement.id : '11010b8a-01d9-467f-a7f9-93dd66ec0ef5'
      return Bluebird.resolve(invertMeasurement(measurementId, modelType))
        .then((res: Blob) => {
          if (modelType === 'polynom') {
            this.imageUrlPoly = URL.createObjectURL(res);
          } else if (modelType == 'step') {
            this.imageUrlStep = URL.createObjectURL(res);
          } else {
            console.log('Model type not found')
          }
          return res;
        })
        .catch((err: Error | AxiosError) => {
          return Promise.reject(err)
        })
    }


  }

});
