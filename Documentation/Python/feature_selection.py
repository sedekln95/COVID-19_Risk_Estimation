"""
Feature Selection
-----------------------------
This python code computes the correlation matrix of our raw data to reduce the number of features.

Reference: https://medium.com/analytics-vidhya/feature-selection-techniques-2614b3b7efcd

"""

def feature_selection(dataframe):

	"""
	Read mobility pattern's csv file and define the coorelation matrix. From the matrix, plot a heatmap and 
	remove the least coorelated feature.
	
	Heat map interpretation: https://stats.stackexchange.com/questions/392517/how-can-one-interpret-a-heat-map-plot
	
	:param name: mobiltiy pattern, coorelation matrix, coorelation heatmap 

	:param type: dataframe (mobility pattern, coorelation matrix), figure (coorelation heatmap)

	:return: returns the mobility data with reduced features, as a result of analysing the coorelation matrix and heatmap

	:return type: dataframe
	

	""" 

	# Define the coorelation matrix for the dataframe
	df = dataframe
	cor = df.corr()

	# Plot the heatmap 
	plt.figure(figsize=(15,12))
	sns.heatmap(cor, annot=True)

	# We drop the Day feature as a result from the interpretation of the heatmap
	df=df.drop('Day', axis=1)

	# Checking for coorelation again after removing Day feature via heatmap
	cor=df.corr()
	plt.figure(figsize=(12,10))
	sns.heatmap(cor, annot=True)

	'''
	The following codes are just additional analysis on the features but their results are not included/reflected in the final feature selection
	'''

	# Additional analysis to see how many features in the UserID column is above the threshold, by taking its absolute value  
	threshold=0.0065
	a=abs(cor['UserID'])
	result=a[a>threshold]
	print(result)

	# Checking for unique values in Latitude column
	val_count = pd.value_counts(df.Latitude)
	unique_val  = pd.Series({'nunique' : len(val_count), 'unique values' : val_count.index.tolist()})
	print(val_count.append(unique_val))

	return df

if __name__ == '__main__':
	import pandas as pd
	import seaborn as sns
	import matplotlib.pyplot as plt
	
	# Define the path to read the raw data
	df = pd.read_csv('./Raw_Data/UserMovementsListEvents_0_10000.csv')

	# Call the function to perform feature selection. Returns the dataframe with reduced features.
	df_reduced = feature_selection(df)

	#Export the dataframe as a csv file
	df_reduced.to_csv(r'./Output/paris_10k_100p.csv', index=False)