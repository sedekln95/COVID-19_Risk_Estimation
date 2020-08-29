"""
	Hidden Markov Model (HMM) Clustering
	....................................
	Applies HMM Clustering to the tsne 2D vector of the mobility pattern. Based on the nature of the data,
	clustering is done on predicting the future mobility pattern of each user.

	The number of cluster is set to 5, 6, 7, 8.
"""

def hmm_learn(dataframe):

	"""
	This function applies HMM clustering to the equivalent tsne 2D vector of the mobility data.

	:param name: tsne 2D vector of mobility data

	:param type: dataframe (tsne 2D vector)

	:return: cluster labels

	:return type: dataframe
	"""

	df = dataframe
	#Define the start time of the execution time
	start_time = time.time() 
	
	#Define the parameters of the HMM model and train it. Change the number of clusters (n_components) after each successful execution. 
	model = hmm.GaussianHMM(n_components=8, n_iter=500)
	model.fit(df)
	end = time.time()-start_time
	print('The execution time is %s seconds' % end)

	#Compute the cluster labels
	labels = model.predict(df)

	#Export the labels as a dataframe
	df_label = pd.DataFrame(labels.reshape(-1,1),index=None, columns=['label'])
	print(len(df_label))
	
	return df_label

if __name__ == '__main__':
	from hmmlearn import hmm
	import numpy as np
	import pandas as pd
	import time

	#Import the tsne data representation of the mobility pattern
	df = pd.read_csv('./Output/tsne_10k_50p.csv')

	#Applies HMM clustering to the tsne data. Returns the cluster labels as a dataframe
	df_label = hmm_learn(df)
	
	#Export the dataframe as a csv file
	df_label.to_csv(r'./Output/labels_10k_50p_hmm.csv', index=False)