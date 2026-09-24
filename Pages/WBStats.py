import BinDataGrabber as bsg
import pandas as pd
import streamlit as st
from datetime import date as dt
from Data import Data


st.set_page_config(layout= "wide")
with st.spinner("Loading",show_time=True):
    st.header(dt.today().strftime("%x"), text_alignment= "center")
    main_df = Data(bsg.get_bin_data())
    # making DF for WBStats
    zone_summary = main_df.ZoneSummary()
    # main df to pull from for primaries
    zone_gb_prim_no_chem_no_ds = zone_summary[(zone_summary["Bin Type"].str.contains("PRIM")) & 
                            (zone_summary["Filled?"] == "Available") & 
                            (~zone_summary["Zone"].str.contains("CHEM")) &
                            (~zone_summary["Zone"].str.contains("DEAD"))].groupby("Zone Type").count()["Bins"]
    # making DF for deadstock bins
    zone_ds = zone_summary[(zone_summary["Zone"].str.contains("DEAD")) &
                            (zone_summary["Filled?"] == "Available") &
                            (zone_summary["Bin Type"].str.contains("PRIM"))].groupby("Zone Type").count()["Bins"]
    # making DF for chem bins
    chem_df = zone_summary[(zone_summary["Zone"].str.contains("CHEM")) &
                            (zone_summary["Filled?"] == "Available") &
                            (zone_summary["Bin Type"].str.contains("PRIM"))].groupby("Zone Type").count()["Bins"]

    zone_gb_alt = zone_summary[
        (zone_summary["Bin Type"].str.contains("ALT")) &
        (zone_summary["Filled?"] == "Available")
        ].groupby("Zone Type").count()["Bins"]

    # df made for alternates in 6s and 8s
    zone_gb_alt_6000_8000 = zone_summary[
        (zone_summary["Bin Type"].str.contains("ALT")) &
        (zone_summary["Filled?"] == "Available") &
        (zone_summary["Bins"].str.len() == 6)
        ].groupby("Zone Type").count()["Bins"]

    # df to deal with children bins
    zone_gb_8000_children = zone_summary[
        (zone_summary["Zone"].str.contains("BULK")) &
        (~zone_summary["Zone"].str.contains("'")) &
        (zone_summary["Bin Type"].str.contains("ALT")) &
        (zone_summary["Bins"].str.len() == 6) &
        (zone_summary["Filled?"] == "Available")
    ]

    # main df to be shown
    wbstats_prim_df = pd.DataFrame(
        [
            ["1000/2000s 7FT", zone_gb_prim_no_chem_no_ds.loc["1s, 2s 7'"]],
            ["2000/3000s 4FT", zone_gb_prim_no_chem_no_ds.loc["1s, 3s 4'"] + zone_gb_prim_no_chem_no_ds.loc["2s 4'"]],
            ["2000/3000s 2FT", zone_gb_prim_no_chem_no_ds.loc["2s, 3s 2'"]],
            ["2000s 9FT", zone_gb_prim_no_chem_no_ds.loc["1s, 2s 9'"]],
            ["3000s Deadstock", zone_ds.loc["2s, 3s 2'"]],
            ["3000s Bus Tub",zone_gb_prim_no_chem_no_ds.loc["3s BB"]],
            ["5000s 7FT", zone_gb_prim_no_chem_no_ds.loc["5s, 7s 7'"]],
            ["Food 5FT", zone_gb_prim_no_chem_no_ds.loc["5s, 7s FOOD 5'"]],
            ["Food 2FT", zone_gb_prim_no_chem_no_ds.loc["5s, 7s FOOD 2'"]],
            ["Food BB", zone_gb_prim_no_chem_no_ds.loc["5s, 7s FOOD BB"]],
            ["6000s 7FT", zone_gb_prim_no_chem_no_ds.loc["6s, 8s 7'"]],  # this stat will include any 8000 primary bins in that zone, there is currently none 7-2-2026
            ["6000s 4FT", zone_gb_prim_no_chem_no_ds.loc["6s 4'"]],
            ["6000s 9FT", zone_gb_prim_no_chem_no_ds["6s, 8s 9'"]], # this metric does not include 6I bins
            ["8000s 7FT", zone_gb_prim_no_chem_no_ds["8s BULK 7'"]],
            ["8000s 4FT", zone_gb_prim_no_chem_no_ds["8s BULK 4'"]],
            ["Chemical 5FT", chem_df.loc["5s, 7s 5'"]],
            ["Chemical 4FT", chem_df.loc["1s, 3s 4'"]],
            ["Chemical 2FT", chem_df.loc["2s, 3s 2'"] + chem_df.loc["5s, 7s 2'"]],
            ["4C Small Bins", zone_gb_prim_no_chem_no_ds.loc["4s SS"]],
            ["3X Gaylords", zone_gb_prim_no_chem_no_ds.loc["3s GAYLORD"]]
        ],
        columns=["Zone", "Bins"]
    ).set_index("Zone")

    wbstats_alt_df = pd.DataFrame([
        ["1000/2000s 7FT", zone_gb_alt.loc["1s, 2s 7'"]],
        ["1000/2000/3000s 4FT", zone_gb_alt.loc["1s, 3s 4'"] + zone_gb_alt.loc["2s 4'"] + zone_gb_alt.loc["2s, 3s 2'"]],
        ["2000s 9FT", zone_gb_alt.loc["1s, 2s 9'"]],
        ["5000/7000s 7FT", zone_gb_alt.loc["5s, 7s 7'"]],
        ["Food 5FT", zone_gb_alt.loc["5s, 7s FOOD 5'"]],
        ["6000/8000s 7FT", zone_gb_alt_6000_8000.loc["6s, 8s 7'"]],
        ["6000s 9FT", zone_gb_alt.loc["6s, 8s 9'"]],
        ["8000s BULK 7FT", zone_gb_alt.loc["8s BULK 7'"]],
        ["8000s BULK 4FT", zone_gb_alt.loc["8s 4'"] + zone_gb_alt.loc["8s BULK 4'"]],
        ["8000s Children (SL1 SL2)", zone_gb_8000_children["Bins"].size]
        ],
        columns= ["Zone", "Bins"]
    ).set_index("Zone")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Primary Bins", text_alignment= "center", divider= "blue")
    with col2:
        st.header("Specialized Bins", text_alignment= "center", divider= "gray")
    with col3:
        st.header("Alternate Bins", text_alignment= "center", divider= "orange")


    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("1000/2000s 7FT", wbstats_prim_df.loc["1000/2000s 7FT"], border= True)
        st.metric("2000/3000s 4FT", wbstats_prim_df.loc["2000/3000s 4FT"], border= True)
        st.metric("2000/3000s 2FT", wbstats_prim_df.loc["2000/3000s 2FT"], border= True)
        st.metric("2000s 9FT", wbstats_prim_df.loc["2000s 9FT"], border= True)
        st.metric("3000s Deadstock", wbstats_prim_df.loc["3000s Deadstock"], border= True)
        st.metric("3000s Bus Tub", wbstats_prim_df.loc["3000s Bus Tub"], border= True)
        st.metric("5000s 7FT", wbstats_prim_df.loc["5000s 7FT"], border= True)
        st.metric("Food 5FT", wbstats_prim_df.loc["Food 5FT"], border= True)
        st.metric("Food 2FT", wbstats_prim_df.loc["Food 2FT"], border= True)

    with col2:
        st.metric("Food BB", wbstats_prim_df.loc["Food BB"], border= True)
        st.metric("6000s 7FT", wbstats_prim_df.loc["6000s 7FT"], border= True)
        st.metric("6000s 4FT", wbstats_prim_df.loc["6000s 4FT"], border= True)
        st.metric("6000s 9FT", wbstats_prim_df.loc["6000s 9FT"], border= True)
        st.metric("8000s 7FT", wbstats_prim_df.loc["8000s 7FT"], border= True)
        st.metric("8000s 4FT", wbstats_prim_df.loc["8000s 4FT"], border= True)
        st.metric("Chemical 5FT", wbstats_prim_df.loc["Chemical 5FT"], border= True)
        st.metric("Chemical 4FT", wbstats_prim_df.loc["Chemical 4FT"], border= True)
        st.metric("Chemical 2FT", wbstats_prim_df.loc["Chemical 2FT"], border= True)

    with col5:
        st.metric("1000/2000s 7FT", wbstats_alt_df.loc["1000/2000s 7FT"], border= True)
        st.metric("1000/2000/3000s 4FT", wbstats_alt_df.loc["1000/2000/3000s 4FT"], border= True)
        st.metric("2000s 9FT", wbstats_alt_df.loc["2000s 9FT"], border= True)
        st.metric("5000/7000s 7FT", wbstats_alt_df.loc["5000/7000s 7FT"], border= True)
        st.metric("Food 5FT", wbstats_alt_df.loc["Food 5FT"], border= True)
        st.metric("6000/8000s 7FT", wbstats_alt_df.loc["6000/8000s 7FT"], border= True)
        st.metric("6000s 9FT", wbstats_alt_df.loc["6000s 9FT"], border= True)
        st.metric("8000s BULK 7FT", wbstats_alt_df.loc["8000s BULK 7FT"], border= True)
        st.metric("8000s BULK 4FT", wbstats_alt_df.loc["8000s BULK 4FT"], border= True)
    with col6:
        st.metric("8000s Children", wbstats_alt_df.loc["8000s Children (SL1 SL2)"], border= True)
        for x in range(21):
            st.metric(" ","")
            
    with col3:
        st.metric("4C Small Bins", wbstats_prim_df.loc["4C Small Bins"], border= True)
        st.metric("3X Gaylords", wbstats_prim_df.loc["3X Gaylords"], border= True)



    # st.dataframe(wbstats_prim_df,height= "content")
    # st.dataframe(wbstats_alt_df)
