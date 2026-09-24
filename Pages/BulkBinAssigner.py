import BinDataGrabber as bsg
import streamlit as st
from Data import Data


st.set_page_config(layout= "wide")
output_path = "OutputFiles/BulkBinAssigner.xlsx"
with st.spinner("Loading",show_time= True):
    main_df = Data(bsg.get_bin_data())
    st.title("Bulk Bin Assignment")
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(main_df.SummarizeAvailablePrimaries().rename(
            columns={"Zone":"Aisle"}),hide_index=True,height="content")

    with col2:
        # bulk bin assigner input
        ui = st.text_area("Input list with 2 columns [Aisle, ItemNumber]",height="content")
        ui = [x.split("\t") for x in ui.splitlines()]
        # flattens nested list
        ui = [item for sublist in ui for item in sublist]
        temp_df = main_df.BulkItemAssignmentStreamlit(ui)
        if st.button("Export to CSV"):
            temp_df.to_excel(output_path,index=False)
        st.dataframe(temp_df,hide_index= True,height= "content")
        if len(ui) != 0 and (temp_df is None or temp_df.empty):
            st.error("No available bins found or bins are out of range.")