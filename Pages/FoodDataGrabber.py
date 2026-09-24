import pandas as pd
import os
import BinDataGrabber as bsg
import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils.dataframe import dataframe_to_rows
from pathlib import Path
from openpyxl.formatting.rule import DataBarRule, FormulaRule
from openpyxl.worksheet.page import PageMargins

i_list = ["104WHEAT", "104NFL4550","dfsdfsd"]
base_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(base_dir,"..", "OutputFiles", "ShelfLifeGrabber.xlsx")
cell_border = Border(
    top = Side(border_style= "thin", color= "000000"),
    bottom = Side(border_style= "thin", color= "000000"),
    left = Side(border_style= "thin", color= "000000"),
    right = Side(border_style= "thin", color= "000000")
)
center_align = Alignment(horizontal= "center", vertical= "center")

def GetShelfLifeAndNotes(items:list[str]) -> pd.DataFrame:
    df_sl = bsg.GetExpirationData()
    df_notes = bsg.GetItemNotes()
    item_df = pd.DataFrame({"Items":items})
    item_df["Items"] = item_df["Items"].astype(str).str.upper()
    item_df = item_df.merge(df_notes[["Item Number","Note"]],how= "left",left_on="Items", right_on="Item Number")
    item_df = item_df.merge(df_sl[["ItemNumber","Expiration Days"]],how= "left",left_on="Items", right_on="ItemNumber")
    item_df["Expiration Days"] = ((item_df["Expiration Days"] / 30).floordiv(1).fillna(0).astype(int).astype(str) + " Months")
    item_df["Expiration Days"] = item_df["Expiration Days"].replace("0 Months", "Not Found")
    item_df = item_df[["Items","Note","Expiration Days"]]
    item_df = item_df.rename(columns={"Expiration Days":"Shelf Life"})
    item_df = item_df.fillna("Not Found")
    return item_df

def GenerateExcelReport(df:pd.DataFrame):
    """This function takes a list of items and compares them to a dataframe to pull shelf lifes for food items."""
    wb = Workbook()
    ws = wb.active
    for x,row in enumerate(dataframe_to_rows(df,index= False, header=True),start=1):
        for y,value in enumerate(row,start=1):
            cell = ws.cell(x,y)
            cell.value = value
            cell.border = cell_border
            ws.row_dimensions[x].height = 35.25
            cell.alignment = center_align
            cell.font = Font(size=10)
    ws.column_dimensions["A"].width = 23
    ws.column_dimensions["B"].width = 103
    ws.column_dimensions["C"].width = 23
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = False
    ws.page_margins = PageMargins(left=0.7,right=0.7,top=0.75,bottom=0.75,header=0.3,footer=0.3)
    for cell in ws["B"]:
        cell.alignment = Alignment(horizontal="center",vertical="center",wrap_text=True)
    wb.save(output_path)
    os.startfile(output_path)
    return None

st.title("Shelf Life Grabber")
col1, col2 = st.columns([1,3])
with col1:
    ui = st.text_area("Enter a list of item numbers here",width= 600).upper().split()

with col2:
    with st.container(horizontal_alignment="center"):
        if st.button("Press For Excel Report"):
            GenerateExcelReport(GetShelfLifeAndNotes(ui))
    st.dataframe(GetShelfLifeAndNotes(ui), hide_index= True)
