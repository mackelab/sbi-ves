<template>
  <q-page>
    <edit-wrapper gridCss="col-12 col-xl-10 col-lg-10 col-md-10 q-px-lg">
      <div class="q-pa-md full-width justify-center">
        <q-stepper
          v-model="step"
          header-nav
          ref="stepper"
          color="primary"
          animated
        >
          <q-step
            :name="1"
            title="Upload your data"
            icon="cloud_upload"
            :done="step > 1 && uploadSuccessful"
            class="q-pa-md"
          >
            <q-card flat square class="overflow-auto q-mt-md">
              <q-item :clickable="false" class="text-h6 q-pa-md text-grey-10">
                <q-item-section>
                  Upload Measurements
                </q-item-section>
              </q-item>
              <q-card-section>
                <q-input
                  class="q-mt-md"
                  v-model="measurementStore.editMeasurement.location"
                  label="Location"
                />
                <q-input
                  class="q-mt-md"
                  v-model="measurementStore.editMeasurement.measurementDate"
                  label="Measurement Date"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy>
                        <q-date v-model="measurementStore.editMeasurement.measurementDate">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat/>
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>

                  </template>
                </q-input>

                <q-input
                  class="q-mt-md"
                  v-model="measurementStore.editMeasurement.comment"
                  label="Comment"
                />

                <q-file
                  cleareable
                  class="q-mt-md"
                  v-model="measurementStore.file"
                  label="Pick one file"
                  :disable="disableUpload"
                  color="primary"
                  accept=".csv, .json, .txt, .xls, .xlsx"
                >
                  <template v-if="measurementStore.file" v-slot:append>
                    <q-icon name="cancel" @click.stop.prevent="measurementStore.file = null" class="cursor-pointer"/>
                  </template>
                  <template v-else v-slot:append>
                    <q-icon name="description">
                    </q-icon>

                  </template>
                </q-file>
              </q-card-section>

              <q-card-actions class="q-mt-mb q-pa-md">
                <q-btn flat @click="upload" no-caps>

                  <q-icon left size="2em" name="cloud_upload"/>
                  <div>Upload Data</div>
                </q-btn>
              </q-card-actions>
            </q-card>

            <q-stepper-navigation>
              <q-btn @click="() => { step = 2 }" color="primary" label="Continue" :disable="!uploadSuccessful"
                     class="q-ml-md"/>
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="2"
            title="Polynomial depth profile"
            caption="Invert your Data"
            icon="counter_2"
            :done="isPolyImageLoaded"
            :header-nav="uploadSuccessful"
          >
            <q-card flat square class="overflow-auto q-mt-lg">
              <q-item :clickable="false" class="text-h6 q-pa-md text-grey-10">
                <q-item-section>
                  Polynomial Depth Profile
                </q-item-section>
              </q-item>

              <q-card-section class="flex items-center justify-center">
                <q-img v-if="isPolyImageLoaded" :src="measurementStore.imageUrlPoly" :ratio="16/12" fit="cover"
                       style="max-width: 1200px; max-height: 900px;" class="flex items-center justify-center"/>
                <div v-else-if="!isPolyImageLoaded && polyImageLoading" class="flex items-center justify-center">
                  <q-spinner-gears
                    color="primary"
                    size="3em"
                  />
                  <span> Your data is being inverted ...</span>
                  <q-tooltip :offset="[0, 8]">Your data is currently inverted</q-tooltip>
                </div>
              </q-card-section>

              <q-card-actions class="q-mt-mb flex items-center justify-center">
                <q-btn v-if="!(polyImageLoading || isPolyImageLoaded)" flat @click="invertPolynom" no-caps> Invert your
                  data
                </q-btn>
              </q-card-actions>
            </q-card>

            <q-stepper-navigation>
              <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm"/>
              <q-btn @click="() => { step = 3 }" color="primary" label="Continue"/>
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="3"
            title="Step depth profile"
            caption="Invert your Data"
            icon="stairs"
            :header-nav="uploadSuccessful"
            :done="isStepImageLoaded"
          >
            <q-card flat square class="overflow-auto q-mt-lg">
              <q-item :clickable="true" class="text-h6 q-pa-md text-grey-10">
                <q-item-section>
                  Step depth profile
                </q-item-section>
              </q-item>

              <q-card-section class="flex items-center justify-center">
                <q-img v-if="isStepImageLoaded" :src="measurementStore.imageUrlStep" :ratio="16/12" fit="cover"
                       style="max-width: 1200px; max-height: 900px;"/>
                <div v-else-if="!isStepImageLoaded && stepImageLoading">
                  <q-spinner-gears
                    color="primary"
                    size="3em"
                  />
                  <span> Your data is being inverted ...</span>
                  <q-tooltip :offset="[0, 8]">Your data is being inverted ...</q-tooltip>
                </div>
              </q-card-section>

              <q-card-actions class="q-mt-mb flex items-center justify-center">
                <q-btn v-if="!(stepImageLoading || isStepImageLoaded)" flat @click="invertStep" no-caps> Invert your
                  data
                </q-btn>
              </q-card-actions>
            </q-card>
            <q-stepper-navigation>
              <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm"/>
            </q-stepper-navigation>
          </q-step>
        </q-stepper>
      </div>


      <!--
      <q-card square class="overflow-auto q-mt-lg" v-show="showInversion">
        <q-card-section>
          <div class="text-h6">Inversion of VES Data</div>
          <div class="text-subtitle2">Invert the previously uploaded data</div>
        </q-card-section>

        <q-card-section v-show="!!measurementStore.imageUrl">
          <q-img :src="measurementStore.imageUrl" :ratio="16/12" fit="cover">
            <template v-slot:loading>
              <div class="text-subtitle1 text-white">
                Loading...
              </div>
            </template>
          </q-img>
        </q-card-section>

        <q-card-actions class="q-mt-mb">
          <q-btn flat @click="invert"> Invert Data</q-btn>
        </q-card-actions>
      </q-card>
      -->
    </edit-wrapper>
  </q-page>
</template>

<script setup lang="ts">

import EditWrapper from "components/EditWrapper.vue";
import {useMeasurementStore} from "stores/measurements";
import {computed, ref} from "vue";


const measurementStore = useMeasurementStore();
const disableUpload = ref(false);
const uploadSuccessful = ref(!!measurementStore.editMeasurement.id);
const polyImageLoading = ref(false);
const stepImageLoading = ref(false);
const step = ref(1)

const isPolyImageLoaded = computed(() => {
  return !!measurementStore.imageUrlPoly && !polyImageLoading.value
})
const isStepImageLoaded = computed(() => {
  return !!measurementStore.imageUrlStep && !stepImageLoading.value
})


async function upload() {
  await measurementStore.saveMeasurement()
    .then((success) => {
      if (success) {
        uploadSuccessful.value = true
        console.log('Measurement successfully uploaded')
      }
    })
}

async function invertPolynom() {
  polyImageLoading.value = true
  await measurementStore.invertData('polynom')
    .then((success) => {
      if (success) {
        polyImageLoading.value = false
        console.log('Measurement successfully inverted')
      }
    })
}

async function invertStep() {
  stepImageLoading.value = true
  await measurementStore.invertData('step')
    .then((success) => {
      if (success) {
        stepImageLoading.value = false
        console.log('Measurement successfully inverted')
      }
    })
}
</script>
<style lang="scss">

</style>
