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
	The main function computes the average dependability by checking all the different foresights with different number of clusters
	for the identified clustering algorithms [EM, HMM, k-means].

	'''
	algo_select = [['EM','em'],['HMM','hmm'],['KM','km']]
	cluster_size = np.asarray(([5, 6, 7, 8]))
	partition = ['50p', '60p', '70p', '80p']
	#partition_num = np.asarray(([200000, 240000, 280000, 320000]))
	partition_num = np.asarray((['50% ahead', '40% ahead', '30% ahead', '20% ahead']))
	flag = 0 
	error_list = np.zeros((len(partition),1), float)

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

	df_error[df_error.avg_dependability == df_error.avg_dependability.min()]

	min_list = df_error.groupby(['clustering_method']).avg_dependability.min()

	min_list_arr = min_list.to_numpy()


	min_list_arr =(1 - min_list_arr[:])

	df_error['avg_dependability'] = (1 - df_error['avg_dependability'])



	df_error.to_csv(r'/content/drive/My Drive/Paris_dataset/Metric_score_values/error_values.csv', index=False)

	df_min = df_error.loc[df_error['avg_dependability'].isin(min_list_arr)]

	df_min.to_csv(r'/content/drive/My Drive/Paris_dataset/Metric_score_values/min_error_values.csv', index=False)

	df_error.loc[df_error['avg_dependability'].isin(min_list_arr)]

	df_error.groupby(['clustering_method']).avg_dependability.mean()

	df_error.avg_dependability.mean()

if __name__ == '__main__':

	import pandas as pd
	import numpy as np
	
	#Define the main function
	main()
