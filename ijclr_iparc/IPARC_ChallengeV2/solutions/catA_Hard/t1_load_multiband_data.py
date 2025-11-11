"""Module ID: 1
Title: init
Specification: load multi band data
Inputs: json file path. The json file has keys as "input" and "output". The input is a json file which consists of inputs and outputs. The input and output image are basically binary but with multiple bands. The band in which the pixel has value 1 is denoted as that band number in the original 2D image. e.g. [0 0 1 3 0] means in band 1 the image is: [0 0 1 0 0], in band 2 the image is [0 0 0 0 0] and in band 3 the image is [0 0 0 1 0]. You are given just the task in json format which consists of multiple input-output image pairs. Your job is to process the json, extract input and output into the required nu,ber of bands and return a pandas df. Test it using an example.
Output: pandas dataframe with each row consisting of the image input and output in it's different bands.
"""
import json
import numpy as np
import pandas as pd


def process_multiband(list_of_images, no_of_bands):
    """
    Generate the multiband data

    Parameters:
    list_of_images : list of list of int
        the initial image data
    no_of_bands : int
        the number of bands present

    Returns:
    list of numpy array
        the image data divided into different bands
    """
    return [np.array([[1 if x == band + 1 else 0 for x in row] for row in list_of_images]) for band in
            range(no_of_bands)]


def load_multiband_data(json_file_path):
    """
    Load and process the multiband data from json

    Parameters:
    json_file_path : str
        the path to the json file

    Returns:
    pandas DataFrame
        the DataFrame containing the multiband data
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    df_data = []
    for d in data:
        input_img = d['input']
        output_img = d['output']

        # flatten the lists and find max to get total bands
        total_bands = max(max([ele for sublist in input_img for ele in sublist]),
                          max([ele for sublist in output_img for ele in sublist]))

        # generate the band data
        input_bands = process_multiband(input_img, total_bands)
        output_bands = process_multiband(output_img, total_bands)

        df_data.append(
            {
                'input': input_bands,
                'output': output_bands
            }
        )

    df = pd.DataFrame(df_data)
    return df


if __name__ == "__main__":
    df = load_multiband_data(
        "../../../src/IPARC_ChallengeV2/Dataset/CatA_Hard/Task000.json")
    print(df.loc[0, 'input'][0])  # prints the 1st band for the 1st input image
    print(df.loc[0, 'input'][1])  # prints the 1st band for the 1st input image
    print(df.loc[0, 'input'][2])  # prints the 1st band for the 1st input image
    print(df.loc[0, 'output'][1])  # prints the 2nd band for the 1st output image
    print(df)

    # df = load_multiband_data('image_data.json')
    # get the first band for the first input image
    first_band_input_image = df.loc[0, 'input'][0]
    # get the second band for the first output image
    second_band_output_image = df.loc[0, 'output'][1]