import BinDataGrabber as bsg
import pandas as pd
import streamlit as st
from Data import Data


def FindOpenBins(df:pd.DataFrame):
    """This method is used to find the amount of open bins in the variable df"""
    return len(df[df["Filled?"] == "Available"])

main_df = bsg.get_bin_data()


main_df.loc[main_df["Level"] == "A","Bin Type"] = ""

