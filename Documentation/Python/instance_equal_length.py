"""
    Mobility Pattern Observation Time
    .................................
    This python code tracks the maximum number of mobility instances/maximum travel time across all users and adds the last instance (geo-location) for n times to any user 
    whose travel time is less than the maximum travel time. Ex: user ID = 1 has 6 mobility instances, and user ID = 11 happens to have the highest travel time, i.e., 14 mobility instances.
    So, the last instance of user ID = 1 is added 8 times to its mobility list. Hence, user ID = 1 now has 14 mobility instances.

    The goal is to make all the users have the same number of mobility instances.       
"""

def instance_equal(dataframe):

    """
    This functions performs adding the last instance of any user n-times into their mobility list whose travel time is less than the maximum travel time.
    
    :param name: mobility pattern, users's instance frequency, user ID's   

    :param type: dataframe (mobility pattern), numpy array (users's ins freq, user ID's)

    :return: Equal length mobility instances of all users

    :return type: dataframe
       
    """

    df = dataframe
    
    #Get the frequency of user ID's for all users. This is to know how many mobility instances a particular user has. 
    user_max = df.groupby('UserID').count()

    #Since the entries of all the columns will be the same (frequency value), we can keep only one column
    user_max = user_max.drop(labels=['Longitude','Hour','Min','Sec'], axis=1)
    user_max.columns = ['freq']
    users = user_max.values

    arr = df.values

    #Getting the unique ID's of all the users in the data set
    user_max = user_max.reset_index()
    userid = user_max['UserID'].values

    #Logic for making all the users' instances equal length based on the max travel time from a particular user
    for i in range(len(users)):
        if i==0 and users[i]<users.max():
            diff = users.max()-users[i]   
            temp1 = arr[arr[:,0]==userid[i]]
            adder = temp1[(len(temp1)-1), :].reshape(-1,6)
            adder = np.repeat(adder, diff, axis=0)
            temp1 = np.append(temp1, adder, axis=0)
            print('created', i)
        elif users[i]<users.max():
            diff = users.max() - users[i]
            temp2 = arr[arr[:,0]==userid[i]]
            adder = temp2[(len(temp2)-1), :].reshape(-1,6)
            adder = np.repeat(adder, diff, axis=0)
            temp2 = np.append(temp2, adder, axis=0)
            temp1 = np.append(temp1, temp2, axis=0)
            print('added', i)
        else:
            temp2 = arr[arr[:,0]==userid[i]]
            temp1 = np.append(temp1, temp2, axis=0)
            print('added', i)

    #Export the numpy array as a dataframe (equal length mobility instances of N users)        
    df_add = pd.DataFrame(temp1, index=None, columns=['UserID','Latitude','Longitude','Hour','Min','Sec'])
    df_add[['UserID','Hour','Min','Sec']] = df_add[['UserID','Hour','Min','Sec']].astype('int')

    return df_add

if __name__ == '__main__':

    import numpy as np
    import pandas as pd

    #Import the mobility data. Note that this data set contains unequal length of mobility instances of different users. 
    df = pd.read_csv('paris_30k_100p.csv')

    #Call the instance_equal function to make all the length of mobility instances equal for all users 
    df_eq = instance_equal(df)

    #Export the dataframe as a csv file
    df_eq.to_csv(r'./Output/paris_10k_100p_eq.csv', index=False)
