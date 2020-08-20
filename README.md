# COVID-19 Risk Estimation
This repository contains the work conducted by Sedevizo Kielienyu for community risk estimation of COVID-19 under the supervision of Dr. Burak Kantarci. The project is inspired by the ubiquitous and non-dedicated nature of mobile sensors, where a suitable Mobile Crowdsensing (MCS) campaign is used to collect the mobility pattern of smart mobile device users (individuals who have opted to provide their sensory data to the MCS campaign). These individuals are called MCS participant or simply a user. Documentation of the Python codes are generated using Sphinx, and can be found under the 'Documentation' folder. The project uses CrowdSenSim <sup>1</sup>, a virtual crowdsensing environment to collect the mobility patterns of the MCS participants. Details regarding the simulation settings, clustering methods, input files and output files of the code are given below, along with the pre-requisites that is required for this project:

1. **Pre-requisites**:
  Programming Language: The baseline programming language is Python, which is used to create all the functions regarding the proposed COVID-19 risk estimation. For plotting the   graphs, MATLAB is used. 
  
    Python version: 3.8.4  
    MATLAB version: R2020a  
    CrowdSenSim version: 1.2.0
    Python libraries: Here, the libraries(modules) used for this project are listed.  
    &nbsp;&nbsp;&nbsp;a. pandas  
    &nbsp;&nbsp;&nbsp;b. numpy  
    &nbsp;&nbsp;&nbsp;c. hmmlearn  
    &nbsp;&nbsp;&nbsp;d. sklearm    
    &nbsp;&nbsp;&nbsp;e. time  
    
2. **Simulation Settings, Clustering parameters, other parameters**:  
  **CrowdSenSim**  
  Data collection framework: PCS (Piggyback Crowdsensing)    
  Time interval of the MCS campaign (min-max): 20 - 120 mins      
  Day(s) of simulation: 1  
  Number of users: 10000 (scenario 1), 30000 (scenario 2)  
  City: Paris (area: 105.4 km<sup>2</sup>  
  Selected travel time of each user: 41 mins (41 mins of travel time is selected from each user to define the travel distance, i.e., mobility pattern)  
  **Clustering parameters**  
  Clustering method: k-means, HMM (Hidden Markov Model), EM (Expected Maximization)
  Number of clusters: 5, 6, 7, 8    
  **Other parameters**  
  For estimating the risk scores of each cluster, a t% ahead mechanism is used where an estimation of future risk of a cluster is evaluated with (1-t)% of the time commitments of each user in the MCS campaign. The t% ahead mechanism is known as the 'Foresight' in this risk study.   
  Foresight: 20% - 50%  
  20% ahead means 80% of the mobility pattern of each user. Likewise, 50% means 50% of the mobility pattern of each user.
3. **Raw Data**:
  The raw data (mobility pattern), obtained from the simulator, contains 7 features defined by the tuple <UserID, Latitude, Longitude, Altitude, Day, Hour, Min>. The mobility pattern can be found in each of two sub-folders under 'Raw Data' folder, representing the two scenarios. Each folder is labelled by 'City-Users-Day'. Here is a snippet of the raw data.
<img src="images/raw_data.png" width=800>

4. **Output files**:
  All the output files are stored in the 'Output' folder. The raw data is cleaned using Microsoft Excel, where all the null values in each cell is replaced with 0. Since 'Altitude' feature is not required to determine the geo-location of a user, it can be discarded. Following a feature selection method, 'Day' feature is also discarded. The final tuple becomes <UserID, Latitude, Longitude, Hour, Min, Sec>.  
  
    Details of the output files:
    &nbsp;&nbsp;&nbsp;1. UserMovementListEvents_0_'Users'.csv: This file represents the cleaned version of the raw mobility data from the result of replacing null values and feature selection. 'Users' in the file name can be either 10000 or 30000. 
    &nbsp;&nbsp;&nbsp;2.  
  
  

