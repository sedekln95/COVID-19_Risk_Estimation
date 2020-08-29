"""
	Community Risk Factor
	.....................
	This python code calculates the community risk factor based on the individuals' risk scores in each community. 
	Community is defined as the different spatio-temporal instances of unique users that are clustered based on the 
	projected future movements of these participants. Community and cluster are used interchangeably.
"""

def summationUser(df):
	'''
	This function takes the summation of all the contact list of unique users based on their ID's and cluster labels.
	Eg: User ID = 1 belongs to cluster label = 5, and this user has 10 instances in that cluster. The function will take the summation of the contact 
	list for all the 10 instances of user ID  = 1 in cluster 5.

	:param name: mobility data and their corresponding cluster labels

	:param type: dataframe

	:returns: the summation of contact list of every instance of user i in cluster c

	:return type: numpy array 
	'''
	sumSeries = df.groupby(['UserID','label']).contact_list.sum()
	df_new = sumSeries.to_frame('contact_list_summation')
	df_new = df_new.reset_index()
	arrSum = df_new.values
	return arrSum

def globalMax(arrSum):
	'''
	This function gives the maximum summation value of contact list across all unique users.
	
	:param name: summation of contact list of all users across M clusters

	:param type: numpy array

	:return: the maximum summation value of contact list from an instance of user i across the N users

	:return type: integer
	'''
	return np.max(arrSum[:,2])

def riskFactorUser(arrSum, global_max, riskList):
	'''
	This function computes the risk factor of each instance of a user in cluster c.

	:param name: summation of contact list of all users across M clusters, maximum summation value of contact list across all users

	:param type: numpy array (summation), integer (maximum summation value) 

	:return: risk factor of all users in clusters c
			 
	:return type: numpy array 

	'''
	for i in range(len(riskList)):
		riskList[i][0] = arrSum[i][0]
		riskList[i][1] = arrSum[i][1]
		riskList[i][2] = (arrSum[i][2]/global_max)

def riskListDataframe(riskList):
	'''
	This function creates a dataframe for the risk factor of users.
	
	:param name: risk factor of users

	:param type: numpy array

	:return: risk factor of users in a dataframe

	:return type: dataframe
	'''
	df = pd.DataFrame(riskList,index=None, columns=['UserID','label','risk_factor'])
	df = df.astype({'UserID' : int, 'label' : int})
	return df

def maxRiskFactor(df_risk):

	'''
	This function gets the maximum risk factor of a user across all clusters.

	:param name: risk factor of users

	:param type: dataframe

	:return: the maximum risk factor of an instance of a user across all the M clusters

	:return: numpy array

	'''
	maxSeries = df_risk.groupby(['label']).risk_factor.max()
	df_new = maxSeries.to_frame('max_risk_factor')
	df_new = df_new.reset_index()
	arrMax = df_new.values
	return arrMax

def standardDeviation(df_risk):
	'''
	This function computes the standard deviation of risk factors in M clusters.

	:param name: risk factor of users

	:param type: dataframe

	:return: standard deviation of risk factors in M clusters

	:return type: numpy array
	'''
	stand_devList = df_risk.groupby('label').risk_factor.std()
	df_new = stand_devList.to_frame('standard_deviation_risk_factor')
	df_new = df_new.reset_index()
	arrstd = df_new.values
	return arrstd

def riskFactorCluster(user_count, df_risk, n_cluster):  
	'''
	This function computes the cluster risk factor which is the summation of the risk factors of all users in cluster c and divided by the number of 
	unique users in that cluster. Please do not be confused with the notations 'risk factor of a cluster' and 'risk factor of user'. 

	:param name: number of unique users in cluster c, risk factor of users in cluster c, number of clusters

	:param type: integer (user count, number of clusters), dataframe (users' risk factor)

	:return: the risk factor of each cluster

	:return type: numpy array
	'''
	rf_cluster = np.zeros((n_cluster,1),float)
	rf_sumlist = df_risk.groupby('label').risk_factor.sum()
	df_new = rf_sumlist.to_frame('risk_factor_summation')
	df_new = df_new.reset_index()
	arrSum = df_new.values
	print('The length of risk factor summation is', len(arrSum))
	for i in range(n_cluster):
		rf_cluster[i] = (arrSum[i][1]/user_count[i])
		print('risk factor of cluster', i,'is',rf_cluster[i])
		print('summation of risk factors in cluster', i, 'is',arrSum[i][1])
		print('user count is', user_count[i])
	return rf_cluster

def max_riskFactor_dataframe(max_rf_kcluster):
	'''
	This function creates a dataframe for the maximum risk factor in each cluster. 
	
	:param name: maximum risk factor of a user in all clusters

	:param type: numpy array

	:return: dataframe format of maximum risk factor of a user in all clusters

	:return type: dataframe
	'''
	df = pd.DataFrame(max_rf_kcluster, index=None, columns=['label','max_risk_factor'])
	df = df.astype({'label' : int})
	return df

def std_dataframe(std_arr_cluster):
	'''
	This function creates a dataframe for the standard deviation of the risk factors of user in each cluster.

	:param name: standard deviation of users in each cluster

	:param type: dataframe

	:return: dataframe format of the standard deviation

	:return type: dataframe
	'''
	df = pd.DataFrame(std_arr_cluster, index=None, columns=['label','std_risk_factor'])
	df = df.astype({'label' : int})
	return df

def rf_cluster_dataframe(rf_cluster):
	'''
	This function creates a dataframe for the risk factor of clusters (i.e., cluster risk factor).

	:param name: M cluster risk factor

	:param type: numpy array

	:return: dataframe format of the cluster risk factor

	:return type: dataframe
	'''
	df = pd.DataFrame(rf_cluster, index=None, columns=['risk_factor_cluster'])
	return df

def df_to_csv(df_risk, df_max_rf, df_std, df_cluster_rf):

	'''
	This function exports the dataframe format of users' risk factor, maximum risk factor across all clusters, standard deviation of risk
	factor in each cluster, clusters' risk factor to csv files

	:param name: users' risk factor, max risk factor in each cluster, standard deviation of risk factors in each cluster, clusters' risk factor

	:param type: dataframe (for all the parameters)

	:return: equivalent csv files for the dataframe passed in the argument

	:return type: csv
	'''
	df_risk.to_csv(r'./Output/risk_factor_8_100p_km.csv',index=None)
	df_max_rf.to_csv(r'./Output/max_risk_factor_8_100p_km.csv',index=None)
	df_std.to_csv(r'./Output/std_riskfactor_8_100p_km.csv',index=None)
	df_cluster_rf.to_csv(r'./Output/cluster_riskfactor_8_100p_km.csv',index=None)


if __name__ == '__main__':
	import time 
	import numpy as np
	import pandas as pd
  
	#Define the start time of the execution
	start_time = time.time()
	labels = [5, 6, 7, 8]

	#Import the csv file that contains the geo-location and contact list of every instance of a user
	df_ins = pd.read_csv('./Output/merged_list_ins_cl_8_100p_km.csv')

	'''Sort the data set in the ascending order of cluster labels. 
	This is to group all the instances belonging to the same cluster after each consecutive row'''
	df_res = df_ins.sort_values(by=['label'],ignore_index=True)

	#Read the number of unqiue users for each cluster
	df_usercount = pd.read_csv('./Output/user_count_8_100p_km.csv')

	user_count = df_usercount.values
	user_count = user_count.flatten()

	#Calling the functions to compute the risk factor of clusters
	arrSum = summationUser(df_res)
	globalmax_rf = globalMax(arrSum)
	riskList = np.zeros((len(arrSum),3), float)
	riskFactorUser(arrSum, globalmax_rf, riskList)
	risklist_df = riskListDataframe(riskList)

	'''Creating array for statistical comparisons'''
	max_rf_kcluster = maxRiskFactor(risklist_df)
	std_arr_cluster = standardDeviation(risklist_df)

	'''Dont forget to change the label array with each execution'''
	
	rf_cluster = riskFactorCluster(user_count, risklist_df, 8)

	'''Creating dataframe for the last three values'''
	df_max_rf = max_riskFactor_dataframe(max_rf_kcluster)
	df_std = std_dataframe(std_arr_cluster)
	df_cluster_rf = rf_cluster_dataframe(rf_cluster)

	'''Saving all the dataframe to respective locations'''
	df_to_csv(risklist_df, df_max_rf, df_std, df_cluster_rf)

	print('The length of risk factors of clusters is', len(df_cluster_rf), 'and the instances were', len(df_ins))