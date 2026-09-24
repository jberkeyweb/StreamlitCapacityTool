import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

root = os.getenv("SERVER_FILES")

def main():
    df_primary = pd.read_csv(fr"{root}IDS CSV Export.csv")
    df_overflow = pd.read_csv(fr"{root}IDS CSV Export - Overflow.csv")
    df_bindata = pd.read_excel(fr"{root}Data\BinData.xlsx", engine='openpyxl')
    df_SUOM = pd.read_excel(fr"{root}Data\ItemShippingAttribtues.xlsx", engine='openpyxl')

    df = df_overflow[~ df_overflow["ItemNumber1"].str.startswith("999")]
    df = df.rename(columns={"BinDescription": "Bins"})

    # merges to bin volume
    df = df.merge(df_bindata[["Bins", "Bin Volume"]], on="Bins",how="left")

    df = df.merge(df_SUOM[["ItemNumber", "Volume"]], left_on="ItemNumber1", right_on="ItemNumber", how="left").drop(columns = "ItemNumber")


    df = df.rename(columns={"Volume": "UnitVolume"})
    
    list_cols = ["UnitVolume","UnitsOnHand"]
    for cols in list_cols:
        df[cols] = pd.to_numeric(df[cols].astype(str).str.replace(r"[^\d.-]","",regex=True),errors= "coerce")




    df["VolInTargetBin"] = (df["UnitVolume"] * df["UnitsOnHand"]).round(decimals=2)



    #get the of count
    df["OFCOunt"] = df.groupby("ItemNumber1")["ItemNumber1"].transform(
        "count"
    )

    df.columns
    df_primary = df_primary.merge(df_bindata,how = "left", left_on="BinDescription", right_on = "Bins")

    df = df.merge(df_primary[["BinDescription","Bin Volume","ItemNumber1"]],how = "left", left_on="ItemNumber1", right_on="ItemNumber1")

    df = df.rename(columns={"Bin Volume_y":"PrimaryBinVolume","BinDescription": "Primary Bin"})


    #pulling binpvolume to be merged into df
    df_primary = df_primary.merge(df_SUOM[["ItemNumber", "Volume"]],how = "left", left_on="ItemNumber1", right_on="ItemNumber")


    df_primary.drop("ItemNumber", axis = "columns")


    list_cols = ["UnitsOnHand", "Volume"]
    for cols in list_cols:
        df_primary[cols] = pd.to_numeric(df_primary[cols].astype(str).str.replace(r"[^\d.-]","", regex= True),errors = "coerce")


    df_primary["InBinPVolume"] = (df_primary["UnitsOnHand"] * df_primary["Volume"]).round(2)


    df_primary = df_primary.rename(columns= {"UnitsOnHand":"PUnitsOnHand"})
    df_primary.columns
    df = df.merge(df_primary[["BinDescription", "ItemNumber","InBinPVolume","PUnitsOnHand"]],how = "left", left_on="ItemNumber1", right_on="ItemNumber")
    df = df.drop(["ItemNumber","BinDescription"], axis = "columns")

    df["Fits?"] = (
        (df["InBinPVolume"] + df["VolInTargetBin"]) < df["PrimaryBinVolume"]
    )

    df.loc[df["Bins"] == "1017A2",["PrimaryBinVolume","Bins","OFCOunt","Primary Bin","InBinPVolume","Fits?","VolInTargetBin"]]
    # this section sorts by the vol in target bin and then removes every entry except the first to then be sorted
    # for the end product
    df = df.sort_values(by= "VolInTargetBin")
    df = df.drop_duplicates(subset = "ItemNumber1", keep = "first")
    df = df.sort_values(by=["ZoneDescription1", "VolInTargetBin"])


    #pull only the min volume per item for OF
    df["minvol"] = df.groupby("ItemNumber1")["VolInTargetBin"].transform(
        "min"
    )
    df = df[df["Fits?"] == True]

    df[["ZoneDescription1","ItemNumber1","PrimaryBinVolume","Bins","UnitsOnHand","OFCOunt","Primary Bin","PUnitsOnHand","InBinPVolume","Fits?","VolInTargetBin","minvol"]].to_csv(fr"{root}Tools\MasterEffeciencyFile\SInglePalletPythonScript\SinglePallet.csv",index=False)
