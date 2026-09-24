# Setup
 
1. Install Python 3.14.0  
https://www.python.org/downloads/release/python-3140/
<br>

2. Download the project folder into new folder on desktop:
 
   >(server)\Tools\Python Scripts\PPToolAnalysisStreamlitAppPGNAV

   or

   >git clone https://github.com/jberkeyweb/StreamlitCapacityTool

   (Copy all files into new project folder on desktop)
<br>

3. Open Command Prompt and Navigate into the project folder you just made:
 
   >cd (desktop\newprojectfoldername) 
   
   Do not use the directory above
<br>

4. Create a virtual environment:
 
   >py -m venv venv  
     
   or

   >python -m venv venv

<br>

5. Activate it:
 
   >venv\Scripts\activate

<br>

6. Install dependencies:
 
   >pip install -r requirements.txt


# Using the app

### Starting the app
1. Open a command prompt window

2. Navigate to directory containing project

3. Activate venv using venv\scripts\activate

   You should now see (venv) in front of the directory you are in<br></p>
   EX.  
   >(venv) C:\Users\jberkey\Desktop\Python Scripts\StreamlitCapacityTool
<br>

4. Run the "dir" command to bring up a list of files in the current directory

5. Copy the "PPToolAnalysisStreamlit.py" file

6. Run command Streamlit run PPToolAnalysisStreamlit.py

7. If prompted for email, press enter with nothing entered, this will allow the app to start

### General Use

1. This tool will auto refresh after a page refresh or page navigation (All code is executed within the page while navigating)

2. Dark and light modes are enabled and can be changed by clicking the 3 dots in the top left of the app at any time

3. All output files or made excel reports within the app are stored within the project folder directory project/OutputFiles

# Setup
 
1. Install Python 3.14.0  
https://www.python.org/downloads/release/python-3140/
<br>

2. Download the project folder into new folder on desktop:
 
   >Found in Server files

   (Copy all files into new project folder on desktop)
<br>

3. Open Command Prompt and Navigate into the project folder you just made:
 
   >cd (desktop\newprojectfoldername) 
   
   Do not use the directory above
<br>

4. Create a virtual environment:
 
   >py -m venv venv  
     
   or

   >python -m venv venv

<br>

5. Activate it:
 
   >venv\Scripts\activate

<br>

6. Install dependencies:
 
   >pip install -r requirements.txt

7. You must create a .env file in your project directory, this should have a variable name "SERVER_FILES" connected to the desired directory where readable CSVs and some output exist.


# Using the app

### Starting the app
1. Open a command prompt window

2. Navigate to directory containing project

3. Activate venv using venv\scripts\activate

   You should now see (venv) in front of the directory you are in<br></p>
   EX.  
   >(venv) C:\Users\jberkey\Desktop\Python Scripts\StreamlitCapacityTool
<br>

4. Run the "dir" command to bring up a list of files in the current directory

5. Copy the "PPToolAnalysisStreamlit.py" file

6. Run command Streamlit run PPToolAnalysisStreamlit.py

7. If prompted for email, press enter with nothing entered, this will allow the app to start

### General Use

1. This tool will auto refresh after a page refresh or page navigation (All code is executed within the page while navigating)

2. Dark and light modes are enabled and can be changed by clicking the 3 dots in the top left of the app at any time

3. All output files or made excel reports within the app are stored within the project folder directory project/OutputFiles
   
# Useful Directories
### Full Project Directory  
```
StreamlitCapacityTool/
├── .git                         # Git repository
├── .streamlit/
│   └── config.toml              # Config file containing themes
├── Images/                      # Images used in app
│   ├── BinLookUp1.jpg
│   ├── BinLookUp2.jpg
│   ├── BinLookUp3.jpg
│   ├── BulkBinAssigner.jpg
│   ├── ItemLookUp1.jpg
│   ├── ItemLookUp2.jpg
│   ├── ItemLookUp3.jpg
│   ├── ItemLookUp4.jpg
│   ├── ItemLookUp5.jpg
│   ├── ItemLookUp6.jpg
│   ├── POTools1.jpg
│   ├── POTools2.jpg
│   ├── RandomBinPicker.jpg
│   ├── Scenarios1.jpg
│   ├── Scenarios2.jpg
│   ├── Scenarios3.jpg
│   ├── Scenarios4.jpg
│   ├── ShelfLifeGrabber1.jpg
│   ├── ShelfLifeGrabber2.jpg
│   ├── WBStats1.jpg
│   ├── WBStats2.jpg
│   ├── WebLogo.png
│   └── WelcomeImage1.jpg
├── OutputFiles/                 # Generated excel files
│   ├── BulkBinAssigner.xlsx
│   ├── CapacityReport.xlsx
│   └── ShelfLifeGrabber.xlsx
├── Pages/                       # Streamlit pages used in app
│   ├── BinLookup.py
│   ├── BulkBinAssigner.py
│   ├── DCAnalysis.py
│   ├── FoodDataGrabber.py
│   ├── Help.py
│   ├── ItemLookUp.py
│   ├── PlayingField.py
│   ├── POTools.py
│   ├── RandomBinPicker.py
│   ├── Scenarios.py
│   ├── WBStats.py
│   └── Welcome.py
├── venv                         # Local Python virtual enviroment (not committed)
├── .env                         # Local enviroment variable (not committed)
├── BinDataGrabber.py            # Bin data extraction
├── CapacityReport.py            # Capacity Report Generation
├── Data.py                      # Core class for data processing
├── PPToolAnalysisStreamlit.py   # Application entry point
├── README.md                    # Documentaion
├── requirements.txt             # Python package depndencies
├── SinglePalletConsScript.py    # Consolidation analysis
└── WrongZone.py                 # Wrong Zone analysis
```

### Server Directory
```
.env Server/
├── IDS CSV Export - Overflow.csv                  # Main CSV of Alternate/Overflow Bins
├── IDS CSV Export.csv                             # Main CSV of Primary/Main Bins
├── PO Drop File.xlsx                              # xlsx of items coming in on POs
├── Data/
│   └── CSVData/                                   # Extra CSV data
│       ├── BinData.csv
│       ├── ItemShippingAttributes.csv
│       ├── Item Breakdowns.csv
│       ├── ItemHandlingAttributes.csv
│       └── ItemShippingAttributes.csv
├── HistoryData/
│   ├── Primary History/                           # Primary History, gets auto-saved in app
│   │   └── IDS CSV Export{date}.csv
│   └── Overflow History/
│       └── IDS CSV Export - Overflow{date}.csv    # Overflow History, get auto-saved in app
├── Tools/
│   ├── MasterEffeciencyFile/
│   │   └── SinglePalletPythonScript/
│   │       └── SinglePallet.csv                   # CSV saved from SinglePallet script
│   └── WrongOverflowFinder/
│       └── WrongZoneFinderPythonScript.csv        # CSV saved from WrongZone script
└── Food Data Exports/
    ├── ExpirationData.xlsx                        # xlsx of expiration data for food
    └── ItemNotesList.xlsx                         # xlsx of item notes for food
```