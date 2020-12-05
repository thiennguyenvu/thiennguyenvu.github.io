import pandas


class ProcessFile():
    def ExceltoJSON():
        excel_data_df = pandas.read_excel(
            'excel/test_excel.xlsx', sheet_name='Sheet')
        json_str = excel_data_df.to_json()
        print(json_str)
        pass
