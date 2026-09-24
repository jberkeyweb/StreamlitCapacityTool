import BinDataGrabber as bsg
import streamlit as st
from Data import Data
import pandas as pd



st.set_page_config(layout= "wide")
with st.spinner("Loading", show_time= True):

    main_df = Data(bsg.get_bin_data())
    st.title("Random Bin Picker")
    col1, col2, col3 = st.columns([1,.5,1])

    with col2:
        st.write("For detailed lookups please use Bin Lookup Tab")
        selection_dict = {
        zone: f"{zone} - {bins}"
        for zone, bins in zip(main_df.SummarizeAvailablePrimaries()["Zone"], main_df.SummarizeAvailablePrimaries()["Bins"])
        }
        # using a dict to add ease of visibility to how many bins are open on the dropdown
        ui = st.selectbox("Select Aisle", selection_dict.values(),width=300)
        reverse_dict = {v:k for k, v in selection_dict.items()}
        zone = reverse_dict[ui]
        ui1 = st.text_input("Enter the amount of bins here",value=1,width= 300)

    with col3:
        level_num = main_df.SummarizeAvailablePrimsByLevel()
        # this dataframe logic can be taken out
        level_num = level_num[level_num.index.get_level_values("Zone") == reverse_dict[ui]]
        level_num_df = pd.DataFrame({
            "Level":level_num.index.get_level_values("Level"),
            "Bins":level_num.values})
        level_num_dict = level_num_df.to_dict()
        level_num_dict1 = {f"{x} - {y}":x for x,y in zip(level_num_dict["Level"].values(),level_num_dict["Bins"].values())}
        level_list = ["All"]
        for x in level_num_dict1.keys():
            level_list.append(x)
        level_select = st.radio("Level Select",level_list)
        if level_select != "All":
            level_select = level_num_dict1[level_select]
        else:
            level_select = "All"
            

    with col1:  
        st.dataframe(main_df.SummarizeAvailablePrimaries(),hide_index=True,height="content",width= 600)

    with col2:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                random_button = st.button("Random Bins")
            with col2:
                show_all_button = st.button("Show All")

        if random_button:
            bins = main_df.RandomBinPickerStreamLit(zone,int(ui1),level_select)
            st.dataframe(bins,height= "content", hide_index= True)      

        if show_all_button:
            st.dataframe(main_df.df[(main_df.df["Zone"]==zone) & (main_df.df["Filled?"]=="Available") & (main_df.df["Bin Type"].str.contains("PRIM"))][["Bins","Bin Type"]],height= "content", hide_index= True)