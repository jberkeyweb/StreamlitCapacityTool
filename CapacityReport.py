import BinDataGrabber as bsg
from Data import Data
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils.dataframe import dataframe_to_rows
from pathlib import Path
from openpyxl.formatting.rule import DataBarRule, FormulaRule
import os
import pandas as pd

def RunReport():
        

    main_df = Data(bsg.get_bin_data())
    # output_path = directory / "CapacityReport1.xlsx"
    # output_path = "OutputFiles/CapacityReport.xlsx"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "OutputFiles", "CapacityReport.xlsx")

    total_alts_df = main_df.df[main_df.df["Bin Type"].str.contains("ALTERNATE")]

    total_bins = main_df.get_total_num_bins
    total_alts = main_df.get_total_num_alternates
    total_prims = main_df.get_total_num_primaries
    total_avail_bins = main_df.get_total_num_available_bins
    total_avail_prims = main_df.get_total_num_available_primaries
    total_avail_alts = main_df.get_total_num_available_alts


    total_total_dec = (total_bins - total_avail_bins) / total_bins
    total_prim_dec = (total_prims - total_avail_prims) / total_prims
    total_alt_dec = (total_alts - total_avail_alts) / total_alts
    total_total_percent = f"{(total_bins - total_avail_bins) / total_bins:.2%}"
    total_prim_percent = f"{(total_prims - total_avail_prims) / total_prims:.2%}"
    total_alt_percent = f"{(total_alts - total_avail_alts) / total_alts:.2%}"

    aisle_avail_alts = main_df.SummarizeAvailableAlternate().rename(columns={"Bins":"Available_Alts"})
    aisle_taken_alts = main_df.SummarizeTakenAlternates().rename(columns={"Bins":"Taken_Alts"})
    aisle_all_alts = main_df.SummarizeAllAlternateBins().rename(columns={"Bins":"All_Alts"})

    aisle_avail_prims = main_df.SummarizeAvailablePrimaries().rename(columns={"Bins":"Available_Prims"})
    aisle_taken_prims = main_df.SummarizeTakenPrimaries().rename(columns={"Bins":"Taken_Prims"})
    aisle_all_prims = main_df.SummarizeAllPrimaryBins().rename(columns={"Bins":"All_Prims"})

    df_list = [
        aisle_avail_alts,
        aisle_taken_alts,
        aisle_all_alts,
        aisle_avail_prims,
        aisle_taken_prims,
        aisle_all_prims
    ]

    merge_df = df_list[0]

    for df in df_list[1:]:
        merge_df = merge_df.merge(df, how= "outer", on= "Zone")


    merge_df["Available_Alts"] = merge_df["Available_Alts"].fillna(0)
    merge_df["Taken_Alts"] = merge_df["Taken_Alts"].fillna(0)
    merge_df["All_Alts"] = merge_df["All_Alts"].fillna(0)
    merge_df["Available_Prims"] = merge_df["Available_Prims"].fillna(0)
    merge_df["Taken_Prims"] = merge_df["Taken_Prims"].fillna(0)
    merge_df["All_Prims"] = merge_df["All_Prims"].fillna(0)
    merge_df["P_%"] = ((merge_df["All_Prims"].astype(int) - merge_df["Available_Prims"].astype(int)) / merge_df["All_Prims"].astype(int)).fillna("NO PRIMARIES")
    merge_df["A_%"] = ((merge_df["All_Alts"].astype(int) - merge_df["Available_Alts"].astype(int)) / merge_df["All_Alts"].astype(int)).fillna("NO ALTERNATES")
    merge_df["P_Label"] = merge_df["Taken_Prims"].astype(int).astype(str) + "/" + merge_df["All_Prims"].astype(int).astype(str)
    merge_df["A_Label"] = merge_df["Taken_Alts"].astype(int).astype(str) + "/" + merge_df["All_Alts"].astype(int).astype(str)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" DEAD STOCK","",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" CHEMICAL"," C",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" GAYLORD"," GL",regex= False)
    # merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" FOOD","",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" FULL BAY","",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" - BULK","",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" BULK","",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace(" FOOD"," F",regex= False)
    merge_df["Zone"] = merge_df["Zone"].astype(str).str.replace("C PRO","CPRO",regex= False)

    df_dict = {}
    for x in range(1,10):
        df_label = f"zone_{x}_df"
        df_dict[df_label] = merge_df[merge_df["Zone"].str.startswith(str(x))]

    df_dict["zone_ds_df"] = df_dict["zone_3_df"][(df_dict["zone_3_df"]["Zone"].str.contains("2'")) | 
                                                (df_dict["zone_3_df"]["Zone"].str.contains("BB")) | 
                                                (df_dict["zone_3_df"]["Zone"].str.contains("GL"))]
    df_dict["zone_3_df"] = df_dict["zone_3_df"][~(df_dict["zone_3_df"]["Zone"].str.contains("2'")) &
                                                ~(df_dict["zone_3_df"]["Zone"].str.contains("BB")) &
                                                ~(df_dict["zone_3_df"]["Zone"].str.contains("GL"))]
    len(df_dict)






    # border class object to set cell borders
    cell_border = Border(
        top = Side(border_style= "thin", color= "000000"),
        bottom = Side(border_style= "thin", color= "000000"),
        left = Side(border_style= "thin", color= "000000"),
        right = Side(border_style= "thin", color= "000000")
    )

    # data bar rules from DataBarRule
    purple_bar = DataBarRule(
        start_type="num",
        start_value=0,
        end_type="num",
        end_value=1,
        color="8626B3",
        showValue=True
    )

    blue_bar = DataBarRule(
        start_type="num",
        start_value=0,
        end_type="num",
        end_value=1,
        color="638EC6",
        showValue=True    
    )

    orange_bar = DataBarRule(
        start_type="num",
        start_value=0,
        end_type="num",
        end_value=1,
        color="FF8C00",
        showValue=True      
    )

    center_align = Alignment(horizontal= "center", vertical= "center")
    left_align = Alignment(horizontal= "left", vertical= "center")
    right_align = Alignment(horizontal= "right", vertical= "bottom")

    green_fill = PatternFill(
        start_color="90EE90",
        end_color="90EE90",
        fill_type="solid"
    )

    red_fill = PatternFill(
        start_color="FF9999",
        end_color="FF9999",
        fill_type="solid"
    )

    yellow_fill = PatternFill(
        start_color="FFFF99",
        end_color="FFFF99",
        fill_type="solid"
    )


    wb = Workbook()

    ws1 = wb.active


    # making title
    ws1.merge_cells("J1:T3")
    ws1["J1"] = "876 Capacity Report"
    ws1["J1"].alignment = Alignment(horizontal= "center", vertical= "center")
    ws1["J1"].font = Font(size= 40,bold= "bold")

    # making total data bar and numbersa
    ws1.merge_cells("D4:Z6")
    ws1["D4"] = total_total_dec
    ws1.conditional_formatting.add("D4", purple_bar)
    ws1["D4"].font = Font(size=48, bold="bold")
    ws1["D4"].number_format = '0.00%'
    ws1["D4"].alignment = right_align
    for row in ws1["D4:Z6"]:
        for cell in row:
            cell.border = cell_border

    # setting left total DC bar labels
    ws1["C5"] = "TOTAL"
    ws1["C5"].font = Font(size= 26, bold= "bold", color="8626B3")
    ws1["C5"].alignment = center_align

    ws1["C9"] = "PRIMARY"
    ws1["C9"].font = Font(size= 26, bold= "bold", color="638EC6")
    ws1["C9"].alignment = center_align

    ws1["C13"] = "OVERFLOW"
    ws1["C13"].font = Font(size= 26, bold= "bold", color="FF8C00")
    ws1["C13"].alignment = center_align

    ws1.column_dimensions["C"].width = 15



    # setting right total DC labels
    ws1.merge_cells("AA4:AD6")
    ws1["AA4"] = f"{(total_bins - total_avail_bins)}/{total_bins}"
    ws1["AA4"].font = Font(size= 48, bold= "bold")
    ws1["AA4"].alignment = center_align

    ws1.merge_cells("AA8:AD10")
    ws1["AA8"] = f"{(total_prims - total_avail_prims)}/{total_prims}"
    ws1["AA8"].font = Font(size= 48, bold= "bold")
    ws1["AA8"].alignment = center_align

    ws1.merge_cells("AA12:AD14")
    ws1["AA12"] = f"{(total_alts - total_avail_alts)}/{total_alts}"
    ws1["AA12"].font = Font(size= 48, bold= "bold")
    ws1["AA12"].alignment = center_align


    # making primary data bar and numbers
    ws1.merge_cells("D8:Z10")
    ws1["D8"] = total_prim_dec
    ws1.conditional_formatting.add("D8", blue_bar)
    ws1["D8"].font = Font(size=48, bold= "bold")
    ws1["D8"].number_format = "0.00%"
    ws1["D8"].alignment = right_align
    for row in ws1["D8:Z10"]:
        for cell in row:
            cell.border = cell_border

    ws1.merge_cells("D12:Z14")
    ws1["D12"] = total_alt_dec
    ws1.conditional_formatting.add("D12", orange_bar)
    ws1["D12"].font = Font(size= 48, bold= "bold")
    ws1["D12"].number_format = "0.00%"
    ws1["D12"].alignment = right_align
    for row in ws1["D12:Z14"]:
        for cell in row:
            cell.border = cell_border


    # making Primary, Overflow, and Zone 1 labels
    ws1.merge_cells("G17:I17")
    ws1["G17"] = "PRIMARY"
    ws1["G17"].font = Font(size= 26, bold= "bold", color= "638EC6")
    ws1["G17"].alignment = center_align

    ws1.merge_cells("G21:I21")
    ws1["G21"] = "Zone 1"
    ws1["G21"].font = Font(size= 22, bold= "bold")
    ws1["G21"].alignment = center_align

    ws1.merge_cells("V17:W17")
    ws1["V17"] = "OVERFLOW"
    ws1["V17"].font = Font(size= 26, bold= "bold", color= "FF8C00")
    ws1["V17"].alignment = center_align

    ws1.merge_cells("V21:W21")
    ws1["V21"] = "Zone 1"
    ws1["V21"].font = Font(size= 22, bold= "bold")
    ws1["V21"].alignment = center_align

    ws1.sheet_view.showGridLines = False

    def MakePrimZone(series_p_per: pd.Series,series_zone:pd.Series,series_p_label:pd.Series, start_row:int):
        # printing the percent values and merging the same cells
        for x, y in enumerate(series_p_per,start= start_row):
            ws1.cell(row=x,column=3, value= y)
            current_range = f"C{x}:M{x}"
            current_cell = f"C{x}"
            cell_border_fill = f"C{x}:M{x}"
            ws1.merge_cells(current_range)
            ws1.conditional_formatting.add(current_cell, blue_bar)
            ws1[current_cell].font = Font(size=24, bold= "bold")
            ws1[current_cell].number_format = "0.00%"
            ws1[current_cell].alignment = center_align
            for row in ws1[cell_border_fill]:
                for cell in row:
                    cell.border = cell_border

    # zone labels for zone 1
        for x, y in enumerate(series_zone,start= start_row):
            ws1.cell(row=x,column=2, value= y)
            current_cell = f"B{x}"
            green_rule = FormulaRule(formula=[f"$C{x}<=0.85"],fill= green_fill)
            red_rule = FormulaRule(formula= [f"$C{x}>0.9"], fill= red_fill)
            yellow_rule = FormulaRule(formula= [f"AND($C{x}>0.85,$C{x}<=0.9)"], fill= yellow_fill)
            ws1.merge_cells(current_range)
            ws1[current_cell].font = Font(size=21, bold= "bold")
            ws1[current_cell].alignment = center_align
            ws1[current_cell].border = cell_border
            ws1.conditional_formatting.add(current_cell, green_rule)
            ws1.conditional_formatting.add(current_cell, red_rule)
            ws1.conditional_formatting.add(current_cell, yellow_rule)

        # number labels for zone 1
        for x, y in enumerate(series_p_label,start= start_row):
            ws1.cell(row=x,column=14, value= y)
            current_cell = f"N{x}"
            ws1.merge_cells(current_range)
            ws1[current_cell].font = Font(size=24, bold= "bold")
            ws1[current_cell].alignment = left_align

    def ZoneLabelPrimary(start_cell:int,zone:str):
        label_cell_1 = f"G{start_cell}"
        merge_end_1 = f"I{start_cell}"
        merge_range_1 = f"{label_cell_1}:{merge_end_1}"
        label_cell_2 = f"V{start_cell}"
        merge_end_2 = f"W{start_cell}"
        merge_range_2 = f"{label_cell_2}:{merge_end_2}"
        ws1[label_cell_1] = zone
        ws1.merge_cells(merge_range_1)
        ws1.merge_cells(merge_range_2)
        ws1[label_cell_2] = zone
        ws1[label_cell_1].font = Font(size= 22, bold= "bold")
        ws1[label_cell_1].alignment = center_align
        ws1[label_cell_2].font = Font(size= 22, bold= "bold")
        ws1[label_cell_2].alignment = center_align

    MakePrimZone(df_dict["zone_1_df"]["P_%"],df_dict["zone_1_df"]["Zone"],df_dict["zone_1_df"]["P_Label"],24)
    zone_2_start = len(df_dict["zone_1_df"]["P_%"]) + 24 + 5
    zone_2_label_start = len(df_dict["zone_1_df"]) + 24 + 2
    ZoneLabelPrimary(zone_2_label_start,"Zone 2")
    MakePrimZone(df_dict["zone_2_df"]["P_%"],df_dict["zone_2_df"]["Zone"],df_dict["zone_2_df"]["P_Label"],zone_2_start)
    zone_3_label_start = zone_2_start + len(df_dict["zone_2_df"]["P_%"]) + 2
    zone_3_start = zone_3_label_start + 3
    ZoneLabelPrimary(zone_3_label_start, "Zone 3 4'")
    MakePrimZone(df_dict["zone_3_df"]["P_%"],df_dict["zone_3_df"]["Zone"],df_dict["zone_3_df"]["P_Label"],zone_3_start)
    zone_3_ds_label_start = zone_3_start + len(df_dict["zone_3_df"]["P_%"]) + 2
    zone_3_ds_start = zone_3_ds_label_start + 3
    ZoneLabelPrimary(zone_3_ds_label_start,"Zone 3 2'")
    MakePrimZone(df_dict["zone_ds_df"]["P_%"],df_dict["zone_ds_df"]["Zone"],df_dict["zone_ds_df"]["P_Label"],zone_3_ds_start)
    zone_4_label_start = zone_3_ds_start + len(df_dict["zone_ds_df"]["P_%"]) + 2
    zone_4_start = zone_4_label_start + 3
    ZoneLabelPrimary(zone_4_label_start,"Zone 4")
    MakePrimZone(df_dict["zone_4_df"]["P_%"],df_dict["zone_4_df"]["Zone"],df_dict["zone_4_df"]["P_Label"],zone_4_start)
    zone_5_label_start = zone_4_start + len(df_dict["zone_4_df"]["P_%"]) + 2
    zone_5_start = zone_5_label_start + 3
    ZoneLabelPrimary(zone_5_label_start, "Zone 5")
    MakePrimZone(df_dict["zone_5_df"]["P_%"],df_dict["zone_5_df"]["Zone"],df_dict["zone_5_df"]["P_Label"],zone_5_start)
    zone_6_label_start = zone_5_start + len(df_dict["zone_5_df"]["P_%"]) + 2
    zone_6_start = zone_6_label_start + 3
    ZoneLabelPrimary(zone_6_label_start, "Zone 6")
    MakePrimZone(df_dict["zone_6_df"]["P_%"],df_dict["zone_6_df"]["Zone"],df_dict["zone_6_df"]["P_Label"],zone_6_start)
    zone_7_label_start = zone_6_start + len(df_dict["zone_6_df"]["P_%"]) + 2
    zone_7_start = zone_7_label_start + 3
    ZoneLabelPrimary(zone_7_label_start, "Zone 7")
    MakePrimZone(df_dict["zone_7_df"]["P_%"],df_dict["zone_7_df"]["Zone"],df_dict["zone_7_df"]["P_Label"],zone_7_start)
    zone_8_label_start = zone_7_start + len(df_dict["zone_7_df"]["P_%"]) + 2
    zone_8_start = zone_8_label_start + 3
    ZoneLabelPrimary(zone_8_label_start,"Zone 8")
    MakePrimZone(df_dict["zone_8_df"]["P_%"],df_dict["zone_8_df"]["Zone"],df_dict["zone_8_df"]["P_Label"],zone_8_start)

    def MakeAltZone(series_a_per: pd.Series,series_zone:pd.Series,series_a_label:pd.Series, start_row:int):
        # printing the percent values and merging the same cells
        for x, y in enumerate(series_a_per,start= start_row):
            ws1.cell(row=x,column=17, value= y)
            current_range = f"Q{x}:AB{x}"
            current_cell = f"Q{x}"
            cell_border_fill = f"Q{x}:AB{x}"
            ws1.merge_cells(current_range)
            ws1.conditional_formatting.add(current_cell, orange_bar)
            ws1[current_cell].font = Font(size=24, bold= "bold")
            ws1[current_cell].number_format = "0.00%"
            ws1[current_cell].alignment = center_align
            for row in ws1[cell_border_fill]:
                for cell in row:
                    cell.border = cell_border

    # zone labels for zone 1
        for x, y in enumerate(series_zone,start= start_row):
            ws1.cell(row=x,column=16, value= y)
            current_cell = f"P{x}"
            green_rule = FormulaRule(formula=[f"$Q{x}<=0.85"],fill= green_fill)
            red_rule = FormulaRule(formula= [f"$Q{x}>0.9"], fill= red_fill)
            yellow_rule = FormulaRule(formula= [f"AND($Q{x}>0.85,$Q{x}<=0.9)"], fill= yellow_fill)
            ws1.merge_cells(current_range)
            ws1[current_cell].font = Font(size=21, bold= "bold")
            ws1[current_cell].alignment = center_align
            ws1[current_cell].border = cell_border
            ws1.conditional_formatting.add(current_cell, green_rule)
            ws1.conditional_formatting.add(current_cell, red_rule)
            ws1.conditional_formatting.add(current_cell, yellow_rule)

        # number labels for zone 1
        for x, y in enumerate(series_a_label,start= start_row):
            ws1.cell(row=x,column=29, value= y)
            current_cell = f"AC{x}"
            ws1.merge_cells(current_range)
            ws1[current_cell].font = Font(size=24, bold= "bold")
            ws1[current_cell].alignment = left_align

    MakeAltZone(df_dict["zone_1_df"]["A_%"],df_dict["zone_1_df"]["Zone"],df_dict["zone_1_df"]["A_Label"],24)
    MakeAltZone(df_dict["zone_2_df"]["A_%"],df_dict["zone_2_df"]["Zone"],df_dict["zone_2_df"]["A_Label"],zone_2_start)
    MakeAltZone(df_dict["zone_3_df"]["A_%"],df_dict["zone_3_df"]["Zone"],df_dict["zone_3_df"]["A_Label"],zone_3_start)
    MakeAltZone(df_dict["zone_ds_df"]["A_%"],df_dict["zone_ds_df"]["Zone"],df_dict["zone_ds_df"]["A_Label"],zone_3_ds_start)
    MakeAltZone(df_dict["zone_4_df"]["A_%"],df_dict["zone_4_df"]["Zone"],df_dict["zone_4_df"]["A_Label"],zone_4_start)
    MakeAltZone(df_dict["zone_5_df"]["A_%"],df_dict["zone_5_df"]["Zone"],df_dict["zone_5_df"]["A_Label"],zone_5_start)
    MakeAltZone(df_dict["zone_6_df"]["A_%"],df_dict["zone_6_df"]["Zone"],df_dict["zone_6_df"]["A_Label"],zone_6_start)
    MakeAltZone(df_dict["zone_7_df"]["A_%"],df_dict["zone_7_df"]["Zone"],df_dict["zone_7_df"]["A_Label"],zone_7_start)
    MakeAltZone(df_dict["zone_8_df"]["A_%"],df_dict["zone_8_df"]["Zone"],df_dict["zone_8_df"]["A_Label"],zone_8_start)












    # changing col dims of page
    ws1.column_dimensions["A"].width = 8.43
    ws1.column_dimensions["B"].width = 17.43
    ws1.column_dimensions["C"].width = 34.71
    ws1.column_dimensions["D"].width = 13.43
    ws1.column_dimensions["E"].width = 8.43
    ws1.column_dimensions["F"].width = 9.14
    ws1.column_dimensions["G"].width = 32
    ws1.column_dimensions["H"].width = 13.43
    ws1.column_dimensions["I"].width = 11.86
    ws1.column_dimensions["J"].width = 11.86
    ws1.column_dimensions["K"].width = 35
    ws1.column_dimensions["L"].width = 13.43
    ws1.column_dimensions["M"].width = 8.43
    ws1.column_dimensions["N"].width = 9.14
    ws1.column_dimensions["O"].width = 35
    ws1.column_dimensions["P"].width = 17.43
    ws1.column_dimensions["Q"].width = 11.86
    ws1.column_dimensions["R"].width = 11.86
    ws1.column_dimensions["S"].width = 32
    ws1.column_dimensions["T"].width = 13.43
    ws1.column_dimensions["U"].width = 8.43
    ws1.column_dimensions["V"].width = 9.14
    ws1.column_dimensions["W"].width = 35
    ws1.column_dimensions["X"].width = 13.43
    ws1.column_dimensions["Y"].width = 11.86
    ws1.column_dimensions["Z"].width = 11.86
    ws1.column_dimensions["AA"].width = 35
    ws1.column_dimensions["AB"].width = 5.43
    ws1.column_dimensions["AC"].width = 8.43
    ws1.column_dimensions["AD"].width = 8.43
    ws1.column_dimensions["AE"].width = 8.43

    ws1.sheet_view.zoomScale = 53
    # merge_df.to_excel(output_path)
    wb.save(output_path)

    os.startfile(output_path)


    # rule = FormulaRule(
    #     formula=['$B2="YES"'],
    #     fill=green_fill
    # )

    # ws.conditional_formatting.add("A2", rule)