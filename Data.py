import BinDataGrabber as bsg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

# main_df = bsg.get_bin_data()

load_dotenv()

root = os.getenv("SERVER_FILES")

class Data:
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.show_cols = df.columns
        self.get_available_primaries = df.loc[(df["Filled?"] == "Available") & (df["Bin Type"].str.contains("PRIMARY"))]
        self.get_available_alternates = df.loc[(df["Filled?"] == "Available") & (df["Bin Type"].str.contains("ALTERNATE"))]
        self.get_available_bins = df.loc[(df["Filled?"] == "Available") & (df["Bin Type"] != "STRUCTURAL")]
        self.get_aisles = df["Zone"].unique()
        self.get_all_alts = df.loc[df["Bin Type"].str.contains("ALTERNATE")]
        self.get_all_prims = df.loc[df["Bin Type"].str.contains("PRIMARY")]
        self.get_all_bins = df.loc[~df["Bin Type"].str.contains("STRUCTURAL")]
        self.get_filled_bins = df.loc[(df["Filled?"] != "Available")]
        self.get_filled_primaries = df.loc[(df["Filled?"] != "Available") & (df["Bin Type"].str.contains("PRIMARY"))]
        self.get_filled_alternates = df.loc[(df["Filled?"] != "Available") & (df["Bin Type"].str.contains("ALTERNATE"))]
        self.get_total_num_bins = len(self.get_all_bins[self.get_all_bins["Relationship"] != "Parent"])
        self.get_total_num_available_bins = len(self.get_available_bins[self.get_available_bins["Relationship"] != "Parent"])
        self.get_total_num_primaries = len(self.get_all_prims[self.get_all_prims["Relationship"] != "Parent"])
        self.get_total_num_alternates = len(self.get_all_alts[self.get_all_alts["Relationship"] != "Parent"])
        self.get_total_num_available_primaries = len(self.get_available_primaries[self.get_available_primaries["Relationship"] != "Parent"])
        self.get_total_num_available_alts = len(self.get_available_alternates[self.get_available_alternates["Relationship"] != "Parent"])


    def SummarizeAvailableAlternate(self) -> pd.DataFrame:
        """Returns a summarized dataframe of all of the available """
        temp_df = self.get_available_alternates
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df


    def SummarizeAvailablePrimaries(self) -> pd.DataFrame:
        """Returns a summarized dataframe of all of the available """
        temp_df = self.get_available_primaries
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df
    

    def SummarizeTakenAlternates(self) -> pd.DataFrame:
        temp_df = self.get_filled_alternates
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df

    def SummarizeTakenPrimaries(self) -> pd.DataFrame:
        temp_df = self.get_filled_primaries
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df
    
    def SummarizeTakenBins(self) -> pd.DataFrame:
        temp_df = self.get_filled_bins
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df

    def SummarizeAvailableBins(self) -> pd.DataFrame:
        """Returns a summarized dataframe of all of the available """
        temp_df = self.get_available_bins
        temp_df = temp_df.groupby("Zone")["Filled?"].count().reset_index(name= "Bins")
        return temp_df
    
    def SummarizeAllBins(self) -> pd.DataFrame:
        temp_df = self.get_all_bins
        temp_df = temp_df.groupby("Zone").count()["Bins"].reset_index(name= "Bins")
        return temp_df
    
    def SummarizeAllPrimaryBins(self) -> pd.DataFrame:
        temp_df = self.get_all_prims
        temp_df = temp_df.groupby("Zone").count()["Bins"].reset_index(name= "Bins")
        return temp_df

    def SummarizeAllAlternateBins(self) -> pd.DataFrame:
        temp_df = self.get_all_alts
        temp_df = temp_df.groupby("Zone").count()["Bins"].reset_index(name= "Bins")
        return temp_df

    def RandomBinPickerStreamLit(self,zone:str,bins:int,level:str = "All") -> pd.DataFrame:
        """This function is used to pick a selected amount of random bins from a selected aisle"""

        random_bins = self.df.loc[(self.df["Filled?"] == "Available") & (self.df["Bin Type"].str.contains("PRIMARY"))].sample(frac=1)
        random_bins = random_bins[random_bins["Zone"] == zone]
        if level != "All":
            random_bins = random_bins[random_bins["Level"] == level]
        random_bins = random_bins[["Bins","Bin Type"]]

        return random_bins.head(bins)

    def ZoneSummary(self) -> pd.DataFrame:
        bd = bsg.get_bin_data()
        return bsg.get_bin_data()


    def BulkItemAssignmentStreamlit(self,items:list[str]) -> pd.DataFrame:
        """Matches up a random bin with an index entered by the user. The layout for this should simply be a list of item numbers with the wanted
        index to the left of it (A1: {Index} ||| A2: {Item Number})"""
        zone_list = []
        item_list = []
        bin_list = []
        # temp_df = self.SummarizeAvailablePrimaries()
        bin_grab = self.get_available_primaries.sample(frac=1)
        for x,y in enumerate(items):
            if x % 2 == 1:
                item_list.append(y)
            else:
                zone_list.append(y)
        for x in zone_list:
            temp_df = bin_grab[bin_grab["Zone"] == x]
            if temp_df.empty:
                return None
            bin_list.append(temp_df.iloc[0].Bins)
            bin_grab = bin_grab[bin_grab["Bins"] != temp_df.iloc[0].Bins]
        return pd.DataFrame({"Items":item_list,"Bins":bin_list,"Min":1,"Max":1,"Primary":"True"})


    def ShowLayoutSummary(self) -> pd.DataFrame:
        """Returns a dataframe summary of capacity fillment"""
        temp_df = pd.DataFrame(self.get_aisles)
        temp_df.columns = ["Zone"]
        alts = self.get_all_alts.groupby("Zone")["Bin Type"].count().reset_index(name = "Alts")
        prims = self.get_all_prims.groupby("Zone")["Bins"].count().reset_index(name = "Prims")
        bins = self.get_all_bins.groupby("Zone")["Bins"].count().reset_index(name = "Bins")
        filled_bins = self.get_all_bins.loc[self.get_all_bins["Filled?"] != "Available"].groupby("Zone").size().reset_index(name = "Filled")
        filled_alts = self.get_all_alts[self.get_all_alts["Filled?"] != "Available"].groupby("Zone").size().reset_index(name = "F Alts")
        filled_prims = self.get_all_prims[self.get_all_prims["Filled?"] != "Available"].groupby("Zone").size().reset_index(name = "F Prims")


        # Merging and adding to DF
        temp_df = temp_df.merge(filled_bins, how="left",on= "Zone").fillna(0)
        temp_df = temp_df.merge(bins, how="left",on= "Zone").fillna(0)
        temp_df["Filled%"] = (temp_df["Filled"] / temp_df["Bins"]).fillna(0).map("{:.2%}".format)
        temp_df = temp_df.merge(filled_alts,how= "left", on="Zone")
        temp_df = temp_df.merge(alts, how="left",on= "Zone").fillna(0)
        temp_df = temp_df.rename(columns={"Bin Type":"Alts"})
        temp_df["Alt%"] = (temp_df["F Alts"] / temp_df["Alts"]).fillna(0).map("{:.2%}".format)
        temp_df = temp_df.merge(filled_prims,how = "left", on= "Zone").fillna(0)
        temp_df = temp_df.merge(prims,how = "left", on= "Zone").fillna(0)
        temp_df["Prims%"] = (temp_df["F Prims"] / temp_df["Prims"]).fillna(0).map("{:.2%}".format)
        
        temp_df["F Prims"] = temp_df["F Prims"].astype(int)
        temp_df["Filled"] = temp_df["Filled"].astype(int)
        temp_df["Alts"] = temp_df["Alts"].astype(int)
        temp_df["F Alts"] = temp_df["F Alts"].astype(int)
        temp_df["Prims"] = temp_df["Prims"].astype(int)
        # print(temp_df.to_string(index= False))
        return temp_df

    def ShowLayoutGraph(self):
        """Shows a chart of the bin layout for the warehouse categorized by zone"""
        temp_df = self.ShowLayoutSummary()
        bins_plot = temp_df[["Zone","Prims","Alts"]]
        # bins_plot = bins_plot.set_index("Zone", drop=True)
        merge_df = self.df[["Zone","Zone Type"]]
        bins_plot = bins_plot.merge(merge_df,how= "left", right_on="Zone",left_on="Zone").drop_duplicates()
        bins_plot = bins_plot.set_index("Zone Type", drop=True).drop(columns="Zone")
        bins_plot = bins_plot.groupby("Zone Type")[["Prims","Alts"]].sum()
        ax = bins_plot.plot(kind="bar", stacked= True, subplots= True, sharex= True, sharey= True, figsize=(16.0,9.0))
        # ax.set_yticks(np.arange(0, 18000 + 2, 500))

        for axes in ax.flat:
            axes.set_ylabel("Bins")
            axes.set_xlabel("Zone")
            axes.set_yticks(np.arange(0, 16000 + 1, 2000))
            for container in axes.containers:
                # labels = [f"{v:.0f}" if v >= 1000 else "" for v in container.datavalues]
                axes.bar_label(container, label_type="edge")        
        plt.xticks(rotation= 35)
        plt.show()


        # return print(bins_plot)
        # return plt.show()
        # return print(bins_plot.to_string())
    
    def ItemSearch(self) -> pd.DataFrame:
        """This function serves as an item lookup where the user can copy and paste a list of items to be analyzed"""
        item_list = []
        prim_df = bsg.get_prims()[["ZoneDescription1","BinDescription","BinType","ItemNumber1","UnitsOnHand","MaximumStock2","UnitsOnOrder","ItemDescription"]]
        of_df = bsg.get_ofs()[["ZoneDescription1","BinDescription","BinType","ItemNumber1","UnitsOnHand","MaximumStock2","UnitsOnOrder","ItemDescription"]]
        # suom_df = bsg.get_suom()
        master_df = pd.DataFrame()
        while True:
            ui = input("Enter a list of item numbers to look up\nEnter G to print current item list\nEnter Y to continue script\nEnter Q at anytime to break out of program\n\n")
            if ui.upper() == "Y":
                for x in item_list:
                    temp_prim_df = prim_df[prim_df["ItemNumber1"] == x]
                    temp_of_df = of_df[of_df["ItemNumber1"] == x]
                    all_df = pd.concat([temp_prim_df,temp_of_df])
                    all_df = all_df[all_df["ItemNumber1"].isin(item_list)]
                    master_df = pd.concat([master_df,all_df])
                    primary_bin = temp_prim_df["BinDescription"].to_string(index= False)
                    max_stock = temp_prim_df["MaximumStock2"].to_string(index= False)
                    on_order = temp_prim_df["UnitsOnOrder"].to_string(index= False)
                    item_description = temp_prim_df["ItemDescription"].to_string(index= False)
                    if temp_prim_df.size == 0:
                        primary_bin = "No Primary"
                    print(f"\nItem: {x} ||| Primary: {primary_bin} ||| OnOrder: {on_order} ||| Max: {max_stock}\nDescription: {item_description}\n\n{temp_of_df[["ZoneDescription1","BinDescription","BinType","UnitsOnHand"]]
                    .to_string(index=False)}\n\n")
                ui2 = input("Export CSV of bin locations (Y/N)\n")
                if ui2.upper() == "Y":
                    dir = fr"{root}Tools\Python Scripts\PPToolAnalysis\Output Files\ItemSearchExport.csv"
                    master_df.to_csv(dir,index= False)
                    print(f"\nSaved to {dir}\n")
                    break
                else:
                    break
            if ui.upper() == "G":
                print(item_list)
            if ui.upper() == "Q":
                break
            else:
                item_list.append(ui)

    def InputToList(UI: str) -> list:
        """This function simply converts a string to a list using split"""
        return UI.split()

    def SummarizeAvailablePrimsByLevel(self):
        temp_df = self.get_available_primaries
        temp_df = temp_df.groupby(["Zone","Level"]).size()
        return temp_df
