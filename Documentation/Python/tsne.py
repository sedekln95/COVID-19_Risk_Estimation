"""
	t-Distributed Stochastic Neighbor Embedding	
	...........................................
	Python code for dimensionality reduction of the mobility pattern.
"""

def tsne_compute(dataframe):

	"""
	
	This function computes the t-SNE on the mobility pattern of every instance of N users. Here, N = [10000, 30000]. 
	Note that the mobility pattern can be of different foresights.

	:param name: mobility pattern, tsne result

	:param type: dataframe (mobility pattern), numpy array (tsne result)

	:return: 2D vector representation of mobility data as a dataframe

	:return type: dataframe 

	"""	

	df = dataframe
	#Imported the time to check the execution speed
	time_start = time.time()

	#Declare the tsne parameters  
	tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)

	#Fit and transform the mobility data to a 2D vector
	tsne_results = tsne.fit_transform(df)
	print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

	#Export it to a dataframe of the 2D vector
	df_tsne = pd.DataFrame(data=tsne_results, columns=['tsne_2d_one','tsne_2d_two'])

	return df_tsne

if __name__ == '__main__':
	import pandas as pd 
	import time
	import numpy as np
	from sklearn.manifold import TSNE

	#Read the mobility data
	df = pd.read_csv('./Output/paris_10k_50p.csv')

	#Call the tsne function. Returns the resultant matrix from tsne as a dataframe
	df_tsne = tsne_compute(df)

	#Export the dataframe as a csv file 
	df_tsne.to_csv(r'./Output/tsne_10k_50p.csv', index=False)