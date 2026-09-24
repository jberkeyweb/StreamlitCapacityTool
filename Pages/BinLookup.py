import BinDataGrabber as bsg
import pandas as pd
import streamlit as st
from Data import Data


st.set_page_config(layout= "wide")


with st.spinner("Loading",show_time= True):

    main_df = Data(bsg.get_bin_data())
    st.title("Bin Breakdown",text_alignment= "center")
    bin_breakdown_df = main_df.get_all_bins
    aisle_list = main_df.get_aisles
    zone_list = main_df.df["Area"].unique()



    # selection section
    col1, col2, col3, col4, col5, col6, col7,col8 = st.columns([1,1,1,2,2,2,2,1])
    with col1:
        st.multiselect("Aisle Selection",aisle_list,key= "aisle_select")
    with col2:
        st.multiselect("Area Selection", zone_list, key= "zone_select")
    with col3:
        st.multiselect("Level Selection", main_df.df["Level"].unique(), key= "level_select")
    with col4:
        st.multiselect("Zone Type Selection", main_df.df["Zone Type"].unique(), key= "zone_type_select")        
    with col5:
        st.multiselect("Bin Type Selection", sorted(main_df.df["Bin Type"].unique()), key= "bintype_select")
    with col6:
        st.multiselect("Fillment", main_df.df["Filled?"].unique(), key= "fillment_select")
    with col7:
        st.text_input("Enter Bins (Works with column of bins)", key= "bin_select")

    met_df = Data(bin_breakdown_df)
    with col8:
        with st.container(vertical_alignment="bottom",horizontal_alignment="center",height="stretch"):
            if st.button("Execute Filters"):
                bin_breakdown_df = main_df.get_all_bins
                if st.session_state["aisle_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Zone"].isin(st.session_state["aisle_select"])]
                if st.session_state["zone_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Area"].isin(st.session_state["zone_select"])]
                if st.session_state["fillment_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Filled?"].isin(st.session_state["fillment_select"])]
                if st.session_state["bin_select"]:
                    ui_list = Data.InputToList(st.session_state["bin_select"])
                    ui_list = [x.upper() for x in ui_list]
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Bins"].isin(ui_list)]
                if st.session_state["level_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Level"].isin(st.session_state["level_select"])]
                if st.session_state["bintype_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Bin Type"].isin(st.session_state["bintype_select"])]
                if st.session_state["zone_type_select"]:
                    bin_breakdown_df = bin_breakdown_df[bin_breakdown_df["Zone Type"].isin(st.session_state["zone_type_select"])] 
                # st.session_state["OpenBins"] = FindOpenBins(bin_breakdown_df)
                met_df = Data(bin_breakdown_df)  
            else:
                bin_breakdown_df = main_df.get_all_bins

    
    # original numbers for metric section this will change based on a rerun from the execute filters button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(horizontal_alignment="center",width=1000):
            col1,col2,col3 = st.columns(3)
            with col1:
                st.metric("Available Alternates",len(met_df.get_available_alternates),border= True)
                st.metric("Total Alternates",len(met_df.get_all_alts),border= True)
            with col2:
                st.metric("Available Primaries", len(met_df.get_available_primaries),border= True)
                st.metric("Total Primaries",len(met_df.get_all_prims),border= True)
            with col3:
                st.metric("Available Bins",len(met_df.get_available_bins),border= True)
                st.metric("Total Bins",len(met_df.get_all_bins),border= True)


    st.header("Bin Overview")
    st.dataframe(bin_breakdown_df.rename(columns= {"Zone":"Aisle"}),hide_index=True)

    item_breakdown = pd.concat([bsg.get_ofs(),bsg.get_prims()]).sort_values("BinDescription")
    item_breakdown = item_breakdown[item_breakdown["BinDescription"].isin(bin_breakdown_df["Bins"])]
    st.header("Item Overview")

    # renamer variable
    renamer = {
        "ZoneDescription1":"Aisle",
        "ItemNumber1":"ItemNumber",
        "MaximumStock2":"Max",
        "MinimumStock":"Min",
        "ALternateBinProfileName":"AlternateBinProfile",
        "UnitDisplay2":"UOM"
        }

    # column remover variable
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

    # renaming df columns
    item_breakdown = item_breakdown.rename(columns=renamer)

    # selecting columns to display
    st.dataframe(item_breakdown[rem_cols], hide_index= True)