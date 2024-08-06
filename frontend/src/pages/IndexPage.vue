<template>
  <q-page class="col-xs-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
    <q-card flat full-width>
      <q-card-section class="q-mt-xl">
        <div class="text-h4 text-center"> Welcome to the VESBI Web Application!</div>
      </q-card-section>
      <q-card-section>
        <div class="content-container">
          VESBI is a web application developed as part of a Master's thesis at the University of Tübingen in
          collaboration with the Geophysics group (Prof. Dr. Reinhard Drews) and Machine Learning in Science (Prof. Dr.
          Jakob Macke).
          This application is designed to provide a probabilistic approach for
          analysis of geoelectric measurement data, by inverting <strong>Vertical Electrical Sounding (VES)</strong>
          with <strong>Simulation-based Inference (SBI)</strong>. VESBI offers a user friendly platform for
          geophysicists and
          researchers to
          invert their VES data.
        </div>
        <div class="q-pt-lg q-mt-lg content-container">
          <strong>Key Features:</strong>
          <ul>
            <li>Data Upload: Upload geoelectric measurement data from Vertical Electrical
              Sounding with a Schlumberger survey configuration in .csv, .xls or .xlsx format.
            </li>
            <li>Probabilistic Inversion: We provide two pretrained posterior networks. The models were trained on
              simulations of different prior distributions to define the soil resistivity profile.
              The first network uses Legendre Polynomials of degree 5 and the second network uses a spatially
              regularized
              step prior to represent the resistivity depth profile.
            </li>
            <li>
              Soon: Data Download including the trained posterior networks for further custom analysis.
            </li>
          </ul>
        </div>

      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">

defineOptions({
  name: 'IndexPage'
});

</script>
<style scoped>
.content-container {
  max-width: 80%;
  margin: auto;
  text-align: left;
  font-size: large;
}
</style>
