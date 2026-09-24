import BinDataGrabber as bsg
import streamlit as st
import re
import time
from Data import Data
import pandas as pd


st.set_page_config(layout= "wide")
with st.spinner("Loading", show_time= True):

    main_df = Data(bsg.get_bin_data())
    bin_check = bsg.get_prims()
    PO_df = bsg.GetPODropFile()[["Item Number","Purchase Order Number","Quantity Ordered"]]
    PO_df = PO_df.rename(columns={"Purchase Order Number":"PO#","Quantity Ordered":"QTY Ordered"})
    PO_df = PO_df[~PO_df["Item Number"].isin(bin_check["ItemNumber1"])]

        
        
    st.header("PO Tools",text_alignment= "center")  
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"""### Last PO Drop
{bsg.GetExportTimes()["PO Drop File"]}""")
        with col2:
            po_ui = st.text_area("Trucking Schedule Parser")
            cons_pos = po_ui.upper()
            # regex for pulling PO#s
            result = re.findall(r'(?<!\d)\d{5,}(?!\d)',po_ui)
            if st.button("Force PO Parser"):
                result = re.findall(r'(?<!\d)\d{5,}(?!\d)',po_ui)            
            if st.button("Clear PO List"):
                result = []


        with col3:
            st.write("Found PO#s")
            PO_fives = [x for x in result if len(x) == 7]
            st.dataframe(pd.DataFrame({"PO#":PO_fives}),hide_index=True,height="content")
            # for j in PO_fives:
            #     st.markdown("- " + j)

        with col4:
            st.write("Non POs, possible transfers")
            PO_non_fives = [x for x in result if len(x) != 7]
            st.dataframe(pd.DataFrame({"PO#":PO_non_fives}),hide_index=True,height="content")
            # for j in PO_non_fives:
            #     st.markdown("- " + j)

        with col5:

            st.write("Items in PO drop file")
            st.dataframe(bsg.GetPODropFile()[["Item Number","Purchase Order Number","Quantity Ordered"]].rename(columns= {"Purchase Order Number":"PO","Quantity Ordered":"QTY Ordered"})
                        ,hide_index= True, width= "stretch")
    
            

    st.header("Items In PO Drop File not binned")
    st.dataframe(PO_df,hide_index= True)
    # st.header("Items In Consumable PO Drop File")
    # st.dataframe(bsg.GetConsumablePOFile()[["Item Number","Purchase Order Number","Vendor Code"]].rename(columns={"Purchase Order Number":"PO#","Quantity Ordered":"QTY Ordered"}), hide_index= True)