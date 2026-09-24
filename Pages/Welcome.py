import BinDataGrabber as bsg
import WrongZone as wz
import streamlit as st
import CapacityReport
import SinglePalletConsScript as sp

st.set_page_config(layout= "wide")
with st.spinner("Loading", show_time= True):
    st.title("Welcome to the PP/Analysis Tool!",text_alignment= "center")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text("This streamlit app is used as a PPTool and to answer general DC Analysis questions. Please use this page below or the top navigation bar to go to different pages.",
                 text_alignment= "center")
        if st.button("Pull Random Bins", width= "stretch"):
            st.switch_page("Pages/RandomBinPicker.py")
        if st.button("Bulk Bin Assingment", width= "stretch"):
            st.switch_page("Pages/BulkBinAssigner.py")
        if st.button("In Depth Bin Lookup", width= "stretch"):
            st.switch_page("Pages/BinLookup.py")
        if st.button("In Depth Item Lookup", width= "stretch"):
            st.switch_page("Pages/ItemLookUp.py")
        if st.button("PO Truck Schedule Parser/PO No Bin Lookup", width= "stretch"):
            st.switch_page("Pages/POTools.py")
        if st.button("Shelf Life Grabber", width= "stretch"):
            st.switch_page("Pages/FoodDataGrabber.py")            
        if st.button("WBStats", width= "stretch"):
            st.switch_page("Pages/WBStats.py")
        if st.button("Scenarios", width= "stretch"):
            st.switch_page("Pages/Scenarios.py")
    with col2:
        st.header("Export Times", text_alignment= "center")

            # st.header(f"{x} : {y}",text_alignment= "center")

    with col3:
        st.header("CSV/Script Button")
        if st.button("Press to execute labor scripts"):
            sp.main()
            wz.main()
            bsg.save_csvs()
        if st.button("Run Capacity Report"):
            CapacityReport.RunReport()


    with col2:
        st.markdown(f"""#### Last Execution --- {bsg.GetLastButtonExecution()["Last Execution"]}""", text_alignment="center")
        for (x, y) in bsg.GetExportTimes().items():
            st.markdown(f"""#### {x} --- {y}""",text_alignment="center")



    
