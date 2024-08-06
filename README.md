# Simulation-Based Inference of Soil Resistivity from Vertical Electrical Sounding

Master thesis project on a probabilistic approach towards inversion of vertical electrical sounding with SBI.
Four probabilistic models were trained on simulations from different prior distributions.
They were designed to address shortcomings of classical deterministic inversion methods for VES, that do not provide
uncertainty estimation or support for gradual soil transitions.
By utilizing SBI for inversion of VES, I am capable to porridge uncertainty estimation, amortization over simulation and
training costs and incorporate soil characteristics into the inversion process.
The models are trained and evaluated in the sbi-ves directory.


<img src="final figures/experimental setup.png" style="zoom: 80%;" />



In addition, I have developed a web application called VESBI, that hosts the models and provides a user-friendly,
standardized and centralized approach towards inversion of VES data.
Due to the scope of the thesis, this web application is not fully mature and needs further development to exploit the
full potential it has. However, I was able to implement a web-based inversion tool employing the pre-trained neural
networks and with this a solid foundation on which further development can be based on,

This repository contains both the web-application and the analysis part.
The repository is structured in the following way:

- **sbi-ves**

  On the top level, there are the notebooks to reproduce the results and the figures I've created in the course of this
  project.
    - Step Model.ipynb, Polynomial Model.ipynb, Block Model.ipynb and Independent Step.ipynb are the notebooks used to
      generate the simulated data and train the models that were used in this study. For each model the Simulation Based
      Calibration was executed in those notebooks.
    - Prior Distributions.ipynb generates the prior plot in the methods section and shows prior samples for each of the
      four prior distributions on which the notebooks were trained.
    - RMSE analysis.ipynb generates the synthetic ground truths and evaluates them under each of the posterior networks
      to generate the RMSE values for each of the GT samples.
    - Synthetic Test Case.ipynb recreates the plots that shows a GT sample which is inferred by each of the posteriors
      and combines them into one final plot
    - RMSE analysis pygimli.ipynb calculates the RMSE values for the deterministic models on the same GT samples.
    - Real Data Analysis.ipynb generates the plot of the for the real observation that was confirmed by drilling. And
      computes the RMSE values for each of the models.
      Sediment Core.iypnb creates the plot for the sediment core.
    - forward.py and survey.py are two classes with which the SimPEG implementation used for the forward simulations can
      be initialised.
    - polynomials.py contains some helper functions for the polynomial model
    - utils.py, block_utils.py and pygimli_utils.py contain helper functions, that were used to visualize and convert
      the data to generate the plots.
    - config contains some config data, but mainly colors.
    - pygimliInvers.py contains functionality to carry out inversion of VES with pygimli
    - PygimliInversion.ipynb inverts the synthetic prior samples and the real VES data to obtain deterministic inversion
      results


- **frontend**
    - Quasar Frontend structure in which the frontend implementation is defined for the VESBI web app.
    - The Frontend can be started via the command `npm run dev` in the frontend directory.

- **backend**

    - Flask Backend Structure, that contains sql scripts to create the tables and test data
    - api contains the backend functionality which is structured in models (defining the entities and dtos), services
      and routes, that define the endpoints and the functionality.
    - the backend can be started via the command `flask run` in the backend directory.

## Results

Visual representation of the inference results of the four models on synthetic test data in comparison to classical
deterministic inversion approaches.

<img src="final figures/synth_data_gt_step_all_posteriors.png" style="zoom: 80%;" />

### Some of the main results were:

- Probabilistic models are capable to meet and outperform deterministic models.
- However, their accuracy depends on the prior distribution on which the models were trained, and the test instances on
  which tey were tested.
- The non-uniqueness of the forward model has been demonstrated and confirmed through the variety of depth profiles from
  multiple models that fit the observation equally well. This underlines the benefit of uncertainty quantification for
  inversion of VES.
- Characteristics of soil types and transitions can be incorporated into the inference process via the prior
  distribution and are clearly reflected in the inferred depth profiles.
- A web application as initiated within this project, has the potential to fully exploit the advantages of this
  probabilistic approach towards inversion. It has the potential to develop towards a platform for inversion across
  geophysical disciplines. 




