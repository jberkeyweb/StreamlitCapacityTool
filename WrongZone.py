import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
root = os.getenv("SERVER_FILES")
def main():

    #Defining original DataFrames
    df_prim = pd.read_csv(fr"{root}IDS CSV Export.csv")
    df_of = pd.read_csv(fr"{root}IDS CSV Export - Overflow.csv")
    df_main = df_of


    #Merge overflow and primary by itemnumber, Rename columns
    df_main = df_main.merge(df_prim[["BinDescription", "ItemNumber1"]], how = "left", left_on="ItemNumber1", right_on= "ItemNumber1")
    df_main = df_main.rename(columns={"BinDescription_y": "PrimaryBin","BinDescription_x": "Bin"})

    df_main["OFZone"] = df_main["Bin"].str[:1]
    df_main["PrimZone"] = df_main["PrimaryBin"].str[:1]
    df_main["Move?"] = "DontMove"
    df_main.loc[(~df_main["OFZone"].isin(["1","2","3"])) & (df_main["PrimZone"].isin(["1","2","3"])),["Move?", "Move to Zone"]] = ["Move", "Moves to 1/2/3"]
    df_main.loc[(~df_main["OFZone"].isin(["5","7"])) & (df_main["PrimZone"].isin(["5","7"])),["Move?", "Move to Zone"]] = ["Move", "Moves to 5/7"]
    df_main.loc[(~df_main["OFZone"].isin(["6","8","9"])) & (df_main["PrimZone"].isin(["6","8","9"])),["Move?", "Move to Zone"]] = ["Move", "Moves to 6/8/9"]

    df_main= df_main[df_main["Move to Zone"].isna()==False][["ItemNumber1","PrimaryBin","Bin","Move to Zone"]]

    df_main.to_csv(fr"{root}Tools\WrongOverflowFinder\WrongZoneFinderPythonScript.csv",index=False)