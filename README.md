# Group 9: Explaining Distribution Shifts

Hey this is the repository for our project: Explaining Distribution Shifts.
If you have any questions or problems running the code, please reach out to us!

# Code for our Project


To recreate the results of the experiments, first create the corresponding environment (via conda by `conda env create -f environment.yml`).

We condoned 3 experiments in our project. You can find them in the Shift_Explanation, NBA_Data_Analysis and NBA_Data_Analysis_3_Vars folders. You will find all the results for our experiments. 
If you want to create new results with different parameters please refer to following instructions:

Simulated Logistics data:
For the simulated logistic data you need to run the run_experiment.py in the Shift_Explanation folder.
To adjust the parameters you need to change the chosen chosen_simulation_parameters within the module.
After you run the programm you will find your new results in the Results_Experiments folder.

NBA Experiments:

To run the code for the NBA Data experiments you simply need to run the run_nba_experiment.py in the NBA_Data_Analysis (NBA_Data_Analyis_3_Vars) folder. You will be asked to select the features you split the data on over the console.

PLEASE NOTE: We tested this code in Visual Studio Code. 

