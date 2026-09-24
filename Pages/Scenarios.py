import BinDataGrabber as bsg
import streamlit as st
from Data import Data



empty_space = f"""
<div style="height:70px; display:flex; align-items:center;">
<h2 style="margin:0;"></h2>
</div>
"""

st.set_page_config(layout= "wide")
zone_analysis, aisle_analysis = st.tabs(["Zone Analysis", "Aisle Analysis"])

with zone_analysis:
    with st.spinner("Loading", show_time= True):

        main_df = Data(bsg.get_bin_data())

        temp_dict = {}
        for x in main_df.df["Zone Type"].unique():
            temp_dict[x] = main_df.df[main_df.df["Zone Type"].str.contains(x)]
            temp_dict[x] = Data(temp_dict[x])

            # session states to make the right side of the page scenarios
            if f"{x}_total_open" not in st.session_state:

                st.session_state[f"{x}_total_open"] = temp_dict[x].get_total_num_available_bins
                st.session_state[f"{x}_total_filled"] = temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins
                st.session_state[f"{x}_total_bins"] = temp_dict[x].get_total_num_bins

                st.session_state[f"{x}_total_p_open"] = temp_dict[x].get_total_num_available_primaries
                st.session_state[f"{x}_total_p_filled"] = temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries
                st.session_state[f"{x}_total_p_bins"] = temp_dict[x].get_total_num_primaries

                st.session_state[f"{x}_total_a_open"] = temp_dict[x].get_total_num_available_alts
                st.session_state[f"{x}_total_a_filled"] = temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts
                st.session_state[f"{x}_total_a_bins"] = temp_dict[x].get_total_num_alternates

                st.session_state[f"{x}_total_%"] = (
                (temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins)
                / temp_dict[x].get_total_num_bins
                if temp_dict[x].get_total_num_bins != 0
                else 0
                )

                st.session_state[f"{x}_p_%"] = (
                (temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries)
                / temp_dict[x].get_total_num_primaries
                if temp_dict[x].get_total_num_primaries != 0
                else 0
                )

                st.session_state[f"{x}_a_%"] = (
                (temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts)
                / temp_dict[x].get_total_num_alternates
                if temp_dict[x].get_total_num_alternates != 0
                else 0
                )


        
        st.session_state["total_open"] = main_df.get_total_num_available_bins
        st.session_state["total_filled"] = main_df.get_total_num_bins - main_df.get_total_num_available_bins
        st.session_state["total_bins"] = main_df.get_total_num_bins

        st.session_state["total_p_open"] = main_df.get_total_num_available_primaries
        st.session_state["total_p_filled"] = main_df.get_total_num_primaries - main_df.get_total_num_available_primaries
        st.session_state["total_p_bins"] = main_df.get_total_num_primaries

        st.session_state["total_a_open"] = main_df.get_total_num_available_alts
        st.session_state["total_a_filled"] = main_df.get_total_num_alternates - main_df.get_total_num_available_alts
        st.session_state["total_a_bins"] = main_df.get_total_num_alternates

        st.session_state["total_%"] = (
        (main_df.get_total_num_bins - main_df.get_total_num_available_bins)
        / main_df.get_total_num_bins
        if main_df.get_total_num_bins != 0
        else 0
        )
        st.session_state["p_%"] = (
        (main_df.get_total_num_primaries - main_df.get_total_num_available_primaries)
        / main_df.get_total_num_primaries
        if main_df.get_total_num_primaries != 0
        else 0
        )
        st.session_state["a_%"] = (
        (main_df.get_total_num_alternates - main_df.get_total_num_available_alts)
        / main_df.get_total_num_alternates
        if main_df.get_total_num_alternates != 0
        else 0
        )

        
        col1, col2 = st.columns(2)    

        st.title("Scenarios", text_alignment= "center")

        st.selectbox("Zone Selector", main_df.df["Zone Type"].unique(), placeholder="Choose an Option", key="zone_select",index=None)

        # key making for zones
        tot_p_key = f"{st.session_state["zone_select"]}_total_p_bins"
        filled_p_key = f"{st.session_state["zone_select"]}_total_p_filled"
        open_p_key = f"{st.session_state["zone_select"]}_total_p_open"
        percent_p_key = f"{st.session_state["zone_select"]}_p_%"
        tot_open_key = f"{st.session_state["zone_select"]}_total_open"
        tot_bins_key = f"{st.session_state["zone_select"]}_total_bins"
        tot_filled_bins_key = f"{st.session_state["zone_select"]}_total_filled"
        tot_percent_key = f"{st.session_state["zone_select"]}_total_%"
        filled_a_key = f"{st.session_state["zone_select"]}_total_a_filled"
        open_a_key = f"{st.session_state["zone_select"]}_total_a_open"
        tot_a_key = f"{st.session_state["zone_select"]}_total_a_bins"
        percent_a_key = f"{st.session_state["zone_select"]}_a_%"
        col1, col2, = st.columns(2)
        with col1:
            if st.button("Press to clear zone of product"):
                st.session_state[filled_p_key] = 0
                st.session_state[open_p_key] = 0
                st.session_state[open_a_key] = 0
                st.session_state[filled_a_key] = 0
                st.session_state[percent_p_key] = 0
                st.session_state[percent_a_key] = 0
                st.session_state[tot_open_key] = 0
                st.session_state[tot_filled_bins_key] = 0
                st.session_state[tot_percent_key] = 0
        with col2:
            if st.button("Press to clear zone of all total bins"):
                st.session_state[filled_p_key] = 0
                st.session_state[open_p_key] = 0
                st.session_state[open_a_key] = 0
                st.session_state[filled_a_key] = 0
                st.session_state[percent_p_key] = 0
                st.session_state[percent_a_key] = 0
                st.session_state[tot_open_key] = 0
                st.session_state[tot_filled_bins_key] = 0
                st.session_state[tot_percent_key] = 0
                st.session_state[tot_a_key] = 0
                st.session_state[tot_bins_key] = 0
                st.session_state[tot_p_key] = 0
        st.selectbox("Bin Type Selector",["Alternate","Primary"], placeholder= "Choose an Option", key= "bin_type_select",index=None)
        st.selectbox("Open or Filled?", ["Filled", "Open"], placeholder= "Pick Open or Filled to take or add from", key= "bin_fillment", index=None)
        st.text_input("Enter the number of bin to add (+) or delete (-)", placeholder= 0, key= "bin_math", value= 0)
        st.radio("Take From Totals?",["Yes","No"], key="total_input")
        but = st.button("Execute Filters")

        col1, col2 = st.columns(2)
        with col1:
            box = st.selectbox("Select a zone to look at", main_df.df["Zone Type"].unique(), key= "left_zone")
        with col2:
            box = st.selectbox("Select a zone to look at", main_df.df["Zone Type"].unique(), key= "right_zone") 
        if but:
            if st.session_state["bin_type_select"] == "Primary":
                tot_p_key = f"{st.session_state["zone_select"]}_total_p_bins"
                filled_p_key = f"{st.session_state["zone_select"]}_total_p_filled"
                open_p_key = f"{st.session_state["zone_select"]}_total_p_open"
                percent_p_key = f"{st.session_state["zone_select"]}_p_%"
                tot_open_key = f"{st.session_state["zone_select"]}_total_open"
                tot_bins_key = f"{st.session_state["zone_select"]}_total_bins"
                tot_filled_bins_key = f"{st.session_state["zone_select"]}_total_filled"
                tot_percent_key = f"{st.session_state["zone_select"]}_total_%"
                filled_a_key = f"{st.session_state["zone_select"]}_total_a_filled"
                open_a_key = f"{st.session_state["zone_select"]}_total_a_open"
                tot_a_key = f"{st.session_state["zone_select"]}_total_a_bins"        
                if st.session_state["total_input"] == "Yes":
                    st.session_state[tot_p_key] = int(st.session_state[tot_p_key]) + int(st.session_state["bin_math"])

                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    st.session_state[tot_open_key] = int(st.session_state[open_p_key]) + int(st.session_state[open_a_key])
                    st.session_state[tot_bins_key] = int(st.session_state[tot_p_key]) + int(st.session_state[tot_a_key])
                if st.session_state["bin_fillment"] == "Filled":
                    st.session_state[filled_p_key] = int(st.session_state[filled_p_key]) + int(st.session_state["bin_math"])
                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    if st.session_state[tot_p_key] > 0:
                        st.session_state[percent_p_key] = int(st.session_state[filled_p_key]) / int(st.session_state[tot_p_key]) 
                    else: 0
                    if st.session_state[tot_percent_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0

                if st.session_state["bin_fillment"] == "Open":
                    st.session_state[open_p_key] = int(st.session_state[open_p_key]) + int(st.session_state["bin_math"])
                    st.session_state[tot_open_key] = int(st.session_state[tot_open_key]) + int(st.session_state["bin_math"])
                    if st.session_state[tot_p_key] > 0:
                        st.session_state[percent_p_key] = int(st.session_state[filled_p_key]) / int(st.session_state[tot_p_key])
                    else: st.session_state[percent_p_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0




            if st.session_state["bin_type_select"] == "Alternate":
                tot_a_key = f"{st.session_state["zone_select"]}_total_a_bins"
                filled_a_key = f"{st.session_state["zone_select"]}_total_a_filled"
                open_a_key = f"{st.session_state["zone_select"]}_total_a_open"
                percent_a_key = f"{st.session_state["zone_select"]}_a_%"
                tot_open_key = f"{st.session_state["zone_select"]}_total_open"
                tot_bins_key = f"{st.session_state["zone_select"]}_total_bins"
                tot_filled_bins_key = f"{st.session_state["zone_select"]}_total_filled"
                tot_percent_key = f"{st.session_state["zone_select"]}_total_%"
                filled_p_key = f"{st.session_state["zone_select"]}_total_p_filled"
                open_p_key = f"{st.session_state["zone_select"]}_total_p_open"
                tot_p_key = f"{st.session_state["zone_select"]}_total_p_bins"
                if st.session_state["total_input"] == "Yes":
                    st.session_state[tot_a_key] = int(st.session_state[tot_a_key]) + int(st.session_state["bin_math"])

                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    st.session_state[tot_open_key] = int(st.session_state[open_p_key]) + int(st.session_state[open_a_key])
                    st.session_state[tot_bins_key] = int(st.session_state[tot_p_key]) + int(st.session_state[tot_a_key])
                if st.session_state["bin_fillment"] == "Filled":
                    st.session_state[filled_a_key] = int(st.session_state[filled_a_key]) + int(st.session_state["bin_math"])
                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    if st.session_state[tot_a_key] > 0:
                        st.session_state[percent_a_key] = int(st.session_state[filled_a_key]) / int(st.session_state[tot_a_key])
                    else: st.session_state[percent_a_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0

                if st.session_state["bin_fillment"] == "Open":
                    st.session_state[open_a_key] = int(st.session_state[open_a_key]) + int(st.session_state["bin_math"])
                    st.session_state[tot_open_key] = int(st.session_state[tot_open_key]) + int(st.session_state["bin_math"])
                    if st.session_state[tot_a_key] > 0:
                        st.session_state[percent_a_key] = int(st.session_state[filled_a_key]) / int(st.session_state[tot_a_key])
                    else: st.session_state[percent_a_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0

        # comparison left side
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

        total_open_key = f"{st.session_state["left_zone"]}_total_open"
        primary_open_key = f"{st.session_state["left_zone"]}_total_p_open"
        alternates_open_key = f"{st.session_state["left_zone"]}_total_a_open"
        total_filled_key = f"{st.session_state["left_zone"]}_total_filled"
        primary_filled_key = f"{st.session_state["left_zone"]}_total_p_filled"
        alternate_filled_key = f"{st.session_state["left_zone"]}_total_a_filled"
        total_bins_key = f"{st.session_state["left_zone"]}_total_bins"
        primary_total_key = f"{st.session_state["left_zone"]}_total_p_bins"
        alternate_total_key = f"{st.session_state["left_zone"]}_total_a_bins"
        total_percent_key = f"{st.session_state["left_zone"]}_total_%"
        primary_percent_key = f"{st.session_state["left_zone"]}_p_%"
        alternate_percent_key = f"{st.session_state["left_zone"]}_a_%"
        with col1:
            st.markdown(
            f"""
            <div style="height:70px; display:flex; align-items:center;">
                <h2 style="margin:0;">{st.session_state["left_zone"]}</h2>
            </div>
            """,
            unsafe_allow_html=True,
            )
            st.metric("Total Open", st.session_state[total_open_key], border= True)
            st.metric("Primary Open", st.session_state[primary_open_key], border= True)
            st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
        with col2:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state[total_filled_key], border= True)
            st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
            st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
        with col3:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state[total_bins_key], border= True)
            st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
            st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
        with col4:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)


        # comparison right side
    
        total_open_key = f"{st.session_state["right_zone"]}_total_open"
        primary_open_key = f"{st.session_state["right_zone"]}_total_p_open"
        alternates_open_key = f"{st.session_state["right_zone"]}_total_a_open"
        total_filled_key = f"{st.session_state["right_zone"]}_total_filled"
        primary_filled_key = f"{st.session_state["right_zone"]}_total_p_filled"
        alternate_filled_key = f"{st.session_state["right_zone"]}_total_a_filled"
        total_bins_key = f"{st.session_state["right_zone"]}_total_bins"
        primary_total_key = f"{st.session_state["right_zone"]}_total_p_bins"
        alternate_total_key = f"{st.session_state["right_zone"]}_total_a_bins"
        total_percent_key = f"{st.session_state["right_zone"]}_total_%"
        primary_percent_key = f"{st.session_state["right_zone"]}_p_%"
        alternate_percent_key = f"{st.session_state["right_zone"]}_a_%"
        with col6:
            st.markdown(
            f"""
            <div style="height:70px; display:flex; align-items:center;">
                <h2 style="margin:0;">{st.session_state["right_zone"]}</h2>
            </div>
            """,
            unsafe_allow_html=True,
            )
            st.metric("Total Open", st.session_state[total_open_key], border= True)
            st.metric("Primary Open", st.session_state[primary_open_key], border= True)
            st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
        with col7:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state[total_filled_key], border= True)
            st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
            st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
        with col8:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state[total_bins_key], border= True)
            st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
            st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
        with col9:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)



        col1, col2 = st.columns(2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Current Situation", text_alignment= "center")
        with col2:
            st.header("Modified Situation", text_alignment= "center")
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9) 

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




        # left side of page
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



        with col6:
            st.header("Whole DC")
            st.metric("Total Open", st.session_state["total_open"], border= True)
            st.metric("Primary Open", st.session_state["total_p_open"], border= True)
            st.metric("Alternates Open", st.session_state["total_a_open"], border= True)
        with col7:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state["total_filled"], border= True)
            st.metric("Primary Filled", st.session_state["total_p_filled"], border= True)
            st.metric("Alternates Filled", st.session_state["total_a_filled"], border= True)
        with col8:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state["total_bins"], border= True)
            st.metric("Total Primaries", st.session_state["total_p_bins"], border= True)
            st.metric("Total Alternates", st.session_state["total_a_bins"], border= True)
        with col9:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state["total_%"]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state["p_%"]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state["a_%"]:.2%}", border= True)


        # right side of the page
        # printing metrics for zones
        for x, y in temp_dict.items():

            total_open_key = f"{x}_total_open"
            primary_open_key = f"{x}_total_p_open"
            alternates_open_key = f"{x}_total_a_open"
            total_filled_key = f"{x}_total_filled"
            primary_filled_key = f"{x}_total_p_filled"
            alternate_filled_key = f"{x}_total_a_filled"
            total_bins_key = f"{x}_total_bins"
            primary_total_key = f"{x}_total_p_bins"
            alternate_total_key = f"{x}_total_a_bins"
            total_percent_key = f"{x}_total_%"
            primary_percent_key = f"{x}_p_%"
            alternate_percent_key = f"{x}_a_%"
            with col6:
                st.markdown(
                f"""
                <div style="height:70px; display:flex; align-items:center;">
                    <h2 style="margin:0;">{x}</h2>
                </div>
                """,
                unsafe_allow_html=True,
                )
                st.metric("Total Open", st.session_state[total_open_key], border= True)
                st.metric("Primary Open", st.session_state[primary_open_key], border= True)
                st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
            with col7:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Total Filled", st.session_state[total_filled_key], border= True)
                st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
                st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
            with col8:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Total Bins", st.session_state[total_bins_key], border= True)
                st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
                st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
            with col9:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
                st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
                st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)


with aisle_analysis:
    with st.spinner("Loading", show_time= True):

        main_df = Data(bsg.get_bin_data())

        temp_dict = {}
        for x in main_df.df["Zone"].unique():
            temp_dict[x] = main_df.df[main_df.df["Zone"].str.contains(x)]
            temp_dict[x] = Data(temp_dict[x])

            # session states to make the right side of the page scenarios
            if f"{x}_total_open_aisle" not in st.session_state:

                st.session_state[f"{x}_total_open_aisle"] = temp_dict[x].get_total_num_available_bins
                st.session_state[f"{x}_total_filled_aisle"] = temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins
                st.session_state[f"{x}_total_bins_aisle"] = temp_dict[x].get_total_num_bins

                st.session_state[f"{x}_total_p_open_aisle"] = temp_dict[x].get_total_num_available_primaries
                st.session_state[f"{x}_total_p_filled_aisle"] = temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries
                st.session_state[f"{x}_total_p_bins_aisle"] = temp_dict[x].get_total_num_primaries

                st.session_state[f"{x}_total_a_open_aisle"] = temp_dict[x].get_total_num_available_alts
                st.session_state[f"{x}_total_a_filled_aisle"] = temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts
                st.session_state[f"{x}_total_a_bins_aisle"] = temp_dict[x].get_total_num_alternates

                st.session_state[f"{x}_total_%_aisle"] = (
                (temp_dict[x].get_total_num_bins - temp_dict[x].get_total_num_available_bins)
                / temp_dict[x].get_total_num_bins
                if temp_dict[x].get_total_num_bins != 0
                else 0
                )

                st.session_state[f"{x}_p_%_aisle"] = (
                (temp_dict[x].get_total_num_primaries - temp_dict[x].get_total_num_available_primaries)
                / temp_dict[x].get_total_num_primaries
                if temp_dict[x].get_total_num_primaries != 0
                else 0
                )

                st.session_state[f"{x}_a_%_aisle"] = (
                (temp_dict[x].get_total_num_alternates - temp_dict[x].get_total_num_available_alts)
                / temp_dict[x].get_total_num_alternates
                if temp_dict[x].get_total_num_alternates != 0
                else 0
                )


        
        st.session_state["total_open_aisle"] = main_df.get_total_num_available_bins
        st.session_state["total_filled_aisle"] = main_df.get_total_num_bins - main_df.get_total_num_available_bins
        st.session_state["total_bins_aisle"] = main_df.get_total_num_bins

        st.session_state["total_p_open_aisle"] = main_df.get_total_num_available_primaries
        st.session_state["total_p_filled_aisle"] = main_df.get_total_num_primaries - main_df.get_total_num_available_primaries
        st.session_state["total_p_bins_aisle"] = main_df.get_total_num_primaries

        st.session_state["total_a_open_aisle"] = main_df.get_total_num_available_alts
        st.session_state["total_a_filled_aisle"] = main_df.get_total_num_alternates - main_df.get_total_num_available_alts
        st.session_state["total_a_bins_aisle"] = main_df.get_total_num_alternates

        st.session_state["total_%_aisle"] = (
        (main_df.get_total_num_bins - main_df.get_total_num_available_bins)
        / main_df.get_total_num_bins
        if main_df.get_total_num_bins != 0
        else 0
        )
        st.session_state["p_%_aisle"] = (
        (main_df.get_total_num_primaries - main_df.get_total_num_available_primaries)
        / main_df.get_total_num_primaries
        if main_df.get_total_num_primaries != 0
        else 0
        )
        st.session_state["a_%_aisle"] = (
        (main_df.get_total_num_alternates - main_df.get_total_num_available_alts)
        / main_df.get_total_num_alternates
        if main_df.get_total_num_alternates != 0
        else 0
        )

        
        col1, col2 = st.columns(2)    

        st.title("Scenarios", text_alignment= "center")

        st.selectbox("Zone Selector", main_df.df["Zone"].unique(), placeholder="Choose an Option", key="zone_select_aisle",index=None)
        tot_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_bins_aisle"
        filled_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_filled_aisle"
        open_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_open_aisle"
        percent_p_key = f"{st.session_state["zone_select_aisle"]}_p_%_aisle"
        tot_open_key = f"{st.session_state["zone_select_aisle"]}_total_open_aisle"
        tot_bins_key = f"{st.session_state["zone_select_aisle"]}_total_bins_aisle"
        tot_filled_bins_key = f"{st.session_state["zone_select_aisle"]}_total_filled_aisle"
        tot_percent_key = f"{st.session_state["zone_select_aisle"]}_total_%_aisle"
        filled_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_filled_aisle"
        open_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_open_aisle"
        tot_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_bins_aisle"
        percent_a_key = f"{st.session_state["zone_select_aisle"]}_a_%_aisle"
        col1, col2, = st.columns(2)
        with col1:
            if st.button("Press to clear aisle of product"):
                st.session_state[filled_p_key] = 0
                st.session_state[open_p_key] = 0
                st.session_state[open_a_key] = 0
                st.session_state[filled_a_key] = 0
                st.session_state[percent_p_key] = 0
                st.session_state[percent_a_key] = 0
                st.session_state[tot_open_key] = 0
                st.session_state[tot_filled_bins_key] = 0
                st.session_state[tot_percent_key] = 0
        with col2:
            if st.button("Press to clear aisle of all total bins"):
                st.session_state[filled_p_key] = 0
                st.session_state[open_p_key] = 0
                st.session_state[open_a_key] = 0
                st.session_state[filled_a_key] = 0
                st.session_state[percent_p_key] = 0
                st.session_state[percent_a_key] = 0
                st.session_state[tot_open_key] = 0
                st.session_state[tot_filled_bins_key] = 0
                st.session_state[tot_percent_key] = 0
                st.session_state[tot_a_key] = 0
                st.session_state[tot_bins_key] = 0
                st.session_state[tot_p_key] = 0
        st.selectbox("Bin Type Selector",["Alternate","Primary"], placeholder= "Choose an Option", key= "bin_type_select_aisle",index=None)
        st.selectbox("Open or Filled?", ["Filled", "Open"], placeholder= "Pick Open or Filled to take or add from", key= "bin_fillment_aisle", index=None)
        st.text_input("Enter the number of bin to add (+) or delete (-)", placeholder= 0, key= "bin_math_aisle", value= 0)
        st.radio("Take From Totals?",["Yes","No"], key="total_input_aisle")
        but5 = st.button("Execute Filters",key= "execute_filter")

        col1, col2 = st.columns(2)
        with col1:
            box = st.selectbox("Select an aisle to look at", main_df.df["Zone"].unique(), key= "left_aisle")
        with col2:
            box = st.selectbox("Select an aisle to look at", main_df.df["Zone"].unique(), key= "right_aisle")            




        if but5:
            if st.session_state["bin_type_select_aisle"] == "Primary":
                tot_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_bins_aisle"
                filled_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_filled_aisle"
                open_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_open_aisle"
                percent_p_key = f"{st.session_state["zone_select_aisle"]}_p_%_aisle"
                tot_open_key = f"{st.session_state["zone_select_aisle"]}_total_open_aisle"
                tot_bins_key = f"{st.session_state["zone_select_aisle"]}_total_bins_aisle"
                tot_filled_bins_key = f"{st.session_state["zone_select_aisle"]}_total_filled_aisle"
                tot_percent_key = f"{st.session_state["zone_select_aisle"]}_total_%_aisle"
                filled_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_filled_aisle"
                open_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_open_aisle"
                tot_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_bins_aisle"        
                if st.session_state["total_input_aisle"] == "Yes":
                    st.session_state[tot_p_key] = int(st.session_state[tot_p_key]) + int(st.session_state["bin_math_aisle"])

                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    st.session_state[tot_open_key] = int(st.session_state[open_p_key]) + int(st.session_state[open_a_key])
                    st.session_state[tot_bins_key] = int(st.session_state[tot_p_key]) + int(st.session_state[tot_a_key])
                if st.session_state["bin_fillment_aisle"] == "Filled":
                    st.session_state[filled_p_key] = int(st.session_state[filled_p_key]) + int(st.session_state["bin_math_aisle"])
                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    if st.session_state[tot_p_key] > 0:
                        st.session_state[percent_p_key] = int(st.session_state[filled_p_key]) / int(st.session_state[tot_p_key]) 
                    else: 0
                    if st.session_state[tot_percent_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0

                if st.session_state["bin_fillment_aisle"] == "Open":
                    st.session_state[open_p_key] = int(st.session_state[open_p_key]) + int(st.session_state["bin_math_aisle"])
                    st.session_state[tot_open_key] = int(st.session_state[tot_open_key]) + int(st.session_state["bin_math_aisle"])
                    if st.session_state[tot_p_key] > 0:
                        st.session_state[percent_p_key] = int(st.session_state[filled_p_key]) / int(st.session_state[tot_p_key])
                    else: st.session_state[percent_p_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0



            if st.session_state["bin_type_select_aisle"] == "Alternate":
                tot_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_bins_aisle"
                filled_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_filled_aisle"
                open_a_key = f"{st.session_state["zone_select_aisle"]}_total_a_open_aisle"
                percent_a_key = f"{st.session_state["zone_select_aisle"]}_a_%_aisle"
                tot_open_key = f"{st.session_state["zone_select_aisle"]}_total_open_aisle"
                tot_bins_key = f"{st.session_state["zone_select_aisle"]}_total_bins_aisle"
                tot_filled_bins_key = f"{st.session_state["zone_select_aisle"]}_total_filled_aisle"
                tot_percent_key = f"{st.session_state["zone_select_aisle"]}_total_%_aisle"
                filled_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_filled_aisle"
                open_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_open_aisle"
                tot_p_key = f"{st.session_state["zone_select_aisle"]}_total_p_bins_aisle"
                if st.session_state["total_input_aisle"] == "Yes":
                    st.session_state[tot_a_key] = int(st.session_state[tot_a_key]) + int(st.session_state["bin_math_aisle"])

                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    st.session_state[tot_open_key] = int(st.session_state[open_p_key]) + int(st.session_state[open_a_key])
                    st.session_state[tot_bins_key] = int(st.session_state[tot_p_key]) + int(st.session_state[tot_a_key])
                if st.session_state["bin_fillment_aisle"] == "Filled":
                    st.session_state[filled_a_key] = int(st.session_state[filled_a_key]) + int(st.session_state["bin_math_aisle"])
                    st.session_state[tot_filled_bins_key] = int(st.session_state[filled_p_key]) + int(st.session_state[filled_a_key])
                    if st.session_state[tot_a_key] > 0:
                        st.session_state[percent_a_key] = int(st.session_state[filled_a_key]) / int(st.session_state[tot_a_key])
                    else: st.session_state[percent_a_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0

                if st.session_state["bin_fillment_aisle"] == "Open":
                    st.session_state[open_a_key] = int(st.session_state[open_a_key]) + int(st.session_state["bin_math_aisle"])
                    st.session_state[tot_open_key] = int(st.session_state[tot_open_key]) + int(st.session_state["bin_math_aisle"])
                    if st.session_state[tot_a_key] > 0:
                        st.session_state[percent_a_key] = int(st.session_state[filled_a_key]) / int(st.session_state[tot_a_key])
                    else: st.session_state[percent_a_key] = 0
                    if st.session_state[tot_bins_key] > 0:
                        st.session_state[tot_percent_key] = int(st.session_state[tot_filled_bins_key]) / int(st.session_state[tot_bins_key])
                    else: st.session_state[tot_percent_key] = 0





        # comparison left side
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

        total_open_key = f"{st.session_state["left_aisle"]}_total_open_aisle"
        primary_open_key = f"{st.session_state["left_aisle"]}_total_p_open_aisle"
        alternates_open_key = f"{st.session_state["left_aisle"]}_total_a_open_aisle"
        total_filled_key = f"{st.session_state["left_aisle"]}_total_filled_aisle"
        primary_filled_key = f"{st.session_state["left_aisle"]}_total_p_filled_aisle"
        alternate_filled_key = f"{st.session_state["left_aisle"]}_total_a_filled_aisle"
        total_bins_key = f"{st.session_state["left_aisle"]}_total_bins_aisle"
        primary_total_key = f"{st.session_state["left_aisle"]}_total_p_bins_aisle"
        alternate_total_key = f"{st.session_state["left_aisle"]}_total_a_bins_aisle"
        total_percent_key = f"{st.session_state["left_aisle"]}_total_%_aisle"
        primary_percent_key = f"{st.session_state["left_aisle"]}_p_%_aisle"
        alternate_percent_key = f"{st.session_state["left_aisle"]}_a_%_aisle"
        with col1:
            st.markdown(
            f"""
            <div style="height:70px; display:flex; align-items:center;">
                <h2 style="margin:0;">{st.session_state["left_aisle"]}</h2>
            </div>
            """,
            unsafe_allow_html=True,
            )
            st.metric("Total Open", st.session_state[total_open_key], border= True)
            st.metric("Primary Open", st.session_state[primary_open_key], border= True)
            st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
        with col2:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state[total_filled_key], border= True)
            st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
            st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
        with col3:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state[total_bins_key], border= True)
            st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
            st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
        with col4:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)


        # comparison right side
    
        total_open_key = f"{st.session_state["right_aisle"]}_total_open_aisle"
        primary_open_key = f"{st.session_state["right_aisle"]}_total_p_open_aisle"
        alternates_open_key = f"{st.session_state["right_aisle"]}_total_a_open_aisle"
        total_filled_key = f"{st.session_state["right_aisle"]}_total_filled_aisle"
        primary_filled_key = f"{st.session_state["right_aisle"]}_total_p_filled_aisle"
        alternate_filled_key = f"{st.session_state["right_aisle"]}_total_a_filled_aisle"
        total_bins_key = f"{st.session_state["right_aisle"]}_total_bins_aisle"
        primary_total_key = f"{st.session_state["right_aisle"]}_total_p_bins_aisle"
        alternate_total_key = f"{st.session_state["right_aisle"]}_total_a_bins_aisle"
        total_percent_key = f"{st.session_state["right_aisle"]}_total_%_aisle"
        primary_percent_key = f"{st.session_state["right_aisle"]}_p_%_aisle"
        alternate_percent_key = f"{st.session_state["right_aisle"]}_a_%_aisle"
        with col6:
            st.markdown(
            f"""
            <div style="height:70px; display:flex; align-items:center;">
                <h2 style="margin:0;">{st.session_state["right_aisle"]}</h2>
            </div>
            """,
            unsafe_allow_html=True,
            )
            st.metric("Total Open", st.session_state[total_open_key], border= True)
            st.metric("Primary Open", st.session_state[primary_open_key], border= True)
            st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
        with col7:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state[total_filled_key], border= True)
            st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
            st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
        with col8:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state[total_bins_key], border= True)
            st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
            st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
        with col9:
            st.markdown(empty_space,unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)

        col1, col2 = st.columns(2)
        with col1:
            st.header("Current Situation", text_alignment= "center")
        with col2:
            st.header("Modified Situation", text_alignment= "center")



        col1, col2 = st.columns(2)
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9) 

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




        # left side of page
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



        with col6:
            st.header("Whole DC")
            st.metric("Total Open", st.session_state["total_open"], border= True)
            st.metric("Primary Open", st.session_state["total_p_open"], border= True)
            st.metric("Alternates Open", st.session_state["total_a_open"], border= True)
        with col7:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Total Filled", st.session_state["total_filled"], border= True)
            st.metric("Primary Filled", st.session_state["total_p_filled"], border= True)
            st.metric("Alternates Filled", st.session_state["total_a_filled"], border= True)
        with col8:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Total Bins", st.session_state["total_bins"], border= True)
            st.metric("Total Primaries", st.session_state["total_p_bins"], border= True)
            st.metric("Total Alternates", st.session_state["total_a_bins"], border= True)
        with col9:
            st.markdown(empty_space, unsafe_allow_html= True)
            st.metric("Filled %", f"{st.session_state["total_%"]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state["p_%"]:.2%}", border= True)
            st.metric("Filled %", f"{st.session_state["a_%"]:.2%}", border= True)


        # right side of the page
        # printing metrics for aisles using st.sessionstate to change inputs
        for x, y in temp_dict.items():

            total_open_key = f"{x}_total_open_aisle"
            primary_open_key = f"{x}_total_p_open_aisle"
            alternates_open_key = f"{x}_total_a_open_aisle"
            total_filled_key = f"{x}_total_filled_aisle"
            primary_filled_key = f"{x}_total_p_filled_aisle"
            alternate_filled_key = f"{x}_total_a_filled_aisle"
            total_bins_key = f"{x}_total_bins_aisle"
            primary_total_key = f"{x}_total_p_bins_aisle"
            alternate_total_key = f"{x}_total_a_bins_aisle"
            total_percent_key = f"{x}_total_%_aisle"
            primary_percent_key = f"{x}_p_%_aisle"
            alternate_percent_key = f"{x}_a_%_aisle"
            with col6:
                st.markdown(
                f"""
                <div style="height:70px; display:flex; align-items:center;">
                    <h2 style="margin:0;">{x}</h2>
                </div>
                """,
                unsafe_allow_html=True,
                )
                st.metric("Total Open", st.session_state[total_open_key], border= True)
                st.metric("Primary Open", st.session_state[primary_open_key], border= True)
                st.metric("Alternates Open", st.session_state[alternates_open_key], border= True)
            with col7:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Total Filled", st.session_state[total_filled_key], border= True)
                st.metric("Primary Filled", st.session_state[primary_filled_key], border= True)
                st.metric("Alternates Filled", st.session_state[alternate_filled_key], border= True)
            with col8:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Total Bins", st.session_state[total_bins_key], border= True)
                st.metric("Total Primaries", st.session_state[primary_total_key], border= True)
                st.metric("Total Alternates", st.session_state[alternate_total_key], border= True)
            with col9:
                st.markdown(empty_space,unsafe_allow_html= True)
                st.metric("Filled %", f"{st.session_state[total_percent_key]:.2%}", border= True)
                st.metric("Filled %", f"{st.session_state[primary_percent_key]:.2%}", border= True)
                st.metric("Filled %", f"{st.session_state[alternate_percent_key]:.2%}", border= True)