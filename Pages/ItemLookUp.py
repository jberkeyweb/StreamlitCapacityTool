import BinDataGrabber as bsg
import pandas as pd
import streamlit as st
from Data import Data


st.set_page_config(layout= "wide")


with st.spinner("Loading",show_time= True):
    
    main_df = Data(bsg.get_bin_data())
    # renamer variable
    rem_cols = [
        "Aisle","BinDescription","BinType","ItemNumber","ItemDescription","UOM","UnitsOnOrder",
        "Max","Min","UnitsOnHand","AlternateBinProfileName"
        ]

    # default column names to display something when no UI is present
    default_cols = [
        "ZoneDescription1",
        "BinDescription",
        "BinType",
        "ItemNumber1",
        "ItemDescription",
        "UnitDisplay2",
        "UnitsOnOrder",
        "MaximumStock2",
        "MinimumStock",
        "UnitsOnHand",
        "PrimaryBinMinimumQuantity",
        "PrimaryBinMaximumQuantity",
        "LicensePlateNumbers",
        "TiHiQtyPerLayerHuom",
        "TiHiQuantity",
        "AlternateBinProfileName",
    ]

    # renamer variable
    renamer = {
        "ZoneDescription1":"Aisle",
        "ItemNumber1":"ItemNumber",
        "MaximumStock2":"Max",
        "MinimumStock":"Min",
        "ALternateBinProfileName":"AlternateBinProfile",
        "UnitDisplay2":"UOM"
        }



    st.title("Item Lookup")
    col1, col2 = st.columns(2)

    with col1:
        ui = st.text_area("Enter Item Numbers below in one column",height= 400)
        item_list = ui.split()
        item_list = [x.upper() for x in item_list]
        ui1 = {"Items":item_list}
        # temp dfs to be inputted into
        temp_df = pd.DataFrame(columns= default_cols)
        temp_df2 = pd.DataFrame()
        temp_df3 = pd.DataFrame(columns= default_cols)
        temp_of_df = pd.DataFrame(columns= default_cols)
        prim_df = bsg.get_prims()
        of_df = bsg.get_ofs()
        count_df = pd.concat([prim_df,of_df])
        for j in item_list:
            presult = prim_df[prim_df["ItemNumber1"] == j]
            aresult = of_df[of_df["ItemNumber1"] == j]
            if presult.size > 0:
                temp_df = pd.concat([temp_df,presult])
            else:
                temp_df2 = pd.concat([temp_df2,pd.DataFrame({"ItemNumber":[j],"Bin":["No Bin"]})])
            if aresult.size > 0:
                temp_of_df = pd.concat([temp_of_df,aresult])
            # temp_df = temp_df[["BinDescription","ItemNumber1"]]
        count_df = count_df[count_df["ItemNumber1"].isin(item_list)].groupby("ItemNumber1")["ItemNumber1"].size().reset_index(name= "Bins Affected")

    with col2:
        ui1 = pd.DataFrame(ui1)
        if ui1.size > 0:
            ui1 = ui1.merge(count_df,how= "left",left_on="Items",right_on="ItemNumber1")
        count_df = count_df.rename(columns= {"ItemNumber1":"ItemNumber"})
        st.dataframe(count_df, hide_index= True)

    col1,col2 = st.columns(2)

    with col1:
        st.header("Binned Items")
        if temp_df.size > 0:
            temp_df3 = temp_df[["ItemNumber1","BinDescription","ZoneDescription1"]]
            
        temp_df3 = temp_df3.rename(columns= {"ItemNumber1": "ItemNumber","BinDescription":"Bin","ZoneDescription1": "Aisle"})
        st.dataframe(temp_df3,hide_index= True)
    with col2:
        st.header("Non Bins")
        st.dataframe(temp_df2,hide_index= True)
    st.header("Primary Info")
    st.dataframe(temp_df.rename(columns= renamer)[rem_cols],hide_index= True)
    st.header("Overflow Info")
    st.dataframe(temp_of_df.rename(columns= renamer)[rem_cols],hide_index= True)

    # making breakdown df and output
    breakdown_df = bsg.GetItemBreakdown()[["Source Item Number","Breakdown Item Number","Breakdown Quantity","Breakdown Shrink Wrap Required", "Source Quantity"]]
    breakdown_df = breakdown_df.merge(prim_df[["ItemNumber1", "BinDescription"]], how= "left", left_on= "Breakdown Item Number", right_on= "ItemNumber1")
    breakdown_df = breakdown_df[breakdown_df["Source Item Number"].isin(ui.split())]
    breakdown_df = breakdown_df.drop(columns= "ItemNumber1")
    breakdown_df = breakdown_df.rename(columns= {"BinDescription":"Breakdown Primary", "Breakdown Shrink Wrap Required":"Shrinkwrap?"})
    breakdown_df = breakdown_df[["Source Item Number", "Breakdown Item Number", "Breakdown Primary", "Shrinkwrap?", "Breakdown Quantity", "Source Quantity"]]
    suom_df = bsg.get_suom()
    
    st.header("Breakdowns")
    st.dataframe(breakdown_df, hide_index= True)

    # making SUOM df and output
    st.header("SUOM Data")
    # a list of columns to keep in the SUOM df
    suom_cols = [
        "ItemNumber",
        "Length",
        "Width",
        "Height",
        "Volume",
        "Weight",
        "Description",
        "UOM",
        "HandlingSUOMQuantity",
        "ShipmentRegulationType",
        "WebStockSignificanceCode"
    ]
    st.dataframe(suom_df[suom_df["ItemNumber"].isin(ui.split())][suom_cols],hide_index= True)
    temp_dict = {}
    for header in bsg.get_prims().columns:
        temp_dict[header] = [header]
    export_headers = pd.DataFrame(temp_dict)
    st.header("Export Headers")
    st.dataframe(export_headers, hide_index= True)
    st.header("Full Primary Export")
    st.dataframe(bsg.get_prims(),hide_index= True)
    st.header("Full Alternate Export")
    st.dataframe(bsg.get_ofs(),hide_index= True)
