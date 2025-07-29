# Appendices

## Prompts used for PHY

Here we show the initial prompts given to the LLM for each of the sub-tasks in the PHY problem. This is provided at the start of each InteractCode session for each sub-task. The function-description given to the InteractCode procedure is a combination of the task description and the sub-task specification combined in this manner:

- "*task_description *+ While the whole task description is given above, in this current session let us focus only on the users given sub-task:* sub-task_specification*".

We describe below the task description given for the PHY problem, 
followed by each session specification which consists of the sub-task 
specification, pre-condition and the post-condition. This prompt is used 
at the start of the InteractCode session for that sub-task and is 
followed by messages exchanged between the human and machine with 
message-tags by the interaction model described in 
section II A (Generating Human-Ratified Code for a Function) of the main paper.

**Task Description:**
Title: Predicting star formation properties. Background: The ultimate goal is to determine a few output parameters such as the current star formation rate, the stellar mass, dust mass. The input dataset located at 'data/filtered_galaxies.csv' consists of 22 input parameters and 3 output parameters. The data columns are: ['FUV_flux', 'NUV_flux', 'u_flux', 'g_flux', 'r_flux', 'i_flux', 'z_flux', 'X_flux', 'Y_flux', 'J_flux', 'H_flux', 'K_flux', 'W1_flux', 'W2_flux', 'W3_flux', 'W4_flux', 'P100_flux', 'P160_flux', 'S250_flux', 'S350_flux', 'S500_flux', 'Z', 'SFR_0_1Gyr_percentile50', 'L_dust_percentile50', 'mass_stellar_percentile50']. The three output parameters that need to be predicted are: 'SFR_0_1Gyr_percentile50', 'L_dust_percentile50', 'mass_stellar_percentile50'. What needs to be done: Use the flux measurements (inputs) to predict the outputs ('SFR_0_1Gyr_percentile50', 'L_dust_percentile50', 'mass_stellar_percentile50'. For evaluating the results, use a custom error metric: `error = σ(y_actual-y_predicted)` Expected output: ML model(s) that can predict the star formation properties with minimal error.

**Session 1: Perform exploratory data analysis**  
Description: load data and do exploratory data analysis.  
Pre-condition: data/filtered_galaxies.csv  
Post-condition: graphs plotted and better understanding of the data. Data loaded as df.

**Session 2: Feature engineering**  
Description: Feature engineering. Normalise the data by removing the mean and scaling to unit variance. Split the data into training and test sets.  
Pre-condition: the data is loaded in the variable df  
Post-condition: Normalised train and test data to be given to ML model to train.

**Session 3: Train ML models**  
Description: Train a ML/AI model to predict the three output parameters. I leave it upto you based on your expertise in astrophysics and machine learning, whether to build a single model to predict all the three parameters or to build separate models for each. I need a model that will result in the least RMSE and the custom error given. Monitor the time taken to train the models for each output parameters. Save the model in a format that can be loaded again easily to compute various evaluation parameters. Save the predicted values and the actual values in a csv file for each of the three output parameters.  
Pre-condition: x_train, y_train, x_test, y_test datasets are available.  
Post-condition: Model trained and saved. Predicted and actual values saved.

**Session 4: Reporting on evaluation metric and validation plots**  
Description: Load the file with actual and predicted values saved. Evaluate the predictions with the actual values and report the metric. Report on the custom error, root mean square error, mean absolute deviation, r2 adjusted. Create plots of actual vs predicted values. Make the plot look sophisticated and professional.  
Pre-condition: actual and predicted values are stored as 'y_test,y_pred' in: f'{output}_actual_vs_predicted.csv' for outputs = ['SFR_0_1Gyr_percentile50', 'L_dust_percentile50', 'mass_stellar_percentile50'].  
Post-condition: evaluation metric reported and saved on the custom error metric. Plots created and saved.
