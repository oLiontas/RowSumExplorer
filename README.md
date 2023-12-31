# GENERAL

Many times we want an excel table that will result from combinations of additions in a column of our choice. With this package, by selecting the initial excel table, the column and the target number, we will get a dataframe in txt format, which we can then import into an excel table from the external data import option. Of course, the time the results will take depends on the time complexity, i.e. the number of combinations that the program must execute. For this reason there are parameters that you will be able to set and choose if you want it to return the first single result it finds, to return the number of combinations you want, to stop the execution in a time that you have determine.


## Instructions
- Create an instance of the SetExcelColumn class by providing the required parameters:


<code>

    ec = rowSumExplorer.SetExcelColumn(excel_path='path/to/excel_file.xlsx',
                                sheet_name='Sheet1',
                                cell_range='A:1:D:10',
                                target_sum=100,
                                n=3,
                                column_name='Column1',
                                time_limit=10,
                                max_combinations=5,
                                first_result=True)
    

- Replace the following parameters based on your needs:

1. **excel_path**: Path to the Excel file that contains the table you want to process.

2. **sheet_name**: Name of the sheet within the Excel file that contains the table.

3. **cell_range:** Range of cells in the format "start_cell:end_cell" that define the table's location.

4. **target_sum**: The desired sum you want to achieve by combining rows.

5. **n**: Number of rows to combine in each combination.

6. **column_name**: The name of the column from which rows will be selected.

7. **time_limit**: Maximum time limit (in seconds) for finding combinations. Set to None if there is no time limit.

8. **max_combinations**: Maximum number of combinations to find. Set to None if there is no limit.

9. **first_result**: Set to True if you want to stop searching after finding the first combination that meets the target sum.

Run the code and specify the output file:



    ec.run(output_file='output.txt')

Replace 'output.txt' with the desired file name where the results will be saved.

When you execute the code, it performs the following steps:

Loads the specified Excel file and extracts the table from the given cell range.
Finds combinations of rows from the specified column where the sum of values in each combination matches the target sum.
Writes the resulting combinations to the output file.
If the target sum cannot be reached due to minimum limits, it writes an appropriate message to the output file.
Make sure to replace 'path/to/excel_file.xlsx' with the actual path to your Excel file and adjust the other parameters according to your requirements.

#**Note**

The output file is in a .txt format so you can insert this to an excel sheet via data import

