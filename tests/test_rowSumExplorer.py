import unittest
import pandas as pd
import numpy as np
import tempfile
import os
from itertools import combinations
from rowSumExplorer.rowSumExplorer import SetExcelTableColumn


class TestSetExcelTableColumn(unittest.TestCase):
    """Test suite for SetExcelTableColumn class"""

    def setUp(self):
        """Create temporary Excel files for testing"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a simple test Excel file
        self.test_file = os.path.join(self.temp_dir, 'test.xlsx')
        self.create_test_excel()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def create_test_excel(self):
        """Helper method to create a test Excel file"""
        data = {
            'ID': ['1', '2', '3', '4', '5'],
            'Value': [10, 20, 30, 40, 50],
            'Category': ['A', 'B', 'A', 'B', 'A']
        }
        df = pd.DataFrame(data)
        df.to_excel(self.test_file, sheet_name='Sheet1', index=False)

    def test_initialization(self):
        """Test class initialization"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=10,
            max_combinations=5,
            first_result=False
        )
        
        self.assertEqual(instance.excel_path, self.test_file)
        self.assertEqual(instance.sheet_name, 'Sheet1')
        self.assertEqual(instance.target_sum, 60)
        self.assertEqual(instance.n, 2)
        self.assertEqual(instance.column_name, 'Value')
        self.assertEqual(instance.time_limit, 10)
        self.assertEqual(instance.max_combinations, 5)
        self.assertEqual(instance.first_result, False)
        self.assertEqual(instance.bypass_time_limit, False)

    def test_initialization_with_first_result_true(self):
        """Test that bypass_time_limit is set when first_result is True"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=10,
            max_combinations=5,
            first_result=True
        )
        
        self.assertEqual(instance.bypass_time_limit, True)

    def test_find_table(self):
        """Test find_table method"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        
        # Check DataFrame properties
        self.assertEqual(len(df), 5)
        self.assertListEqual(list(df.columns), ['ID', 'Value', 'Category'])
        self.assertIn('Value', df.columns)

    def test_find_table_with_invalid_range(self):
        """Test find_table with invalid cell range"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:Z:100',  # Out of bounds
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        # Should still work but may have fewer rows
        self.assertGreater(len(df), 0)

    def test_get_combinations_basic(self):
        """Test get_combinations with valid data"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        # Should find at least one combination (10+50 or 20+40)
        self.assertIsNotNone(result_dfs)
        self.assertGreater(len(result_dfs), 0)
        
        # Each result should have n+1 rows (n data rows + 1 total row)
        for result_df in result_dfs:
            self.assertEqual(len(result_df), instance.n + 1)

    def test_get_combinations_impossible_sum(self):
        """Test get_combinations with impossible target sum"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=999,  # Impossible to reach
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        self.assertIsNone(result_dfs)

    def test_get_combinations_sum_too_small(self):
        """Test get_combinations when target sum is less than minimum possible"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=5,  # Less than 10 + 20
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        self.assertIsNone(result_dfs)

    def test_get_combinations_with_max_combinations_limit(self):
        """Test get_combinations respects max_combinations limit"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=1,  # Limit to 1 result
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=1)
        
        self.assertIsNotNone(result_dfs)
        self.assertLessEqual(len(result_dfs), 1)

    def test_get_combinations_with_first_result_true(self):
        """Test get_combinations with first_result=True"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=True
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        self.assertIsNotNone(result_dfs)
        # Should return only first result
        self.assertEqual(len(result_dfs), 1)

    def test_total_row_creation(self):
        """Test that TOTAL row is correctly created"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        if result_dfs:
            for result_df in result_dfs:
                last_row = result_df.iloc[-1]
                # Check TOTAL label exists
                self.assertEqual(last_row['ID'], 'TOTAL')
                # Check sum value
                self.assertEqual(last_row['Value'], instance.target_sum)

    def test_result_dataframe_structure(self):
        """Test that result dataframes have proper structure"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        if result_dfs:
            for result_df in result_dfs:
                # Should have same columns as original
                self.assertEqual(list(result_df.columns), list(df.columns))
                # Should have n+1 rows
                self.assertEqual(len(result_df), instance.n + 1)

    def test_run_with_valid_combinations(self):
        """Test run method with valid combinations"""
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=60,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        instance.run(output_file)
        
        # Check output file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Check content
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn('DataFrame', content)

    def test_run_with_impossible_sum(self):
        """Test run method with impossible target sum"""
        output_file = os.path.join(self.temp_dir, 'output_impossible.txt')
        
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=999,
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        instance.run(output_file)
        
        # Check output file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Check message about impossible sum
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("can't be reached", content)

    def test_combination_sum_correctness(self):
        """Test that found combinations actually sum to target"""
        instance = SetExcelTableColumn(
            excel_path=self.test_file,
            sheet_name='Sheet1',
            cell_range='A:1:C:6',
            target_sum=70,  # 20 + 50
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        if result_dfs:
            for result_df in result_dfs:
                # Exclude TOTAL row and sum the values
                data_rows = result_df[:-1]  # All rows except last (TOTAL)
                actual_sum = data_rows[instance.column_name].sum()
                self.assertEqual(actual_sum, instance.target_sum)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and potential bugs"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_duplicate_values_in_column(self):
        """Test handling of duplicate values in column"""
        test_file = os.path.join(self.temp_dir, 'duplicates.xlsx')
        data = {
            'ID': ['1', '2', '3', '4'],
            'Value': [20, 20, 30, 30],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:5',
            target_sum=40,  # 20 + 20
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        # BUG: The code doesn't handle duplicate values correctly
        # It uses the same index multiple times
        # This might return results that look wrong
        self.assertIsNotNone(result_dfs)

    def test_single_row_table(self):
        """Test with single row data"""
        test_file = os.path.join(self.temp_dir, 'single_row.xlsx')
        data = {
            'ID': ['1'],
            'Value': [100],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:2',
            target_sum=100,
            n=1,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        self.assertIsNotNone(result_dfs)
        self.assertEqual(len(result_dfs), 1)

    def test_n_larger_than_available_rows(self):
        """Test when n is larger than number of available rows"""
        test_file = os.path.join(self.temp_dir, 'few_rows.xlsx')
        data = {
            'ID': ['1', '2'],
            'Value': [10, 20],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:3',
            target_sum=30,
            n=5,  # Larger than available rows
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        # Should return None since n > available rows
        self.assertIsNone(result_dfs)

    def test_zero_and_negative_values(self):
        """Test handling of zero and negative values"""
        test_file = os.path.join(self.temp_dir, 'zero_neg.xlsx')
        data = {
            'ID': ['1', '2', '3', '4'],
            'Value': [-10, 0, 20, 30],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:5',
            target_sum=50,  # -10 + 0 + 20 + 30 would be 40, but 20 + 30 = 50
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        self.assertIsNotNone(result_dfs)
        self.assertGreater(len(result_dfs), 0)


class TestBugReport(unittest.TestCase):
    """Tests highlighting specific bugs"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_bug_duplicate_indices_with_repeated_values(self):
        """
        BUG: When column has duplicate values, the code:
            indices = [i for i, val in enumerate(column_values) if val in combination][:self.n]
        
        Returns wrong indices because 'val in combination' matches based on VALUE not position.
        If we have [20, 20, 30] and look for combination (20, 20), 
        it will return [0, 0] instead of [0, 1].
        """
        test_file = os.path.join(self.temp_dir, 'bug_duplicates.xlsx')
        data = {
            'ID': ['A', 'B', 'C'],
            'Value': [20, 20, 30],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:4',
            target_sum=40,  # 20 + 20
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        # BUG: This might return wrong IDs or duplicate rows
        if result_dfs:
            for result_df in result_dfs:
                ids = result_df['ID'].tolist()[:-1]  # Exclude TOTAL
                # Should be ['A', 'B'] but might be ['A', 'A']
                print(f"Bug Test - IDs returned: {ids} (should be ['A', 'B'])")
                self.assertNotEqual(ids, ['A', 'A'])  # This test WILL fail, exposing the bug

    def test_bug_index_mismatch_with_combinations(self):
        """
        BUG: The code generates combinations from column_values (which is a list),
        but then tries to match indices back to the original dataframe.
        The issue is that combinations() uses values from column_values, 
        but indices are based on enumerate of column_values in the same iteration.
        
        When there are duplicate values, the line:
            indices = [i for i, val in enumerate(column_values) if val in combination][:self.n]
        
        Will return WRONG indices. For example:
        column_values = [10, 20, 30, 10, 50]
        Looking for combination (10, 20):
        - indices would return [0, 1] correctly if 10 appears first
        - But if we're looking for the second 10, it still returns 0
        """
        test_file = os.path.join(self.temp_dir, 'bug_index.xlsx')
        data = {
            'ID': ['1', '2', '3', '4', '5'],
            'Value': [10, 20, 30, 10, 50],
        }
        df = pd.DataFrame(data)
        df.to_excel(test_file, sheet_name='Sheet1', index=False)
        
        instance = SetExcelTableColumn(
            excel_path=test_file,
            sheet_name='Sheet1',
            cell_range='A:1:B:6',
            target_sum=60,  # 10 + 50
            n=2,
            column_name='Value',
            time_limit=None,
            max_combinations=None,
            first_result=False
        )
        
        df = instance.find_table()
        result_dfs = instance.get_combinations(df, time_limit=None, max_combinations=None)
        
        if result_dfs:
            # Count unique IDs in results - should not have duplicates
            for result_df in result_dfs:
                ids = result_df['ID'].tolist()[:-1]  # Exclude TOTAL
                unique_ids = len(set(ids))
                same_ids = len(ids)
                if unique_ids != same_ids:
                    print(f"Bug detected: Got {ids}, which has duplicate IDs")


if __name__ == '__main__':
    unittest.main()
