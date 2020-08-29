"""
    k-means Clustering
    ..................
    This python code applies k-means algorithm to the reduced 2D vector representation of the mobility pattern. Based on the nature of the data,
    clustering is done on predicting the future mobility pattern of each user.
    
    The number of cluster is set to 5, 6, 7, 8.
"""
def k_means(dataframe):

    """
    Performs k-means clustering on the equivalent tsne data (2D vector) representation of the mobility pattern.

    :param name: tsne 2D vector of mobility data, cluster centroids, frequency of different mobility instances in all the clusters, i.e., how many instances a particular cluster has

    :param type: dataframe (tsne 2D vector), numpy array (centroids, frequency)

    :return: cluster labels

    :return type: dataframe
    """

    #Define the number of clusters for k-means. Please change the n_cluster value after each successful execution
    df = dataframe
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(df)

    #Compute the clusters
    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_
    
    #Checking how many mobility instances have fallen into the different clusters 
    (unique, counts) = np.unique(labels, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    print(frequencies)
    
    #Create a dataframe from the cluster labels
    df_label = pd.DataFrame(labels, columns=['label'])
    print(len(df_label))

    return df_label


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans

    #Import the equivalent tsne data of the mobility pattern
    df = pd.read_csv('./Output/tsne_10k_50p.csv')

    #Apply k-means to the imported data. The function returns the cluster labels. 
    df_label = k_means(df) 

    #Export the dataframe as a csv file
    df_label.to_csv(r'./Output/labels_10k_50p_km.csv', index=False)