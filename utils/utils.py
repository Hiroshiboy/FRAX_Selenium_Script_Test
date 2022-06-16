import pathlib
import pandas as pd
import numpy as np
import requests

def load_dataframe(file_name):
    """
    Loads a dataframe from a csv file.
    :param file_name: name of the csv file
    :return: dataframe
    """
    return pd.read_csv(file_name)

def select_columns_from_df(dataframe, columns):
    """
    Selects columns from a dataframe.
    :param dataframe: dataframe
    :param columns: list of columns
    :return: dataframe
    """
    return dataframe[columns]

def check_internet_connection():
    """
    Checks if the internet connection is working.
    :return: boolean
    """
    try:
        return  requests.get("http://www.google.com", timeout=5)
    except ImportError:
        return False
    
def remove_dataframe_columns(dataframe, columns):
    """
    Removes columns from a dataframe.
    :param dataframe: dataframe
    :param columns: list of columns
    :return: dataframe
    """
    return dataframe.drop(columns, axis=1)

def get_frax_risk_level(percentage):
    result = ""
    if percentage < 10:
        result = "Low"
    elif 10 <= percentage <= 20:
        result = "Moderate"
    elif percentage > 20:
        result = "High"
    return result

def save_dataframe(dataframe, file_name):
    """
    Saves a dataframe to a csv file.
    :param dataframe: dataframe
    :param file_name: name of the csv file
    :return: None
    """
    dataframe.to_csv(file_name, index=False)

def does_file_exist(file_name):
    """
    Checks if a file exists.
    :param file_name: name of the file
    :return: boolean
    """
    return pathlib.Path(file_name).exists()

def delete_all_files_in_folder(folder_name):
    """
    Deletes all files in a folder.
    :param folder_name: name of the folder
    :return: None
    """
    for file in pathlib.Path(folder_name).glob('*'):
        file.unlink()