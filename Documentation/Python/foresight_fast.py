"""
    Foresight/Partitioning
    ......................
    
    This python code applies different foresight values to the mobility data: 20% - 50% ahead.
    Ex: 20% ahead (80% of the mobility pattern of each user)

"""

def foresight(dataframe):

    """
    This functions performs a partition on the dataset based on a foresight value (20%-50% ahead). The resultant dataset will contain X%
    of the mobility pattern of each user.

    :param name: mobility pattern, user ID's, users's instance frequency

    :param type: dataframe (mobility pattern, users's ins freq), numpy array (users ID's)

    :return: X% of the mobility pattern of each user. In other words, the function returns a t% ahead foresight of the mobility pattern.

    :return type: numpy array

    """

    #Get the unique users
    df_test = dataframe
    users = df_test['UserID'].unique()

    #Get the frequency of the ID's of each user
    df_freq = df_test.groupby('UserID').count()
    df_freq = df_freq.drop(labels=['Longitude','Hour','Min','Sec'],axis=1)
    df_freq.columns = ['freq']
    user_count = df_freq.values
    
    arr = df_test.values

    #Logic to perform the foresight
    for i in range(len(users)):
        if i == 0:
            temp1 = arr[arr[:,0]==users[i]]
            '''
            In the code below, the decimal value (here, it is 0.8) multiplied to user count represents how many percentage of mobility data 
            we want in the final dataset. This actually represents the X% mobility pattern. The decimal value is set to the following values: 
            0.5, 0.6, 0.7, 0.8]. Please change the decimal value accordingly after each successful execution.
            '''
            p_col = (np.ceil(0.8*user_count[i])-1)[0].astype('int')
            #p_col = 30
            print(p_col)
            temp1 = temp1[:p_col+1,]
            print('Created', i)
        else:
            temp2 = arr[arr[:,0]==users[i]]
            p_col = (np.ceil(0.8*user_count[i])-1)[0].astype('int')
            #p_col = 30
            print(p_col)
            temp2 = temp2[:p_col+1,]
            temp1 = np.append(temp1,temp2,axis=0)
            print('appended', i)

    return temp1

if __name__ == '__main__':
    import pandas as pd
    import numpy as np

    #Import the mobility data. This mobility data contains equal length of mobility instances for all users.
    df = pd.read_csv('./Output/paris_10k_100p.csv') 

    #foresight function performs a patitioning method where a particular foresight value (input from the user) is chosen to our mobility data  
    temp = foresight(df)

    #Exporting the numpy temp array to a dataframe 
    df_red = pd.DataFrame(temp, index=None, columns=['UserID', 'Latitude', 'Longitude', 'Hour', 'Min', 'Sec'])
    df_red[['UserID','Hour','Min','Sec','label']] = df_red[['UserID','Hour','Min','Sec','label']].astype('int')
    df_red['contact_list'] = df_red['contact_list'].astype('int')

    #Export the dataframe as a csv file
    df_red.to_csv(r'./Output/paris_10k_50p.csv',index=False)

