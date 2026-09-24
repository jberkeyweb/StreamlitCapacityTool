import BinDataGrabber as bsg
import streamlit as st
from Data import Data



def GetOpenBins(df:Data):
    m1 = st.metric(label= "Total Open", value= df.get_total_num_available_bins,border= True)
    m2 = st.metric(label= "Primary Open", value= df.get_total_num_available_primaries,border= True)
    m3 = st.metric(label= "Alternates Open", value= df.get_total_num_available_alts,border= True)
    return {"Total Open": m1, "Primary Open": m2,"Alternates Open": m3}

def GetFilledBins(df:Data):
    m1 = st.metric(label= "Total Filled", value= df.get_total_num_bins - df.get_total_num_available_bins,border= True)
    m2 = st.metric(label= "Primary Filled", value= df.get_total_num_primaries - df.get_total_num_available_primaries, border= True)
    m3 = st.metric(label= "Alternates Filled", value= df.get_total_num_alternates - df.get_total_num_available_alts, border= True)
    return {"Total Filled": m1, "Primary Filled": m2,"Alternates Filled": m3}

def GetTotalBins(df:Data):
    m1 = st.metric(label= "Total Bins", value= df.get_total_num_bins,border= True)
    m2 = st.metric(label= "Total Primaries", value= df.get_total_num_primaries,border= True)
    m3 = st.metric(label= "Total Alternates", value= df.get_total_num_alternates,border= True)
    return {"Total Bins": m1, "Total Primaries": m2,"Total Alternates": m3}

def GetBinPercentages(df:Data):
    """This function gets the filled % for each catergory of bin, checking for a divide by 0 scenario"""
    v0 = (
        (df.get_total_num_bins - df.get_total_num_available_bins)
        / df.get_total_num_bins
        if df.get_total_num_bins != 0
        else 0
    )
    st.metric("Filled %", f"{v0:.2%}", border=True)

    v1 = (
        (df.get_total_num_primaries - df.get_total_num_available_primaries)
        / df.get_total_num_primaries
        if df.get_total_num_primaries != 0
        else 0
    )
    st.metric("Filled %", f"{v1:.2%}", border=True)

    v2 = (
        (df.get_total_num_alternates - df.get_total_num_available_alts)
        / df.get_total_num_alternates
        if df.get_total_num_alternates != 0
        else 0
    )
    st.metric("Filled %", f"{v2:.2%}", border=True)

empty_space = f"""
<div style="height:70px; display:flex; align-items:center;">
<h2 style="margin:0;"></h2>
</div>
"""

st.set_page_config(layout= "wide")

with st.spinner("Loading", show_time= True):

    main_df = Data(bsg.get_bin_data())

    temp_dict = {}
    for x in main_df.df["Zone Type"].unique():
        temp_dict[x] = main_df.df[main_df.df["Zone Type"].str.contains(x)]
        temp_dict[x] = Data(temp_dict[x])
    
    col1, col2 = st.columns(2)
    

    

    st.title("DC Analysis", text_alignment= "center")

    st.selectbox("Zone Selector", main_df.df["Zone Type"].unique(), placeholder="Choose an Option", key="zone_select",index=None)
    st.selectbox("Bin Type Selector",["Alternate","Primary"], placeholder= "Choose an Option", key= "bin_type_select",index=None)
    st.text_input("Enter the number of bin to add (+) or delete (-)", placeholder= "Enter Number", key= "bin_math")
    but = st.button("Execture Filters")
    # if st.button("Execute Filters"):
    #     if st.session_state["zone_select"]:
    #         if st.session_state["bin_type_select"] == "Primary":


    col1, col2 = st.columns(2)
    with col1:
        st.title("Current Situation")
        analysis_breakdown_df = main_df.get_all_bins
        st.dataframe(analysis_breakdown_df,hide_index= True)
    
    col1, col2 = st.columns(2)
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8) 
    st.header("Current Situation", text_alignment= "center")   
    if but:
        if st.session_state["zone_select"]:
            if st.session_state["bin_type_select"] == "Primary":
                if st.session_state["bin_math"]:
                        
                    with col1:
                        st.header("Whole DC")
                    with col1:
                        m1 = st.metric(label= "Total Open", value= main_df.get_total_num_available_bins,border= True)
                        m2 = st.metric(label= "Primary Open", value= main_df.get_total_num_available_primaries + int(st.session_state["bin_math"]),border= True)
                        m3 = st.metric(label= "Alternates Open", value= main_df.get_total_num_available_alts,border= True)
                    with col2:
                        m4 = st.metric(label= "Total Filled", value= main_df.get_total_num_bins - main_df.get_total_num_available_bins,border= True)
                        m5 = st.metric(label= "Primary Filled", value= main_df.get_total_num_primaries - main_df.get_total_num_available_primaries, border= True)
                        m6 = st.metric(label= "Alternates Filled", value= main_df.get_total_num_alternates - main_df.get_total_num_available_alts, border= True)
                    with col3:
                        m1 = st.metric(label= "Total Bins", value= main_df.get_total_num_bins,border= True)
                        m2 = st.metric(label= "Total Primaries", value= main_df.get_total_num_primaries,border= True)
                        m3 = st.metric(label= "Total Alternates", value= main_df.get_total_num_alternates,border= True)
                    with col4:
                        v0 = (
                        (main_df.get_total_num_bins - main_df.get_total_num_available_bins)
                        / main_df.get_total_num_bins
                        if main_df.get_total_num_bins != 0
                        else 0
                        )
                        st.metric("Filled %", f"{v0:.2%}", border=True)

                        v1 = (
                            (main_df.get_total_num_primaries - main_df.get_total_num_available_primaries)
                            / main_df.get_total_num_primaries
                            if main_df.get_total_num_primaries != 0
                            else 0
                        )
                        st.metric("Filled %", f"{v1:.2%}", border=True)

                        v2 = (
                            (main_df.get_total_num_alternates - main_df.get_total_num_available_alts)
                            / main_df.get_total_num_alternates
                            if main_df.get_total_num_alternates != 0
                            else 0
                        )
                        st.metric("Filled %", f"{v2:.2%}", border=True)

    else:   
        with col1:
            st.header("Whole DC")   
            m1 = st.metric(label= "Total Open", value= main_df.get_total_num_available_bins,border= True)
            m2 = st.metric(label= "Primary Open", value= main_df.get_total_num_available_primaries,border= True)
            m3 = st.metric(label= "Alternates Open", value= main_df.get_total_num_available_alts,border= True)
        with col2:
            st.markdown(empty_space,unsafe_allow_html= True)
            m4 = st.metric(label= "Total Filled", value= main_df.get_total_num_bins - main_df.get_total_num_available_bins,border= True)
            m5 = st.metric(label= "Primary Filled", value= main_df.get_total_num_primaries - main_df.get_total_num_available_primaries, border= True)
            m6 = st.metric(label= "Alternates Filled", value= main_df.get_total_num_alternates - main_df.get_total_num_available_alts, border= True)
        with col3:
            st.markdown(empty_space,unsafe_allow_html= True)
            m1 = st.metric(label= "Total Bins", value= main_df.get_total_num_bins,border= True)
            m2 = st.metric(label= "Total Primaries", value= main_df.get_total_num_primaries,border= True)
            m3 = st.metric(label= "Total Alternates", value= main_df.get_total_num_alternates,border= True)
        with col4:
            st.markdown(empty_space,unsafe_allow_html= True)
            v0 = (
            (main_df.get_total_num_bins - main_df.get_total_num_available_bins)
            / main_df.get_total_num_bins
            if main_df.get_total_num_bins != 0
            else 0
            )
            st.metric("Filled %", f"{v0:.2%}", border=True)

            v1 = (
                (main_df.get_total_num_primaries - main_df.get_total_num_available_primaries)
                / main_df.get_total_num_primaries
                if main_df.get_total_num_primaries != 0
                else 0
            )
            st.metric("Filled %", f"{v1:.2%}", border=True)

            v2 = (
                (main_df.get_total_num_alternates - main_df.get_total_num_available_alts)
                / main_df.get_total_num_alternates
                if main_df.get_total_num_alternates != 0
                else 0
            )
            st.metric("Filled %", f"{v2:.2%}", border=True)





    for x, y in temp_dict.items():
        with col1:
            st.markdown(
            f"""
            <div style="height:70px; display:flex; align-items:center;">
                <h2 style="margin:0;">{x}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
            m1 = st.metric(label= "Total Open", value= temp_dict[x].get_total_num_available_bins,border= True)
            m2 = st.metric(label= "Primary Open", value= temp_dict[x].get_total_num_available_primaries,border= True)
            m3 = st.metric(label= "Alternates Open", value= temp_dict[x].get_total_num_available_alts,border= True)

        with col2:
            st.markdown(empty_space,unsafe_allow_html=True)
            m1 = st.metric(label= "Total Filled", value= temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins,border= True)
            m2 = st.metric(label= "Primary Filled", value= temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries, border= True)
            m3 = st.metric(label= "Alternates Filled", value= temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts, border= True)

        with col3:
            st.markdown(empty_space,unsafe_allow_html= True)
            m1 = st.metric(label= "Total Bins", value= temp_dict[x].get_total_num_bins,border= True)
            m2 = st.metric(label= "Total Primaries", value= temp_dict[x].get_total_num_primaries,border= True)
            m3 = st.metric(label= "Total Alternates", value= temp_dict[x].get_total_num_alternates,border= True)

        with col4:
            st.markdown(empty_space,unsafe_allow_html= True)
            v0 = (
                (temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins)
                / temp_dict[x].get_total_num_bins
                if temp_dict[x].get_total_num_bins != 0
                else 0
            )
            st.metric("Filled %", f"{v0:.2%}", border=True)

            v1 = (
                (temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries)
                / temp_dict[x].get_total_num_primaries
                if temp_dict[x].get_total_num_primaries != 0
                else 0
            )
            st.metric("Filled %", f"{v1:.2%}", border=True)

            v2 = (
                (temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts)
                / temp_dict[x].get_total_num_alternates
                if temp_dict[x].get_total_num_alternates != 0
                else 0
            )
            st.metric("Filled %", f"{v2:.2%}", border=True)