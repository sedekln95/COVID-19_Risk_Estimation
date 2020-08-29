"""
	Expected Maximization (EM) Clustering
	.....................................
	Applies EM Clustering to the tsne 2D vector of the mobility pattern. Based on the nature of the data,
	clustering is done on predicting the future mobility pattern of each user.

	The number of cluster is set to 5, 6, 7, 8.

"""
def em_clust(dataframe):

	"""
	Performs EM clustering on the equivalent tsne data (2D vector) representation of the mobility pattern.

	:param name: tsne 2D vector of mobility data, frequency of different mobility instances in all the clusters, i.e., how many instances a particular cluster has

	:param type: dataframe (tsne 2D vector), numpy array (frequency)

	:return: cluster labels

	:return type: dataframe
	"""

	df = dataframe
	#Define the start time of the clustering execution
	start_time = time.time()

	#Define the parameters of the EM model and train it. Change the number of clusters (n_components) after each successful execution
	gaussmix = GaussianMixture(n_components=8, max_iter = 500)
	gaussmix.fit(df)
	end = time.time() - start_time
	print('The execution time is %s seconds' %end)

	#Compute the cluster labels
	labels = gaussmix.predict(df)

	#Checking how many mobility instances have fallen into the different clusters 
	(unique, counts) = np.unique(labels, return_counts=True)
	frequencies = np.asarray((unique, counts)).T

	#Export the cluster labels as a dataframe
	df_lab = pd.DataFrame(labels, index=None, columns=['label'])
	print(len(labels))

	return df_lab

if __name__ == '__main__':
	import numpy as np
	import pandas as pd
	from sklearn.mixture import GaussianMixture
	import time

	#Import the equivalent tsne data of the mobility pattern
	df = pd.read_csv('./Output/tsne_10k_50p.csv')

	#Apply k-means to the imported data. The function returns the cluster labels. 
	df_label = em_clust(df) 

	#Export the dataframe as a csv file
	df_label.to_csv(r'./Output/labels_10k_50p_em.csv', index=False)