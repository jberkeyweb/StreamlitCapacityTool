import pandas as pd
import warnings
import shutil
from datetime import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

root = os.getenv("SERVER_FILES")


warnings.filterwarnings("ignore")
def get_bin_data() -> pd.DataFrame:
    """This function is used to create a workable bin data DF that has fillment inputted"""
    # initializing needed dfs
    of_df = pd.read_csv(fr"{root}IDS CSV Export - Overflow.csv")
    prim_df = pd.read_csv(fr"{root}IDS CSV Export.csv")
    bindata_df = pd.read_csv(fr"{root}Data\CSVData\BinData.csv")


    main_df = bindata_df
    # making the OF Values in Filled?
    main_df.loc[main_df["Bins"].isin(of_df["BinDescription"]), "Filled?"] = "OF"
    main_df.loc[main_df["Bins"].isin(of_df["BinDescription"].str[:-1]), "Filled?"] = "OF"
    main_df.loc[main_df["Bins"].isin(of_df["BinDescription"].astype(str) + "1"), "Filled?"] = "OF"
    main_df.loc[main_df["Bins"].isin(of_df["BinDescription"].astype(str) + "2"), "Filled?"] = "OF"
    # making the Taken Values in Filled?
    main_df.loc[main_df["Bins"].isin(prim_df["BinDescription"]),"Filled?"] = "Taken"
    main_df.loc[main_df["Bins"].isin(prim_df["BinDescription"].str[:-1]), "Filled?"] = "Taken"
    main_df.loc[main_df["Bins"].isin(prim_df["BinDescription"].astype(str) + "1"), "Filled?"] = "Taken"
    main_df.loc[main_df["Bins"].isin(prim_df["BinDescription"].astype(str) + "2"), "Filled?"] = "Taken"
    # making the Available Values in Filled?
    main_df.loc[(main_df["Zone"] == "4C - SS") & ~(main_df["Bins"].isin(prim_df["BinDescription"])) & ~(main_df["Bins"].isin(of_df["BinDescription"])),"Filled?"] = "Available"
    main_df.loc[main_df["Filled?"].isna() == True,"Filled?"] = "Available"
    return main_df

    # main_df.to_csv(r"C:\Users\jberkey\Downloads\test1.csv")


    # main_df.loc[main_df["Bins"] == "6263A2"]

    # of_df.loc[of_df["BinDescription"] == "6263E2"  ]
def get_ofs() -> pd.DataFrame:
    temp_df = pd.read_csv(fr"{root}IDS CSV Export - Overflow.csv")
    return temp_df

def get_prims() -> pd.DataFrame:
    temp_df = pd.read_csv(fr"{root}IDS CSV Export.csv")
    return temp_df

def get_suom() -> pd.DataFrame:
    temp_df = pd.read_csv(fr"{root}Data\CSVData\ItemShippingAttribtues.csv")
    return temp_df

def save_csvs():
    tdate = dt.date(dt.now())
    psrc = fr"{root}IDS CSV Export.csv"
    pdst = fr"{root}Data\HistoryData\Primary History\IDS CSV Export{tdate}.csv"
    asrc = fr"{root}IDS CSV Export - Overflow.csv"
    adst = fr"{root}Data\HistoryData\Overflow History\IDS CSV Export - Overflow{tdate}.csv"

    shutil.copy(psrc,pdst)
    shutil.copy(asrc,adst)

def get_all() -> pd.DataFrame:
    temp_df = pd.read_csv(fr"{root}IDS CSV Export - All.csv")
    return temp_df

def GetPODropFile() -> pd.DataFrame:
    temp_df = pd.read_excel(fr"{root}PO Drop File.xlsx")
    return temp_df

def GetItemBreakdown() -> pd.DataFrame:
    temp_df = pd.read_csv(fr"{root}Data\CSVData\Item Breakdowns.csv")
    return temp_df

def GetLastButtonExecution() -> dict:
    """This function's only purpose is to pull the export time for labor files"""
    return {"Last Execution":dt.fromtimestamp(
        os.path.getmtime(
            fr"{root}Tools\MasterEffeciencyFile\SinglePalletPythonScript\SinglePallet.csv"
            ))
            .strftime("%m/%d/%Y %I:%M:%S %p")}

def GetExportTimes() -> dict:
    """This function returns a dictionay of export times for files used in this project"""
    r_dict = {}
    r_dict["IDS CSV Primary"] = os.path.getmtime(fr"{root}IDS CSV Export.csv")
    r_dict["IDS CSV Overflow"] = os.path.getmtime(fr"{root}IDS CSV Export - Overflow.csv")
    r_dict["Bin Data"] = os.path.getmtime(fr"{root}Data\CSVData\BinData.csv")
    r_dict["PO Drop File"] = os.path.getmtime(fr"{root}PO Drop File.xlsx")
    r_dict["Breakdowns"] = os.path.getmtime(fr"{root}Data\CSVData\Item Breakdowns.csv")
    r_dict["HUOM"] = os.path.getmtime(fr"{root}Data\CSVData\ItemHandlingAttributes.csv")
    r_dict["SUOM"] = os.path.getmtime(fr"{root}Data\CSVData\ItemShippingAttribtues.csv")
    r_dict["Item Stock Data"] = os.path.getmtime(fr"{root}Tools\MasterEffeciencyFile\SinglePalletPythonScript\SinglePallet.csv")
    
    for x,y in r_dict.items():
        r_dict[x] = dt.fromtimestamp(y).strftime("%m/%d/%Y %I:%M:%S %p")
    return r_dict

def GetConsumablePOFile() -> pd.DataFrame:
    temp_df = pd.read_excel(fr"{root}ConsumablePODropFile.xlsx")
    return temp_df

def GetExpirationData() -> pd.DataFrame:
    temp_df = pd.read_excel(fr"{root}Food Data Exports\ExpirationData.xlsx")
    return temp_df

def GetItemNotes() -> pd.DataFrame:
    temp_df = pd.read_excel(fr"{root}Food Data Exports\ItemNotesList.xlsx")
    return temp_df