"""
	Contact List Generation
	.......................
	This python code generates the contact list of every instance of a user to every other instance of other users
	based on a pre-determined distance (10 metres) around a particular instance of a user.  
"""

def labelSplit(df, label):
	"""
	This function returns a sub-portion of the mobility data based on the cluster labels.

	:param name: merged mobility data + cluster labels , cluster label

	:param type: dataframe (mobility data), integer (cluster label)

	:return: A sub-portion of the mobility data with the same cluster label

	:return type: dataframe
	"""

	df_new = df[(df['label']==label)]
	df_new = df_new.reset_index(drop=True)
	return df_new

	'''The three functions below are already coded in the main function in a much simplified version so I have not provided the documentation
	in Sphinx. But just in case, if you want to know what it does, I have provided comments in some of the lines of code.'''
def remove_user(df_split, userID, user_index):
	'''
	The operation performed here is to isolate the row of an instance of a particular user id using 
	the index value from a sub-portion dataset which only has a single cluster label.

	Note: Function is not used in the main function.

	:param name: mobility data of one cluster from M clusters, user ID, user index

	:param type: dataframe (mobility data), integer (user ID, user index)

	:return: dataset with all instances of user ID passed in the argument removed, and the isolated row of an instance of a user based on the index value passed in the function argument

	:return type: dataframe (dataset), numpy array (isolated row)	
	''' 
	series = df_split.iloc[user_index, :]
	df_user = series.to_frame().values
	#user_arr = df_user.values
	user_arr = np.delete(df_user, [0,3], 0)
	user_arr = user_arr.flatten()
	df_new = df_split.drop(df_split[df_split['UserID'] == userID].index, inplace=False)
	return df_new.values, user_arr

def splitArrGen(df_new):
	'''
	Returns the numpy array representation of the sub-portion dataset.

	Note: Function is not used in the main function.

	:param name: mobility data of one cluster from M clusters, eg: cluster ID = 1.

	:param type: dataframe

	:return: Equivalent array representation of the dataframe passed in the argument

	:return type: numpy array 	
	'''
	arrList = df_new.values
	return arrList

def concatContactList(contact_list, df_contactList):
	'''
	Concatenate the contact list of an instance of a user to a list of 'contact list' for a particular cluster label.
	Everytime a contact list is created for one particular instance of a user, we add that instance to a list of users' instance whose 
	contact list is already being found.

	Note: Function is not used in the main function. 

	:param name: contact list of an instance of a user, concatenated contact list of instances of unique users in a cluster

	:param type: numpy array (contact list), dataframe(concatenated contact list)

	:return: the contatenation of the list of contact list for different instance of users with an instance of user i in a cluster.

	:return type: dataframe
	'''
	df_concatList = pd.DataFrame(contact_list.reshape(-1,1), columns=['contact_list'])
	df_contactList = pd.concat((df_contactList,df_concatList),axis=0,ignore_index=True)
	return df_contactList  

def num_user(user):
	"""
	This functions creates a dataframe for the number of unique users in a cluster. 

	:param name: unique users

	:param type: numpy array (unique users)

	:return: number of unique users in a cluster

	:return type: dataframe
	"""

	df = pd.DataFrame(user.reshape(-1,1), index=None, columns=['user_count'])
	return df

def haversine(sin_lat1, sin_lat2, cos_lat1, cos_lat2, cos_lon1, cos_lon2, sin_lon1, sin_lon2, R):
	"""
	This function calculates the haversine distance between an instance of a user to every other instances of other users belonging to the same cluster. 
	The haversine distance is a modified version of the original formula and the explanation to the modification can be found in 'Haversine distance.docx' under 'Docs' 
	folder of the repo.

	The geo-coordinates are coverted to radians before calculating the distance.
	
	:param name: sine(latitude_centroid), sine(latitude_others), cosine(latitude_centroid), consine(latitude_others), sine(longitude_centroid), sine(longitude_others), cosine(longitude_centroid), consine(longitude_others), radius of the earth

	:param type: radians (centroid), numpy array (others), floating point (radius of the earth)

	:return: haversine distance

	:return type: floating point   
	"""
	a = (1 - sin_lat1*sin_lat2 - cos_lat1 * cos_lat2 * (cos_lon1*cos_lon2 + sin_lon1*sin_lon2))/2
	c = 2 * np.arcsin(np.sqrt(a)) 
	total_m = R * c
	return total_m


if __name__ == '__main__':
	import numpy as np
	import pandas as pd
	import time

	#Define the start time of the execution
	start_time = time.time()
	
	#Define the radius of the earth in metres
	R = 6378.137 * 1000
	k  = 0 

	#Import the cluster labels from the identified clustering algorithm and the mobility pattern at t% ahead foresight
	df_ins = pd.read_csv('./Output/paris_30k_60p.csv')
	df_label = pd.read_csv('./Output/labels_5_60p_em.csv')

	#Concatenate the mobility pattern and the labels
	df_res = pd.concat((df_ins,df_label),axis=1, ignore_index=True)
	df_res.columns = ['UserID','Latitude','Longitude','Hour','Min','Sec','label']
	
	#Sort the concatenated dataframe in the ascending order of labels
	df_res = df_res.sort_values(by=['label'])
	df_res = df_res.reset_index(drop=True)

	#Get the ID/labels of clusters
	num_cluster = df_res['label'].nunique()
	
	#Drop unwanted features
	df_drop = df_res.drop(['Hour','Min','Sec'],axis=1,inplace=False)
	
	'''
	Since the geo-coordinate of each instance of our users are in degree value, we need to use great circle distance to 
	determine the distance between any two instances of two users. Another option is using Vincenty distance.
	We will define the trigonometric values prior before calculation of haversine distance. This is to save execution time
	'''  
	df_drop[['Latitude','Longitude']] = np.deg2rad(df_drop[['Latitude','Longitude']])
	#The numbering right beside each code just represents the column index of these values 
	df_drop['cos_lat'] = np.cos(df_drop['Latitude'])#4
	df_drop['sin_lat'] = np.sin(df_drop['Latitude'])#5
	df_drop['cos_long'] = np.cos(df_drop['Longitude'])#6
	df_drop['sin_long'] = np.sin(df_drop['Longitude'])#7
	
	hav_val  = np.zeros((len(df_res),1), float)
	#Count how many number of unique users are there in a particular cluster
	user_count = np.zeros((num_cluster,1),int)

	#Logic to find the contact list of any instance of a user. Note that the execution time will be in order of hours.
	for i in range(num_cluster):
		#The loop is designed to generate the contact list for every instance of a user in a particular cluster
		
		#Takes a portion of the mobility data having the same cluster label
		df_split = labelSplit(df_drop, i)

		#Save the number of unique users in a cluster through each entry of the array
		user_count[i] = df_split['UserID'].nunique()
		
		#Get the user ID's
		userid = df_split['UserID'].values

		split_arr = df_split.values
		for j in range(len(df_split)):
			s = time.time()

			'''Deleting every instance of user j when we treat j as the centroid. This is because we cannot count another instance of the 
			same user into its own contact list''' 
			arr = np.delete(split_arr, np.where(split_arr[:,0] == userid[j]),axis=0)

			#Calculate haversine distance
			hav_dist = haversine(arr[:,5], split_arr[j][5], arr[:,4], split_arr[j][4], arr[:,6], split_arr[j][6], arr[:,7], split_arr[j][7], R)
			
			#Updating the contact list of an instance of a user if it falls within 10 metre distance around that user
			hav_val[k] = len(hav_dist[hav_dist<=10])
			k = k+1
			print('Contact list formed for label', i, 'at row', j)
			print('time in sec ->', time.time()-s)

	#Exporting the contact list, and number of unique users in a cluster as csv files.  
	df_hav = pd.DataFrame(hav_val.astype('int'),index=None, columns=['contact_list'])
	print('The execution time is %s seconds' %(time.time()-start_time))
	df_user_count = num_user(user_count)
	df_user_count.to_csv(r'./Output/user_count_5_60p_em.csv',index=None)
	df_hav.to_csv(r'./Output/contact_list_5_60p_em.csv',index=None)
	
	#Merge the mobility pattern and contact list into a single dataframe 
	df_res = pd.concat((df_res,df_hav),axis=1,ignore_index=True)
	df_res.columns = ['UserID','Latitude','Longitude','Hour','Min','Sec','label','contact_list']

	#Before exporting, we rearrange the dataset in the ascending order of user ID's
	df_res = df_res.sort_values(by=['UserID'])
	df_res = df_res.reset_index(drop=True)
	df_res.to_csv(r'./Output/merged_list_ins_cl_5_60p_em.csv',index=None)
	print('Merged list created')
