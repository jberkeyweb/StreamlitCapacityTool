import streamlit as st

# main_df = bsg.get_bin_data()


image_path = "Images/WebLogo.png"
st.set_page_config(layout="wide",page_icon= image_path)

pg = st.navigation(
    [
        st.Page("Pages/Welcome.py", title= "Welcome"),
        st.Page("Pages/RandomBinPicker.py", title= "Random Bin Picker"),
        st.Page("Pages/BulkBinAssigner.py", title= "Bulk Bin Assigner"),
        st.Page("Pages/BinLookup.py", title= "Bin Look Up"),
        st.Page("Pages/ItemLookUp.py", title= "Item Look Up"),
        st.Page("Pages/POTools.py",title= "POTools"),
        st.Page("Pages/FoodDataGrabber.py", title= "Shelf Life Grabber"),
        st.Page("Pages/WBStats.py", title= "WBStats"),
        st.Page("Pages/Scenarios.py", title= "Scenarios"),
        st.Page("Pages/Help.py", title="Help")
    ],
    position= "top"
)
pg.run()