import streamlit as st
welcome, random_bin_picker, bulk_bin_assigner, bin_lookup, item_lookup, POTools, shelf_life_grabber, WBStats, scenarios = st.tabs(
    ["Welcome", 
     "Random Bin Picker",
     "Bulk Bin Assinger",
     "Bin Look Up",
     "Item Look Up",
     "PO Tools",
     "Shelf Life Grabber",
     "WBStats",
     "Scenarios"]
    )

# This page is made as help page for this project

tabs = [welcome, random_bin_picker, bulk_bin_assigner, bin_lookup, item_lookup, POTools, shelf_life_grabber, WBStats, scenarios]

for tab in tabs:
    with tab:
        st.header("This tab is intended to be a guide on how to use each tab in this tool", text_alignment="center")

with welcome:
    co1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            st.write("This tool is intended to be a way quick to pull data and bin items within the DC")
            st.write("Data is pulled from the RestaurantStore file server")
            st.write("All written exported data from this project is stored within the parent project folder in OutputFiles folder")
            st.write("Switch between dark and light mode by clicking the 3 dots in the top right")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border= True, horizontal_alignment="center",vertical_alignment="center",width= 700):
            st.markdown(
                """
                <div style="
                    height: 155px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                ">
                    Used for page navigation
                </div>
                """,
                unsafe_allow_html=True
            )
    with col2:
        with st.container(border= True, horizontal_alignment="center",vertical_alignment="center",width= 700):
            st.markdown(
                """
                <div style="
                    height: 155px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                ">
                    Shows the latest export times used in this tool
                </div>
                """,
                unsafe_allow_html=True
            )
    with col3:
        with st.container(border= True, horizontal_alignment="center",vertical_alignment="center",width= 700):
            st.markdown(
                """
                <div style="
                    height: 155px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                ">
                    Buttons to run different scripts<br><br>
                    Labor Scripts runs and saves background 2ft labor and consolidation reports<br><br>
                    Run Capacity Report saves and opens an excel file containing a breakdown of capacity
                </div>
                """,
                unsafe_allow_html=True
            )
    with st.container(border= True):        
        st.image("Images/WelcomeImage1.jpg",width= "stretch")

with random_bin_picker:
    col1, col2, col3, col4 = st.columns([1,3,2,1])
    with col2:
        with st.container(border= True):
            st.image("Images/RandomBinPicker.jpg")
    with col3:
        with st.container(border= True,width=420):
            st.write("This tab is used to pull random bins from a specific aisle")
            st.write("Amount of bins within the aisle are labeled after the aisle")
            st.write("Select desired aisle, enter amount of wanted bins, and press 'Random Bins'")
            st.write("Select a level as desired, these are also labeled with the amount of bins available")

with bulk_bin_assigner:
    col1, col2 = st.columns([3,1])
    with col1:
        with st.container(border=True):
            st.image("Images/BulkBinAssigner.jpg")
    with col2:
        with st.container(border=True):
            st.write("This tab is used as a bulk bin assigner template")
            st.write("Match a list of items with a list of aisles that you would like the specified item to be binned in and click out of the input")
            st.write("EX.<br>2F-7' 711POPCORN<br>6A - 9' 711BUCKET",unsafe_allow_html= True)
            st.write("It is easier to copy and paste the outputted table into an excel document and skipping 'Export to CSV'")

with bin_lookup:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border= True):
            st.image("Images/BinLookUp1.jpg")
            st.image("Images/BinLookup2.jpg")
            st.image("Images/BinLookup3.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab is used for analysis on our bins, showing availablity and items associated with bins if applicable")
            st.write("Use dropdowns to filter data acting as slicers, hit 'Execute Filters' after to filter data")
            st.write("Bin Overview and Item Overview will filter after loading, you can use this as a specfic lookup for what an aisle has in it")
            st.write("Shows: ")
            st.write("- Associated bins and fillment")
            st.write("- Items associated with specified filter")
            st.write("- Capacity within specified filter")
            st.write("Easily copy and paste from these tables into excel as needed")

with item_lookup:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border= True):
            st.image("Images/ItemLookUp1.jpg")
            st.image("Images/ItemLookUp2.jpg")
            st.image("Images/ItemLookUp3.jpg")
            st.image("Images/ItemLookUp4.jpg")
            st.image("Images/ItemLookUp5.jpg")
            st.image("Images/ItemLookUp6.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab acts as a data lookup for a list of specified items")
            st.write("Shows: ")
            st.write("- Item is binned/not binned")
            st.write("- All Primary and OF info for items")
            st.write("- Associated breakdowns")
            st.write("A full primary and overflow export is at the bottom of this tab for ease of access to these files as needed")

with POTools:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border= True):
            st.image("Images/POTools1.jpg")
            st.image("Images/POTools2.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab acts as a PO Tool for parsing POs from the truck schedule and finding non binned items contained within those POs")
            st.write("Copy/Paste truck schedule into text box and click out of it, Found POs will populate with found POs from parser")
            st.write("Continue with normal process of putting POs into PBI report to get the PO Drop file and save")
            st.write("After page refresh, 'Items In PO Drop File not binned' will populate with non binned items")
            st.write("Shows: ")
            st.write("- Last PO Drop file save")
            st.write("- Found POs from truck schedule")
            st.write("- All Items in drop file")
            st.write("- Item in PO Drop file not binned")

with shelf_life_grabber:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border=True):
            st.image("Images/ShelfLifeGrabber1.jpg")
        with st.container(border= True):
            st.image("Images/ShelfLifeGrabber2.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab is used to pull the shelf lifes for specified items")
            st.write("Enter a list of item numbers into the text box")
            st.write("Press 'Press for Excel Report' to bring up a made excel report with the shelf lifes, printing options are already set up for optimal layout")

with WBStats:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border= True):
            st.image("Images/WBStats1.jpg")
            st.image("Images/WBStats2.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab's sole purpose is to be able to easily print a page containing all stats for the white board behind PP Desk")

with scenarios:
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container(border= True):
            st.image("Images/Scenarios1.jpg")
            st.image("Images/Scenarios2.jpg")
            st.image("Images/Scenarios3.jpg")
            st.image("Images/Scenarios4.jpg")
    with col2:
        with st.container(border= True):
            st.write("This tab's purpose is to act as a scenario calculator for movement or layout changes within the DC")
            st.write("Select a zone that you would like to manipulate and start using the slicers as needed")
            st.write("User is able to manipulate the amount of open/filled bins by alternate/primary")
            st.write("This tab will keep manipulated data until tool refresh happens allowing users to look at many different zones and scenarios at one time")