
import sys
import pandas as pd
import numpy as np
import multiprocessing
from pathlib import Path
from service.seleniumService import Selenium_Driver
from utils import utils


# Set logging to info
import logging
logging.basicConfig(level=logging.INFO)


# This worker is used for Multiprocessing
def worker(worker_id, df_sample):

    selenium_driver = Selenium_Driver()
    try:

        # Past the values to the selenium driver and return the frax percentage
        df_sample['FraxRiskPercentage'] = [selenium_driver.get_frax_risk_percentage(
            df_sample.loc[idx, 'PatientId'],
            df_sample.loc[idx, 'PatientGender'],
            df_sample.loc[idx,
                          'PatientAge'],
            df_sample.loc[idx,
                          'bmdtest_weight'],
            df_sample.loc[idx,
                          'bmdtest_height'],
            df_sample.loc[idx,
                          'obreak'],
            df_sample.loc[idx,
                          'parentbreak'],
            df_sample.loc[idx,
                          'smoke'],
            df_sample.loc[idx,
                          'alcohol'],
            df_sample.loc[idx,
                          'diabetes'],
            df_sample.loc[idx,
                          'arthritis'],
            df_sample.loc[idx,
                          'rxlist'],
            df_sample.loc[idx, 'bmdtest_tscore_fn']) for
            idx
            in
            range(len(df_sample))]

        logging.info('Worker %s: Done' % worker_id)

        # Save the data to a temporary file and close the driver
        raw_save_path = f"temp/temp-set-{worker_id}.csv"
        full_file_path = Path(raw_save_path)
        df_sample.to_csv(full_file_path, index=False)
        selenium_driver.close_driver()

    except Exception as e:
        logging.error(
            'Worker %s: Could not find Chrome driver. Follow the readme to install the driver.' % worker_id)


if __name__ == "__main__":
    initial_df = utils.load_dataframe("input/data.csv")

    # The input data is missing some of the columns that the FRAX calculator expects (OBREAK, RXLIST).
    # Osteoporosis Canada was able to provide these columns in the original dataset, but they all had the same value making them useless for calculation
    frax_expected_cols = ["PatientGender", "PatientAge", "bmdtest_weight", "bmdtest_height", "obreak",
                          "parentbreak", "smoke", "alcohol", "diabetes", "arthritis", "rxlist", "bmdtest_tscore_fn"]

    # We will use these columns to calculate the frax risk percentage
    # The frax risk percentage is calculated using the FRAX calculator, and the values of the columns are used to calculate the frax risk percentage
    # We will add the obreak and rxlist columns with a value of 0. The patient id is included to make it easier to identify the patient in the output file
    frax_from_clean = ["PatientId", "PatientGender", "PatientAge", "bmdtest_weight", "bmdtest_height",
                       "parentbreak", "smoke", "alcohol", "diabetes", "arthritis", "bmdtest_tscore_fn"]
    initial_df = utils.select_columns_from_df(initial_df, frax_from_clean)
    initial_df['obreak'] = 0
    initial_df['rxlist'] = 0

    # Create the temp folder if it doesn't exist
    utils.check_if_folder_exists_and_create_if_not("temp")


    # Because each record takes 3 seconds to process in the FRAX Calculator, we are going to use multi-threading to make it faster
    # Total time taken with No multi-threading: 800 records * 3 seconds = 2400 seconds or 40 minutes
    # Total time taken with multi-threading: ( 800 records / total number of physical cores in CPU ) * 3 seconds = total seconds
    # Example with intel core i5-8250u with 4 physical cores => (800/4) * 3 = 600 seconds or 10 minutes

    has_internet_connection = utils.check_internet_connection()
    if has_internet_connection:

        # Split the data based on total number of physical cores in CPU
        number_of_cores = 4
        split_df = np.array_split(initial_df, number_of_cores)

        logging.info("Total Time to finish processing the data: %.3f Min\n" %
                     (3.5 * len(split_df[0]) / 60))

        # Reset the index for each data-frame before processing the data
        for item in split_df:
            item.reset_index(inplace=True)

        # Make an array to hold the workers
        # Make N amount of processes, call the worker function and pass the dataframe to it.
        logging.info("Performing Selenium processing")
        jobs = []
        for i in range(0, number_of_cores):
            process = multiprocessing.Process(
                target=worker, args=(i + 1, split_df[i]))
            jobs.append(process)

        # Start the processes and Wait for all the jobs to finish
        for p in jobs:
            p.start()

        for p in jobs:
            p.join()

        # Check if the temporary files exist, if they do, proceed to merge the files and if not, exit the program
        do_files_exist = utils.does_file_exist("temp/temp-set-1.csv")
        if do_files_exist:
            # Load the data from the temporary file that was creating using the multi-thread worker
            # The data will be in different temporary files that can be found in the temp folder
            logging.info("Calculating FRAX Risk Level and Merging all Data Frames")
            temp_df = []
            for i in range(0, number_of_cores):

                raw_input_path = f"temp/temp-set-{i + 1}.csv"
                file_path = Path(raw_input_path)
                set_df = pd.read_csv(file_path, thousands=',')

                # Remove any rows with NaN values and reset the index of the dataframe
                set_df.dropna(subset=["FraxRiskPercentage"], inplace=True)
                set_df.reset_index(inplace=True)

                # Calculate the frax risk level (low, mid, high)
                set_df['FraxRiskLevel'] = [utils.get_frax_risk_level(
                    set_df.loc[idx, 'FraxRiskPercentage']) for idx in range(len(set_df))]
                temp_df.append(set_df)

            # Concatenate the data frames, and remove the level_0 column that is created from the multi-threading worker
            # Save the data to the output folder
            logging.info("Saving Processed Data and Deleting the temp files")
            utils.delete_all_files_in_folder("temp")
            concatenated_df = pd.concat(temp_df)
            final_merged_df = utils.remove_dataframe_columns(
                concatenated_df, ['level_0'])
            utils.save_dataframe(final_merged_df, "output/data.csv")

        else:
            logging.error(
                "Could not find the temporary files. Please check the logs.")
            sys.exit(1)

    else:
        logging.error("Unable to connect to the Internet")

    logging.info('Program Complete')
    exit(0)
