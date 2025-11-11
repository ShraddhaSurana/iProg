"""Module ID: 1
Title: load data
Specification: Data is in json format with the keys 'input' and 'output'.
Inputs: "../../../src/IPARC_ChallengeV2/Dataset/CatA_Simple/Task000.json"
Output: function that loads the data in pandas
"""

import pandas as pd
import json

def load_data(filepath):
    """
    Function to load data from a json file into a pandas DataFrame.
    
    Args:
    filepath (str): Path to the json file.
    
    Returns:
    df (DataFrame): Pandas dataframe containing the data.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
        
    df = pd.json_normalize(data)
    return df
if __name__ == "__main__":
    df = load_data("../../../src/IPARC_ChallengeV2/Dataset/CatA_Simple/Task000.json")