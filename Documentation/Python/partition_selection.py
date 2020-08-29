""" 
	Dependability
	.............
	The risk factor prediction by taking the absolute difference between the actual risk factor and predicted risk factor 
	(at t% ahead foresight) of clusters is defined as dependability of the prediction. 
	
	Average dependability is the average of the absolute difference between actual-predicted risk scores of clusters.

	Maximum dependability is the minimum absolute difference in the actual-predicted risk score of a cluster. 
"""
def main():
	'''
	This function computes the average dependability for different values of M clusters (M = [5,6,7,8]) with their respective
	foresight values (20%-50% ahead), and clustering algorithms.

	Eg: Cluster M = 6, i.e., 6 clusters. Therefore for 6 clusters, we evaluate the average dependability for the 6 clusters at different 
	foresights in all the three clustering algorithms (HMM, k-means, EM). 

	:param name: summation of the absolute difference between the actual risk factor and predicted risk factor, number of clusters
	
	:param type: floating point (summation value), numpy array (num of clusters)

	:return: the average dependability

	:return type: dataframe
	'''
	algo_select = [['EM','em'],['HMM','hmm'],['KM','km']]
	cluster_size = np.asarray(([5, 6, 7, 8]))
	partition = ['50p', '60p', '70p', '80p']
	partition_num = np.asarray((['50% ahead', '40% ahead', '30% ahead', '20% ahead']))
	flag = 0 
	error_list = np.zeros((len(partition),1), float)

	'''
	The following for loop computes the average dependabililty across all foresights values, different num of clusters, and their respective clustering algo.
	Please note that the file path should be changed based on where the input files are. So, 'file_part' and 'file_main' should be changed 
	accordingly to the respective file directory of input files. Similarly, the file path in 'df_main' and 'df_path' should also be changed.
	This file path change applies to every line of code where an input file is read/imported.
	'''
	for i in range(len(algo_select)):
		for j in range(len(cluster_size)):
			for k in range(len(partition)):
				file_part = str(algo_select[i][0]) + '/cluster_' + str(cluster_size[j]) + '_' + str(partition[k]) + '_' + str(algo_select[i][1]) + '/cluster_riskfactor_' + str(cluster_size[j]) + '_' + str(partition[k]) + '_' + str(algo_select[i][1])
				file_main = str(algo_select[i][0]) + '/cluster_' + str(cluster_size[j]) + '_100p_' + str(algo_select[i][1]) + '/cluster_riskfactor_' + str(cluster_size[j]) + '_100p_' + str(algo_select[i][1])
				df_part = pd.read_csv('/content/drive/My Drive/Paris_dataset/' + file_part + '.csv')
				df_main = pd.read_csv('/content/drive/My Drive/Paris_dataset/' + file_main + '.csv')
				diff_list = abs(df_part['risk_factor_cluster'] - df_main['risk_factor_cluster'])
				sum_diff = sum(diff_list)
				error_list[k] = sum_diff/cluster_size[j]
			algo_name = [[algo_select[i][0]]*1]*len(partition)
			cluster = np.asarray([cluster_size[j]]*len(partition))
			if flag == 0:
				df_error = pd.DataFrame(np.column_stack([error_list.reshape(-1,1), cluster.reshape(-1,1), algo_name, partition_num.reshape(-1,1)]), index=None)
				df_error.columns = ['avg_dependability', 'no_of_communities', 'clustering_method', 'foresight']
				flag = 1
				print('Error dataframe created\n')
			else:
				df_concat = pd.DataFrame(np.column_stack([error_list.reshape(-1,1), cluster.reshape(-1,1), algo_name, partition_num.reshape(-1,1)]), index=None)
				df_concat.columns = ['avg_dependability', 'no_of_communities', 'clustering_method', 'foresight']
				df_error = pd.concat((df_error,df_concat),axis=0,ignore_index=True)
				print('Error dataframe concatenated\n')

	df_error[['avg_dependability']] = df_error[['avg_dependability']].astype('float')
	df_error[['no_of_communities']] = df_error[['no_of_communities']].astype('int')

	#Scaling the average dependability between 0 and 1
	df_error['avg_dependability'] = (1 - df_error['avg_dependability'])

	return df_error

def maxAvgDependability(df_error):
	'''
	This function gives the maximum average dependability at a particular foresight value with M communities in their respective clustering methods, 
	namely, Hidden Markov Model, k-means, and Expectation Maximization.

	:param name: average dependability

	:param type: dataframe

	:return: maximum average dependabilty in all the three clustering methods

	:return type: dataframe
	'''	
	max_list = df_error.groupby(['clustering_method']).avg_dependability.max()
	max_list_arr = min_list.to_numpy()
	#min_list_arr =(1 - min_list_arr[:])

	df_max = df_error.loc[df_error['avg_dependability'].isin(max_list_arr)]

	return df_max

def maxDependability(df_max_avg_dependability):
	
	'''
	This function retrieves the maximum dependability from a particular community at a specific foresight value, whose average with other
	communities at the same foresight is the global maximum average dependability.

	:param name: maximum average dependability  
	
	:param type: dataframe

	:return: maximum dependability at t% ahead foresight for community/cluster c

	:return type:	dataframe
	'''

	#Getting the maximum average dependabilty
	df_max_dep = df_max_avg_dependability.loc[df_max_avg_dependability['avg_dependability'] == df_max_avg_dependability['avg_dependability'].max()]
	df_max_dep = df_max_dep.reset_index(drop=True)
	dep_arr = df_max_dep.values


	comm = df_max_dep.no_of_communities[0]
	clust_method = df_max_dep.clustering_method[0].lower()
	clustU = clust_method.upper()
	fores = df_max_dep.foresight[0]
	foresight = fores

	fores = 100 - int(fores[:2])
	fores = str(fores)+'p'

	'''Getting the file path of actual-predicted risk factor based on identifying the clustering method which has the 
	maximum avg dependability.'''
	file_part = clustU + '/cluster_' + str(comm) + '_' + fores + '_' + clust_method + '/cluster_riskfactor_' + str(comm) + '_' + fores + '_' + clust_method
	file_main = clustU + '/cluster_' + str(comm) + '_' + '100p' + '_' + clust_method + '/cluster_riskfactor_' + str(comm) + '_' + '100p' + '_' + clust_method

	#Reading/importing the csv files
	df_part = pd.read_csv('/content/drive/My Drive/Paris_dataset/' + file_part + '.csv')
	df_main = pd.read_csv('/content/drive/My Drive/Paris_dataset/' + file_main + '.csv')

	#Minimum risk estimation error
	abs_diff = min(abs(df_part.risk_factor_cluster-df_main.risk_factor_cluster))

	#row indices
	ind = np.arange(1, int(comm)+1)

	#Getting the risk estimation error for the m communities from the identified clustering method with the max avg dependability
	error = abs(df_part.risk_factor_cluster-df_main.risk_factor_cluster)
	error = error.to_numpy()
	error = error.reshape(-1,1)

	#Creating the dataframe
	df_diff = pd.DataFrame(error, index=[ind], columns=['risk_estimation'])
	df_diff = df_diff.reset_index(drop=False)
	df_diff.columns = ['community', 'risk_estimation']

	df_max = df_diff.loc[df_diff.risk_estimation == abs_diff]
	df_max  = df_max.reset_index(drop=True)

	#Scaling the dependability value to 0 - 1
	max_dep = 1 - df_max.risk_estimation


	df_max['dependability'] = max_dep
	df_max['clustering method'] = clustU
	df_max['foresight'] = foresight

	return df_max

if __name__ == '__main__':  
	import pandas as pd
	import numpy as np
	
	'''Define the main function which will compute the risk estimation error for between the actual and predicted risk factors
	at different communities.'''
	df_error = main()

	#Export the dataframe as a csv file
	df_error.to_csv(r'./Output/error_values.csv', index=False)

	'''Call the functin maxAvgDependability which gives the maximum average dependability from the identified clustering methods at a 
	particular foresight with M communities/clusters'''
	df_max_avg_dependability = maxAvgDependability(df_error)

	#Export the dataframe as a csv file
	df_max_avg_dependability.to_csv(r'./Output/min_error_values.csv', index=False)

	#Calculate the maximum dependability from the maximum average dependability 
	df_max_depependability  = maxDependability(df_max_avg_dependability)

	#Export the dataframe as a csv file
	df_max_depependability.to_csv(r'./Output/max_dependability.csv', index=False)