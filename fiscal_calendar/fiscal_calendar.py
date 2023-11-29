# -*- coding: utf-8 -*-
# standard libraries
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import calendar
from tabulate import tabulate

# packages related to pdf reporting
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


class FiscalCalendarGenerator:
    """
    FiscalCalendarGenerator is a class for generating and managing fiscal calendar information.

    Attributes:
        - start_date (str): The start date of the fiscal calendar in the format 'yyyy-mm-dd'.
        - end_date (str): The end date of the fiscal calendar in the format 'yyyy-mm-dd'.

    Methods:
        - create_dataframe(): Generates the fiscal calendar and returns it as a DataFrame.
        - print_fiscal_calendar(df_fiscal_calendar, columns=3, week_number=False, year=None): Prints a fiscal calendar based on the provided DataFrame.
        - save_fiscal_calendar_to_pdf(df_fiscal_calendar, columns=3, week_number=False, year=None, filename="fiscal_calendar.pdf"): Saves a fiscal calendar to a PDF file based on the provided DataFrame.
        - pretty_print_year(df_date, year): Pretty prints the fiscal calendar for a specific year.

    Usage:
        from fiscal_calendar import FiscalCalendarGenerator

        # Instantiate the FiscalCalendarGenerator class
        fc = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2031-01-04')

        # Generate the fiscal calendar
        df_fiscal_calendar = fc.create_dataframe()

        # Print the fiscal calendar
        fc.print_fiscal_calendar(df_fiscal_calendar, columns=3, week_number=False, year=2022)

        # Save the fiscal calendar to a PDF file
        fc.save_fiscal_calendar_to_pdf(df_fiscal_calendar, columns=3, week_number=False, year=2022, filename="fcal.pdf")

        # Pretty print the fiscal calendar for the year 2022
        fc.pretty_print_year(df_fiscal_calendar, year=2022)
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.date_format = "%Y-%m-%d"
        self.month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                           10: 'Oct', 11: 'Nov', 12: 'Dec'}
        self.month_name_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                                7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
                                12: 'December'}
        self.quarter_dict = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        self.num_days = 7
        self.num_weeks = 4
        self.lst_array = []
        self.lst_fiscal_weeks = []
        self.weeknumber_lst = []
        self.lst_months = []
        self.lst_fiscalqtrs = []
        self.lst_years = []
        self.lst_week_months = []
        self.fiscal_start_date = None

    def print_fiscal_calendar(self, df_fiscal_calendar: pd.DataFrame, columns: int = 3, week_number: bool = False,
                              year: int = None):
        """
        Prints a fiscal calendar based on the provided DataFrame.

        Parameters:
            - df_fiscal_calendar (pd.DataFrame): DataFrame containing fiscal calendar data.
            - columns (int): Number of columns in the grid layout for printed calendars (default is 3).
            - week_number (bool): If True, includes week numbers in the printed calendar (default is False).
            - year (int): The specific fiscal year to print (default is None, which prints all available years).

        Prints a grid of fiscal calendars, arranged in rows and columns. Each calendar includes the month name,
        fiscal year, and a calendar grid with days of the week. If week_number is True, each day in the calendar
        includes its corresponding fiscal week number.

        Note: The function assumes that the DataFrame (df_fiscal_calendar) contains the following columns:
        'fiscal_year', 'fiscal_month_of_year', 'fiscal_month_name', 'day_date', 'day_of_week_short_name',
        'fiscal_day_of_week', and 'fiscal_week_of_year'.

        Args:
            df_fiscal_calendar (pd.DataFrame): DataFrame containing fiscal calendar data.
            columns (int, optional): Number of columns in the grid layout for printed calendars (default is 3).
            week_number (bool, optional): If True, includes week numbers in the printed calendar (default is False).
            year (int, optional): The specific fiscal year to print (default is None, which prints all available years).

        Returns:
            None

        Example:
        ```python
        from fiscal_calendar import FiscalCalendarGenerator

        fiscal_calendar_generator = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

        # Generate the fiscal calendar
        df_fiscal_calendar = fiscal_calendar_generator.create_dataframe()

        # Print the fiscal calendar for the year 2022 without week numbers in a 6-column layout
        fiscal_calendar_generator.print_fiscal_calendar(df_fiscal_calendar, columns=6, week_number=False, year=2022)
        ```
        """
        # Check if the fiscal year input is provided by user
        if year is not None:
            # Convert the year to a string
            fiscal_years = [str(year)]
        else:
            # Get the unique fiscal years from the DataFrame
            fiscal_years = df_fiscal_calendar['fiscal_year'].unique()

        # Create a mapping dictionary
        day_of_week_mapping = {'SUN': 'Su', 'MON': 'Mo', 'TUE': 'Tu', 'WED': 'We', 'THU': 'Th', 'FRI': 'Fr',
                               'SAT': 'Sa'}

        # Loop through each fiscal year
        for fiscal_year in fiscal_years:
            # Get the fiscal year data from the DataFrame
            fiscal_year_data = df_fiscal_calendar[df_fiscal_calendar['fiscal_year'] == fiscal_year]

            # Create a list to store the formatted months
            formatted_months = []
            # Loop through each fiscal month
            for fiscal_month in range(1, 13):
                # Get the fiscal month data from the DataFrame
                fiscal_month_data = fiscal_year_data[fiscal_year_data['fiscal_month_of_year'] == fiscal_month]

                # Check if the fiscal month data is empty
                if not fiscal_month_data.empty:
                    # Get the fiscal month name from the first row
                    fiscal_month_name = fiscal_month_data['fiscal_month_name'].iloc[0]
                    # Create a string to represent the month
                    month_str = f"{fiscal_month_name} FY{fiscal_year}\n"

                    # if user wants to see fiscal week number and if week number is 2 digits -> add +1 space
                    if week_number and any(fiscal_month_data['fiscal_week_of_year'] > 9):
                        month_str += "W  | Su Mo Tu We Th Fr Sa\n"
                    # if user wants to see fiscal week number and if week number is 1 digit -> remove -1 space
                    elif week_number and any(fiscal_month_data['fiscal_week_of_year'] <= 9):
                        month_str += "W | Su Mo Tu We Th Fr Sa\n"
                    # else user does not want to see fiscal week number in calendar
                    else:
                        month_str += "Su Mo Tu We Th Fr Sa\n"

                    # Create a list to represent the calendar
                    calendar = [['  '] * 7 for _ in range(6)]  # Add an extra column for the week number if needed

                    # Create a list to store the week numbers
                    week_numbers = ['  '] * 6

                    # Sort fiscal_month_data based on day_date
                    fiscal_month_data = fiscal_month_data.sort_values('day_date')

                    # Get the minimum fiscal_week_of_year for the current month
                    min_week_of_year = fiscal_month_data['fiscal_week_of_year'].min()

                    for _, day_data in fiscal_month_data.iterrows():
                        day_date = datetime.strptime(day_data['day_date'], '%m/%d/%Y')
                        day_str = f"{day_date.day:2d}"
                        day_of_week = day_data['day_of_week_short_name'].upper()  # Convert to uppercase

                        # Map the day of the week to the desired format
                        day_of_week = day_of_week_mapping.get(day_of_week, '  ')  # Use '  ' if not found in the mapping

                        # Use the day index from the dataframe, subtract 1 because Python uses 0-based indexing
                        day_index = day_data['fiscal_day_of_week'] - 1

                        # Use the fiscal_week_of_year of dataframe, adjust it to fit within the range of calendar lst
                        week_num = day_data['fiscal_week_of_year'] - min_week_of_year

                        # Fill the calendar array
                        calendar[week_num][day_index] = day_str

                        # Store the week number for each day
                        if week_number:
                            week_numbers[week_num] = str(day_data['fiscal_week_of_year'])

                    # Add the calendar to the month string
                    for week_num, week in enumerate(calendar):
                        week_line = " ".join(day_str if day_str != '  ' else "    " for day_str in week)
                        if week_line.strip():  # Only add the line if it's not empty
                            if week_number:
                                month_str += f"{week_numbers[week_num]} | " + week_line + "\n"
                            else:
                                month_str += week_line + "\n"

                    # Add the month string to the list of formatted months
                    formatted_months.append(month_str)

            # Instead of printing, append the output to a list of strings
            output = []
            # Loop through the formatted months, stepping by the number of columns
            for i in range(0, len(formatted_months), columns):
                # Split each month into lines and store them in a list
                split_months = [month.split("\n") for month in formatted_months[i:i + columns]]
                # Get the maximum number of lines in a month
                max_lines = max(len(split_month) for split_month in split_months)
                # Loop through each line
                for j in range(max_lines):
                    # Initialize a list to store the lines for each month
                    line = []
                    # Loop through each split month
                    for split_month in split_months:
                        # Append the line from the split month to the line list, or append an empty string if the
                        # line doesn't exist
                        line.append(split_month[j].ljust(28) if j < len(split_month) else "".ljust(28))
                    # Join the lines into a single string and append it to the output list
                    output.append("   ".join(line))
                    # Append a newline to the output list
                    output.append("\n")
                # Append an additional newline to the output list to separate the rows of months
                output.append("\n")

            # Join the list of strings into a single string and return it
            return "".join(output)

    def save_fiscal_calendar_to_pdf(self, df_fiscal_calendar: pd.DataFrame, columns: int = 3,
                                    week_number: bool = False,
                                    year: int = None, filename: str = "fiscal_calendar.pdf"):
        """
        Saves a fiscal calendar to a PDF file based on the provided DataFrame.
        [...]
        """
        # Generate the fiscal calendar as a string
        fiscal_calendar_str = self.print_fiscal_calendar(df_fiscal_calendar, columns, week_number, year)

        # Replace spaces with non-breaking spaces
        fiscal_calendar_str = fiscal_calendar_str.replace(" ", "\u00A0")

        try:
            # Create a PDF canvas
            c = canvas.Canvas(filename, pagesize=letter)

            # Set the font and size to courier
            font = "Courier"
            size = 10
            c.setFont(font, size)

            # Get the width and height of the page
            page_width, page_height = letter

            # Increase the top margin by changing the y-coordinate for drawing the title
            top_margin = 700  # Adjust this value as needed
            title = f'Fiscal Calendar {year}'
            c.setFont(font, size + 10)  # Increase the font size for the title
            c.drawCentredString(page_width / 2.0, top_margin, title)
            c.setFont(font, size)  # Reset the font size

            # Get the fiscal year data from the DataFrame
            fiscal_year_data = df_fiscal_calendar[df_fiscal_calendar['fiscal_year'] == str(year)]
            my_start_date = fiscal_year_data['day_date'].iloc[0]
            my_end_date = fiscal_year_data['day_date'].iloc[-1]

            # Draw the date range below the title
            date_range = f"{my_start_date} - {my_end_date}"
            c.setFont(font, size + 2)  # Increase the font size for the title
            c.drawCentredString(page_width / 2.0, top_margin - 20, date_range)
            c.setFont(font, size)  # Reset the font size

            # Add the fiscal calendar string to the PDF
            for i, line in enumerate(fiscal_calendar_str.split("\n")):
                # Calculate the width of the text
                text_width = stringWidth(line, font, size)

                # Calculate the x-coordinate for the text to be centered
                x = (page_width - text_width) / 2

                # Increase the top margin for drawing the fiscal calendar
                fiscal_calendar_y = top_margin - 72 - i * 12  # Subtract an additional 24 to create more space
                c.drawString(x, fiscal_calendar_y, line)

            # Save the PDF
            c.save()
        except PermissionError as e:
            raise PermissionError(f"Failed to save PDF: Permission denied for '{filename}'. "
                                  f"Ensure the file is not open and try again.") from e

    def pretty_print_year(self, df_date, year):
        """
        Pretty print the fiscal calendar for a specific year.

        Parameters:
        - df_date (pd.DataFrame): The DataFrame containing the fiscal calendar.
        - year (int): The fiscal year to pretty print.

        Usage:
            fiscal_calendar_generator.pretty_print_year(2022, df_fiscal_calendar)
        """
        fiscal_year_data = df_date[df_date['fiscal_year'] == str(year)]  # Assuming 'fiscal_year' is a string
        formatted_data = fiscal_year_data[[
            'time_day_id_pk', 'day_date', 'day_of_week_short_name', 'day_of_week_name', 'day_of_week_letter',
            'fiscal_day_of_week', 'fiscal_week_of_year', 'fiscal_week_of_season', 'fiscal_week_of_quarter',
            'fiscal_week_of_month', 'fiscal_week_start_date', 'fiscal_week_end_date', 'fiscal_week_iso_code',
            'fiscal_month_of_year', 'fiscal_month_of_season', 'fiscal_month_of_quarter', 'fiscal_month_name',
            'fiscal_month_short_name', 'fiscal_month_start_date', 'fiscal_month_end_date',
            'fiscal_month_number_of_weeks',
            'fiscal_month_number_of_days', 'fiscal_quarter_of_year', 'fiscal_quarter_of_year_str',
            'fiscal_quarter_of_season',
            'fiscal_season_of_year', 'fiscal_season_name', 'fiscal_year', 'fiscal_year_2_digit',
            'fiscal_year_start_date',
            'fiscal_year_end_date', 'fiscal_year_number_of_weeks', 'fiscal_year_number_of_days',
            'last_year_equiv_day_fk',
            'last_year_equiv_week_fk', 'last_year_equiv_day_date', 'last_year_fiscal_year',
            'last_year_fiscal_month_of_year',
            'prior_year_from_last_year_equiv_day_fk', 'prior_year_from_last_year_equiv_day_date',
            'time_fiscal_week_id_fk',
            'first_fiscal_week_of_fiscal_month_ind', 'last_fiscal_week_of_fiscal_month_ind', 'time_day_id_pk_int'
        ]]

        # Convert the DataFrame to a tabular format for pretty printing
        print(tabulate(formatted_data, headers='keys', tablefmt='pretty'))

    def check_and_shift_start_date(self):
        """
        Checks if the start date is within the last 5 days of the month.
        If it is, shifts the month_name_dict by one.
        """
        start_date = pd.to_datetime(self.start_date)
        if start_date.day > calendar.monthrange(start_date.year, start_date.month)[1] - 5:
            # Shift the month_name_dict by one
            self.month_name_dict = {k - 1 if k != 1 else 12: v for k, v in self.month_name_dict.items()}

    def delta_days(self, mydate):
        """
        Calculate the number of days between the provided date and the end of the fiscal year.

        Parameters:
            - mydate (str): A string representing the date in the format specified by the 'date_format' attribute.

        Returns:
            int: The number of days between the provided date and the end of the fiscal year.

        This method calculates the difference in days between the provided date and the last day
        (January 31st) of the fiscal year in which the provided date falls.

        Args:
            mydate (str): A string representing the date in the format specified by the 'date_format' attribute.

        Returns:
            int: The number of days between the provided date and the end of the fiscal year.

        Example:
        ```python
        from fiscal_calendar import FiscalCalendarGenerator

        fiscal_calendar_generator = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

        # Calculate the delta days for a specific date
        days_difference = fiscal_calendar_generator.delta_days('2023-05-15')
        print(f"Delta days: {days_difference}")
        ```
        """
        fiscal_start_date_dt = datetime.strptime(mydate, self.date_format)
        fsd_year = fiscal_start_date_dt.year
        jan_end_date = datetime(fsd_year + 1, 1, 31)
        y = fiscal_start_date_dt + timedelta(days=364 - 1)
        delta = abs(y - jan_end_date)
        return delta.days

    def generate_fiscal_calendar(self):
        """
        Generates a fiscal calendar DataFrame based on the configured start and end dates.

        Returns:
            pd.DataFrame: DataFrame containing fiscal calendar information, including columns for 'Date', 'Fiscal Wk',
                          'Weekday', 'Day', 'Fiscal Month', 'Fiscal Qtr', and 'Fiscal Year'.

        This method generates a fiscal calendar DataFrame starting from the configured start date (inclusive)
        to the end date (inclusive). The generated DataFrame includes columns for the date, fiscal week,
        weekday, day of the week, fiscal month, fiscal quarter, and fiscal year.

        The fiscal calendar is calculated based on the provided start and end dates and the configured fiscal
        year details such as the number of days in a week, the number of days in a month, and the fiscal month
        dictionary.

        Returns:
            pd.DataFrame: DataFrame containing the fiscal calendar information.

        Example:
        ```python
        from fiscal_calendar import FiscalCalendarGenerator

        fiscal_calendar_generator = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

        # Generate the fiscal calendar DataFrame
        df_fiscal_calendar = fiscal_calendar_generator.generate_fiscal_calendar()

        # Print the first few rows of the fiscal calendar DataFrame
        print(df_fiscal_calendar.head())
        ```
        """
        # Check if the start date is within the last 5 days of the month
        self.check_and_shift_start_date()

        # Get the fiscal start date
        fiscal_start_date = self.start_date
        # Convert the fiscal start date to a datetime object
        fiscal_start_date_dt = datetime.strptime(fiscal_start_date, self.date_format)
        # Get the fiscal month
        fiscal_month = fiscal_start_date_dt.month
        # Get the fiscal year
        fiscal_year = fiscal_start_date_dt.year

        # Initialize lists to hold the fiscal weeks, months, quarters, and years
        self.lst_months = []
        lst_array = []
        lst_fiscal_weeks = []
        lst_fiscalqtrs = []
        lst_years = []

        # Initiate the 53rd week and set it equal to 0 days
        fifthy_third_week = 0

        # Create a DataFrame with a date range based on the start and end dates
        df_date = pd.DataFrame(pd.date_range(start=self.start_date, end=self.end_date), columns=['Date'])

        # Calculate the number of years between the start and end dates
        years_count = (df_date['Date'].max().year - df_date['Date'].min().year) + 1

        # Loop through each year
        for year in range(1, years_count + 1):
            # Increment the fiscal year
            fiscal_year += 1

            # If it's not the first year, set the month to 1, otherwise use the fiscal month
            month = 1 if year != 1 else fiscal_month

            # Loop through each month
            for i in range(month, 12 + 1):
                # Determine the number of weeks in the month
                if (self.delta_days(fiscal_start_date) >= 4) and (self.month_dict.get(i) == 'Dec'):
                    # if the delta days is greater than or equal to 4 and the month is December, add 5th week
                    num_weeks = 5
                    # set 5th week to 7 days
                    fifthy_third_week = 7
                elif (i - 2) % 3 == 0:
                    num_weeks = 5
                else:
                    num_weeks = 4

                # Create an array of the month and append it to the list of months
                my_array = np.repeat(self.month_dict.get(i), (num_weeks * self.num_days))
                # Append the array to the list of months
                lst_array.append(len(my_array))

                # If we've processed 12 months, calculate the fiscal quarters and weeks
                if len(lst_array) == 12:
                    # Create an array of quarter numbers (1 to 4)
                    y = np.array(list(np.arange(0, 4) + 1))
                    # Convert the quarter numbers to strings
                    y = np.char.mod('%d', y)
                    # Add a 'Q' prefix to the quarter numbers
                    y = np.char.add('Q', y)
                    # Repeat each quarter number 91 times (to represent the days in a quarter)
                    # and append it to the list of fiscal quarters
                    lst_fiscalqtr = np.repeat(y, 91)

                    # Count the number of days in the array equals 364 then 52 weeks in the fiscal year
                    if sum(lst_array) == 364:
                        x = np.array(list(np.arange(0, 52) + 1))
                    # Count the number of days in the array equals 371 then 53 weeks in the fiscal year
                    elif sum(lst_array) == 371:
                        # create array with 53 weeks
                        x = np.array(list(np.arange(0, 53) + 1))
                        lst_fiscalqtr = np.append(lst_fiscalqtr, ['Q4'] * 7)
                    else:
                        continue

                    weeknumber_lst = np.repeat(x, self.num_days)
                    lst_fiscal_weeks.append(weeknumber_lst)
                    lst_array = []
                    lst_fiscalqtrs.append(lst_fiscalqtr)

                # Append the array to the list of fiscal weeks
                self.lst_months.append(my_array)

            # Update the fiscal start date for the next year
            fiscal_start_date_dt = datetime.strptime(fiscal_start_date, self.date_format)
            lst_year = np.repeat((fiscal_year - 1), (364 + fifthy_third_week))
            lst_years.append(lst_year)

            # Update the fiscal start date for the next year
            fiscal_start_date = (fiscal_start_date_dt + timedelta(days=364 + fifthy_third_week)).strftime(
                self.date_format)

            # Reset the fifthy_third_week to 0
            fifthy_third_week = 0

        ################################################################################
        # Create the fiscal week, month, quarter, and year columns in the DataFrame
        ################################################################################
        # Concatenate the list of fiscal weeks into a single array
        output_wks = np.hstack(lst_fiscal_weeks)

        # Add the fiscal week numbers to the DataFrame
        df_date['Fiscal Wk'] = pd.Series(list(output_wks))

        # Add the weekday names to the DataFrame
        df_date['Weekday'] = df_date['Date'].dt.day_name()

        # Map the weekday names to their corresponding numbers and add them to the DataFrame
        df_date['Day'] = df_date['Weekday'].map(
            {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7})

        # Concatenate the list of fiscal months into a single array
        output_months = np.hstack(self.lst_months)

        # Add the fiscal month numbers to the DataFrame
        df_date['Fiscal Month'] = pd.Series(list(output_months))

        # Concatenate the list of fiscal quarters into a single array
        output_qtrs = np.hstack(lst_fiscalqtrs)

        # Add the fiscal quarter numbers to the DataFrame
        df_date['Fiscal Qtr'] = pd.Series(list(output_qtrs))

        # Concatenate the list of fiscal years into a single array
        output_years = np.hstack(lst_years)

        # Add the fiscal year numbers to the DataFrame and convert them to strings
        df_date['Fiscal Year'] = pd.Series(list(output_years)).astype('str')

        # Return the DataFrame with the added fiscal calendar information
        return df_date

    def create_dataframe(self):
        """
        Generate and preprocess a fiscal calendar DataFrame.

        Returns:
            pd.DataFrame: Processed DataFrame containing fiscal calendar information.

        This method generates a fiscal calendar DataFrame, adds various columns representing different aspects of the
        fiscal calendar, and returns the processed DataFrame. The added columns include information about time, day, week,
        month, quarter, season, and year components of the fiscal calendar.

        Note: The method relies on a series of helper methods within the class to calculate and add specific columns.

        Returns:
            pd.DataFrame: Processed DataFrame containing fiscal calendar information.
        """
        df_date_copy = self.generate_fiscal_calendar()
        df_date_copy.to_csv('fiscal_calendar.csv', index=False)

        # removed changing 'Date' to 'time_day_id_pk'
        df_fiscal_calendar = self.add_time_day_id_pk(df_date_copy)  # Column 1: time_day_id_pk
        df_fiscal_calendar = self.add_day_date(df_fiscal_calendar)  # Column 2: day_date
        df_fiscal_calendar = self.add_day_of_week_short_name(df_fiscal_calendar)  # Column 3: day_of_week_short_name
        df_fiscal_calendar = self.add_day_of_week_name(df_fiscal_calendar)  # Column 4: day_of_week_name
        df_fiscal_calendar = self.add_day_of_week_letter(df_fiscal_calendar)  # Column 5: day_of_week_letter
        df_fiscal_calendar = self.add_fiscal_day_of_week(df_fiscal_calendar)  # Column 6: fiscal_day_of_week
        df_fiscal_calendar = self.add_fiscal_week_of_year(df_fiscal_calendar)  # Column 7: fiscal_week_of_year
        df_fiscal_calendar = self.add_fiscal_week_of_season(df_fiscal_calendar)  # Column 8: fiscal_week_of_season
        df_fiscal_calendar = self.add_fiscal_week_of_quarter(df_fiscal_calendar)  # Column 9: fiscal_week_of_quarter
        df_fiscal_calendar = self.add_fiscal_week_of_month(df_fiscal_calendar)  # Column 10: fiscal_week_of_month
        df_fiscal_calendar = self.add_fiscal_week_start_date(df_fiscal_calendar)  # Column 11: fiscal_week_start_date
        df_fiscal_calendar = self.add_fiscal_week_end_date(df_fiscal_calendar)  # Column 12: fiscal_week_end_date
        df_fiscal_calendar = self.add_fiscal_week_iso_code(df_fiscal_calendar)  # Column 13: fiscal_week_iso_code
        df_fiscal_calendar = self.add_fiscal_month_of_year(df_fiscal_calendar)  # Column 14: fiscal_month_of_year
        df_fiscal_calendar = self.add_fiscal_month_of_season(df_fiscal_calendar)  # Column 15: fiscal_month_of_season
        df_fiscal_calendar = self.add_fiscal_month_of_quarter(df_fiscal_calendar)  # Column 16: fiscal_month_of_quarter
        df_fiscal_calendar = self.add_fiscal_month_name(df_fiscal_calendar)  # Column 17: fiscal_month_name
        df_fiscal_calendar = self.add_fiscal_month_short_name(df_fiscal_calendar)  # Column 18: fiscal_month_short_name
        df_fiscal_calendar = self.add_fiscal_month_start_date(df_fiscal_calendar)  # Column 19: fiscal_month_start_date
        df_fiscal_calendar = self.add_fiscal_month_end_date(df_fiscal_calendar)  # Column 20: fiscal_month_end_date
        df_fiscal_calendar = self.add_fiscal_month_number_of_weeks(
            df_fiscal_calendar)  # Column 21: fiscal_month_number_of_weeks
        df_fiscal_calendar = self.add_fiscal_month_number_of_days(
            df_fiscal_calendar)  # Column 22: fiscal_month_number_of_days
        df_fiscal_calendar = self.add_fiscal_quarter_of_year(df_fiscal_calendar)  # Column 23: fiscal_quarter_of_year
        df_fiscal_calendar = self.add_fiscal_quarter_of_year_str(
            df_fiscal_calendar)  # Column 24: fiscal_quarter_of_year_str
        df_fiscal_calendar = self.add_fiscal_quarter_of_season(
            df_fiscal_calendar)  # Column 25: fiscal_quarter_of_season
        df_fiscal_calendar = self.add_fiscal_season_of_year(df_fiscal_calendar)  # Column 26: fiscal_season_of_year
        df_fiscal_calendar = self.add_fiscal_season_name(df_fiscal_calendar)  # Column 27: fiscal_season_name
        df_fiscal_calendar = self.add_fiscal_year(df_fiscal_calendar)  # Column 28: fiscal_year
        df_fiscal_calendar = self.add_fiscal_year_2_digit(df_fiscal_calendar)  # Column 29: fiscal_year_2_digit
        df_fiscal_calendar = self.add_fiscal_year_start_date(df_fiscal_calendar)  # Column 30: fiscal_year_start_date
        df_fiscal_calendar = self.add_fiscal_year_end_date(df_fiscal_calendar)  # Column 31: fiscal_year_end_date
        df_fiscal_calendar = self.add_fiscal_year_number_of_weeks(
            df_fiscal_calendar)  # Column 32: fiscal_year_number_of_weeks
        df_fiscal_calendar = self.add_fiscal_year_number_of_days(
            df_fiscal_calendar)  # Column 33: fiscal_year_number_of_days
        df_fiscal_calendar = self.add_last_year_equiv_day_fk(df_fiscal_calendar)  # Column 34: last_year_equiv_day_fk
        df_fiscal_calendar = self.calculate_last_year_equiv_week_fk(
            df_fiscal_calendar)  # Column 35: last_year_equiv_week_fk
        df_fiscal_calendar = self.add_last_year_equiv_day_date(
            df_fiscal_calendar)  # Column 36: last_year_equiv_day_date
        df_fiscal_calendar = self.add_last_year_fiscal_year(df_fiscal_calendar)  # Column 37: last_year_fiscal_year
        df_fiscal_calendar = self.add_last_year_fiscal_month_of_year(
            df_fiscal_calendar)  # Column 38: last_year_fiscal_month_of_year
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_day_fk(
            df_fiscal_calendar)  # Column 39: prior_year_from_last_year_equiv_day_fk
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_week_fk(
            df_fiscal_calendar)  # Column 40: prior_year_from_last_year_equiv_week_fk
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_day_date(
            df_fiscal_calendar)  # Column 41: prior_year_from_last_year_equiv_day_date
        df_fiscal_calendar = self.add_time_fiscal_week_id_fk(df_fiscal_calendar)  # Column 42: time_fiscal_week_id_fk
        df_fiscal_calendar = self.add_first_fiscal_week_of_fiscal_month_ind(
            df_fiscal_calendar)  # Column 43: first_fiscal_week_of_fiscal_month_ind
        df_fiscal_calendar = self.add_last_fiscal_week_of_fiscal_month_ind(
            df_fiscal_calendar)  # Column 44: last_fiscal_week_of_fiscal_month_ind
        df_fiscal_calendar = self.add_time_day_id_pk_int(df_fiscal_calendar)  # Column 44: time_day_id_pk_int

        # drop temporary columns that were needed to calculate above columns
        df_fiscal_calendar = df_fiscal_calendar.drop(
            columns=['Date', 'Fiscal Wk', 'Weekday', 'Day', 'Fiscal Month', 'Fiscal Qtr', 'Fiscal Year'])

        return df_fiscal_calendar

    def add_time_day_id_pk(self, df_date):
        """
        Adds a new column 'time_day_id_pk' and formats the dates in 'Date' to 'yyyymmdd'.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'Date' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'time_day_id_pk' column.
        """
        df_date['time_day_id_pk'] = df_date['Date'].apply(lambda x: x.strftime('%Y%m%d'))
        return df_date

    def add_day_date(self, df_date):
        """
        Adds a new column 'day_date' to the DataFrame and formats the dates in 'Date' column to 'mm/dd/yyyy'.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'Date' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'day_date' column.
        """
        df_date['day_date'] = df_date['Date'].copy()
        df_date['day_date'] = df_date['day_date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_day_of_week_short_name(self, df_date):
        """
        Adds a new column 'day_of_week_short_name' to the DataFrame and maps the day names to their short forms.
        For example: 'Sunday' -> 'SUN', 'Monday' -> 'MON', etc.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'Date' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'day_of_week_short_name' column.
        """
        df_date['day_of_week_short_name'] = df_date['Date'].dt.day_name()
        df_date['day_of_week_short_name'] = df_date['day_of_week_short_name'].map(
            {'Sunday': 'SUN', 'Monday': 'MON', 'Tuesday': 'TUE', 'Wednesday': 'WED', 'Thursday': 'THU',
             'Friday': 'FRI', 'Saturday': 'SAT'})
        return df_date

    def add_fiscal_day_of_week(self, df_date):
        df_date['fiscal_day_of_week'] = df_date['Weekday'].map(
            {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7})
        return df_date

    def add_fiscal_week_start_date(self, df_date):
        df_date['fiscal_week_start_date'] = df_date['Date'].dt.to_period('W-SAT').apply(
            lambda r: r.start_time).dt.date.apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_fiscal_week_iso_code(self, df_date):
        df_date['fiscal_week_iso_code'] = df_date['Fiscal Wk'].astype(str).replace('\.\d+', '', regex=True)
        df_date['fiscal_week_iso_code'] = df_date['fiscal_week_iso_code'].str.zfill(2)
        df_date['fiscal_week_iso_code'] = df_date['Fiscal Year'] + 'W' + df_date['fiscal_week_iso_code']
        return df_date

    def add_day_of_week_name(self, df_date):
        df_date['day_of_week_name'] = df_date['Weekday'].map(
            {'Sunday': 'SUNDAY', 'Monday': 'MONDAY', 'Tuesday': 'TUESDAY', 'Wednesday': 'WEDNESDAY',
             'Thursday': 'THURSDAY', 'Friday': 'FRIDAY', 'Saturday': 'SATURDAY'})
        return df_date

    def add_fiscal_week_end_date(self, df_date):
        df_date['fiscal_week_end_date'] = df_date['Date'].dt.to_period('W-SAT').apply(
            lambda r: r.end_time).dt.date.apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_day_of_week_letter(self, df_date):
        df_date['day_of_week_letter'] = df_date['day_of_week_short_name'].map(
            {'SUN': 'U', 'MON': 'M', 'TUE': 'T', 'WED': 'W', 'THU': 'H', 'FRI': 'F', 'SAT': 'S'})
        return df_date

    def add_fiscal_week_of_year(self, df_date):
        df_date['fiscal_week_of_year'] = df_date['Fiscal Wk']
        return df_date

    def add_fiscal_week_of_season(self, df_date):
        df_date['fiscal_week_of_season'] = df_date['fiscal_week_of_year'].apply(
            lambda x: np.where(x <= 26, x, x - 26))
        return df_date

    def add_fiscal_week_of_quarter(self, df_date):
        df_date['fiscal_week_of_quarter'] = df_date['fiscal_week_of_year'].apply(
            lambda x: np.where(x <= 13, x, np.where(x <= 26, x - 13, np.where(x <= 39, x - 26, x - 39))))
        return df_date

    def add_fiscal_week_of_month(self, df_date):
        lst_week_months = []

        fiscal_year_counts = df_date['Fiscal Year'].value_counts().sort_index()

        for daysyear in range(0, len(fiscal_year_counts)):
            four_week_array = np.repeat(np.array(list(np.arange(0, 4) + 1)), 7)
            five_week_array = np.repeat(np.array(list(np.arange(0, 5) + 1)), 7)
            lst_week_month = np.hstack((four_week_array, five_week_array, four_week_array) * 4)

            if fiscal_year_counts.iloc[daysyear] == 364:
                lst_week_month = lst_week_month
            #elif fiscal_year_counts.iloc[daysyear] == 366:
            elif fiscal_year_counts.iloc[daysyear] == 371:
                lst_week_month = np.append(lst_week_month, (list(np.arange(4, 5) + 1) * 7))
            else:
                pass

            lst_week_months.append(lst_week_month)

        my_output = np.concatenate(lst_week_months).ravel().tolist()
        df_date['fiscal_week_of_month'] = pd.Series(my_output)
        return df_date

    def add_fiscal_month_of_year(self, df_date):
        df_date['fiscal_month_of_year'] = df_date['Fiscal Month'].map(
            {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
             'Nov': 11, 'Dec': 12})
        return df_date

    def add_fiscal_month_of_season(self, df_date):
        df_date['fiscal_month_of_season'] = df_date['fiscal_month_of_year'].apply(
            lambda x: x if x <= 6 else x - 6)
        return df_date

    def add_fiscal_month_of_quarter(self, df_date):
        df_date['fiscal_month_of_quarter'] = df_date['fiscal_month_of_year'].apply(
            lambda x: x % 3 if (x % 3 != 0) else 3)
        return df_date

    def add_fiscal_month_name(self, df_date):
        """
        Adds a 'fiscal_month_name' column to the DataFrame.

        Args:
            df_date (DataFrame): The input DataFrame containing a 'fiscal_month_of_year' column.

        Returns:
            DataFrame: The input DataFrame with an additional 'fiscal_month_name' column,
            where month names are represented with the full month name, with the first letter capitalized
            (e.g., January, February, March, April, May, June, July, August, September, October, November, December).
        """
        df_date['fiscal_month_name'] = df_date['fiscal_month_of_year'].map(self.month_name_dict)
        return df_date

    def add_fiscal_month_short_name(self, df_date):
        df_date['fiscal_month_short_name'] = df_date['fiscal_month_name'].str[0:3]
        return df_date

    def add_fiscal_quarter_of_year(self, df_date):
        df_date['fiscal_quarter_of_year'] = df_date['Fiscal Qtr'].map(self.quarter_dict)
        return df_date

    def add_fiscal_quarter_of_year_str(self, df_date):
        df_date['fiscal_quarter_of_year_str'] = df_date['Fiscal Qtr']
        return df_date

    def add_fiscal_quarter_of_season(self, df_date):
        df_date['fiscal_quarter_of_season'] = df_date['fiscal_quarter_of_year'].apply(
            lambda x: x if x <= 2 else x - 2)
        return df_date

    def add_fiscal_season_of_year(self, df_date):
        df_date['fiscal_season_of_year'] = df_date['fiscal_quarter_of_year'].apply(
            lambda x: 1 if x <= 2 else 2)
        return df_date

    def add_fiscal_season_name(self, df_date):
        df_date['fiscal_season_name'] = df_date['fiscal_season_of_year'].map(
            {1: 'SPRING', 2: 'FALL'})
        return df_date

    def add_fiscal_year(self, df_date):
        df_date['fiscal_year'] = df_date['Fiscal Year']
        return df_date

    def add_fiscal_year_2_digit(self, df_date):
        df_date['fiscal_year_2_digit'] = df_date['fiscal_year'].str[-2:]
        return df_date

    def add_last_year_equiv_day_fk(self, df_date):
        df_date['last_year_equiv_day_fk'] = (df_date['Date'].dt.date - timedelta(days=364)).apply(
            lambda x: x.strftime('%Y%m%d'))
        return df_date

    def calculate_last_year_equiv_week_fk(self, df_date):
        # Shift original dataframe by +364 rows to match last year week
        df_date['last_year_equiv_week_fk'] = df_date['fiscal_week_iso_code'].shift(364)

        # Iterate over all rows of the dataframe
        for i in range(len(df_date)):
            # Start from 0, iterate 364 times
            if i <= 363:
                # Get the first 4 characters of the fiscal_week_iso_code
                year_str = df_date['fiscal_week_iso_code'].iloc[i][0:4]

                # Convert the string year to an integer and get the last year (year - 1)
                left = str(int(year_str) - 1)

                # Get the right part of the string (the week)
                right = df_date['fiscal_week_iso_code'].iloc[i][4:]

                # Combine strings to get last year + 'W' + the same week for the first year (364 rows)
                df_date.at[i, 'last_year_equiv_week_fk'] = left + right
            else:
                # Do nothing for rows after the first 364
                pass

        return df_date

    def add_time_fiscal_week_id_fk(self, df_date):
        """
        This method adds the 'time_fiscal_week_id_fk' column to the DataFrame.
        The values in this column are the same as those in the 'fiscal_week_iso_code' column.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'fiscal_week_iso_code' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'time_fiscal_week_id_fk' column.
        """
        df_date['time_fiscal_week_id_fk'] = df_date['fiscal_week_iso_code']
        return df_date

    def add_prior_year_from_last_year_equiv_day_fk(self, df_date):
        """
        This method adds the 'prior_year_from_last_year_equiv_day_fk' column to the DataFrame.
        The values in this column are calculated by subtracting 2 years (364*2 days) from the 'Date' column.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'Date' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'prior_year_from_last_year_equiv_day_fk' column.
        """
        df_date['prior_year_from_last_year_equiv_day_fk'] = (
                df_date['Date'].dt.date - timedelta(days=364 * 2)).apply(lambda x: x.strftime('%Y%m%d'))
        return df_date

    def add_prior_year_from_last_year_equiv_week_fk(self, df_date):
        """
        Add a column 'last_year_equiv_week_fk' to the DataFrame representing the equivalent fiscal week in the prior year.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'fiscal_week_iso_code' column.

        This method adds a new column 'last_year_equiv_week_fk' to the DataFrame. The values in this column represent
        the equivalent fiscal week in the prior year, derived from the 'fiscal_week_iso_code' column. The calculation
        considers a shift of 364 rows for the initial set of rows, and then iterates over each row to determine the
        equivalent week in the prior year.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'last_year_equiv_week_fk' calculated based on the
                          'fiscal_week_iso_code' column.
        """
        df_date['last_year_equiv_week_fk'] = df_date['fiscal_week_iso_code'].shift(364)

        # iterate over all rows of the dataframe
        for i in range(len(df_date)):
            # e.g. start from 0, so it will be for 364 days iterate 364 times
            if i <= 363:
                # get first for 4 characters e.g. year <yyyy> left part convert from string to integer and get last year e.g. (year - 1)
                left = str(int(df_date['fiscal_week_iso_code'].iloc[i][0:4]) - 1)
                # define right-part e.g. rest of string after year has been removed e.g. (yyyyW01) -> W01
                right = df_date['fiscal_week_iso_code'].iloc[i][4:]
                # combine string to get last year + 'W' + same week for first year e.g. 364 rows
                df_date.at[i, 'last_year_equiv_week_fk'] = left + right
            else:
                # do nothing
                pass
        return df_date

    def add_last_year_equiv_day_date(self, df_date):
        df_date['last_year_equiv_day_date'] = (df_date['Date'] - pd.DateOffset(days=364)).dt.strftime('%m/%d/%Y')
        return df_date

    def add_prior_year_from_last_year_equiv_day_date(self, df_date):
        df_date['prior_year_from_last_year_equiv_day_date'] = (
                df_date['Date'] - pd.DateOffset(days=364 * 2)).dt.strftime('%m/%d/%Y')
        return df_date

    def add_first_fiscal_week_of_fiscal_month_ind(self, df_date):
        df_date['first_fiscal_week_of_fiscal_month_ind'] = df_date['fiscal_week_of_month'].apply(
            lambda x: 1 if x == 1 else 0)
        return df_date

    def add_last_fiscal_week_of_fiscal_month_ind(self, df_date):
        lst_last_weeks_ind = []
        years_count = (pd.to_datetime(self.end_date).year - pd.to_datetime(self.start_date).year) + 1
        for year in range(1, years_count + 1):
            for i in self.lst_months:
                if len(i) == 28:
                    lst_last_week_ind = np.repeat([0, 1], [21, 7])
                elif len(i) == 35:
                    lst_last_week_ind = np.repeat([0, 1], [28, 7])
                lst_last_weeks_ind.append(lst_last_week_ind)

        output_lst_weeks_ind = np.hstack(lst_last_weeks_ind)
        df_date['last_fiscal_week_of_fiscal_month_ind'] = pd.Series(output_lst_weeks_ind)
        return df_date

    def add_last_year_fiscal_year(self, df_date):
        df_date['last_year_fiscal_year'] = df_date['fiscal_year'].apply(lambda x: int(x) - 1)
        return df_date

    def add_last_year_fiscal_month_of_year(self, df_date):
        # Shift 364 places to get the last year fiscal month of year
        df_date['last_year_fiscal_month_of_year'] = df_date['fiscal_month_of_year'].shift(364)

        # Set variables needed
        month_counter = 1
        lst_last_fiscal_month = []
        lst_last_fiscal_months = []

        # Get the fiscal year start month based on the start date
        fiscal_year_start_month = pd.to_datetime(self.start_date).month

        # Iterate over the array which contains if 28 days or 35 days created at the top of the notebook
        for num_days in self.lst_months[:12]:  # Use the first 12 months

            # Adjust the month counter based on the fiscal year start month
            current_month = (month_counter + fiscal_year_start_month - 2) % 12 + 1

            # Repeat the month number for the corresponding number of days
            lst_last_fiscal_month = np.repeat([current_month], len(num_days))
            month_counter += 1

            # Append to a new list for each month the array of month number -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, or 12
            # Either 28 or 35 repeated in a list
            lst_last_fiscal_months.append(lst_last_fiscal_month)

        # Unstack the list of lists to a single list
        output_month_number = np.hstack(lst_last_fiscal_months)

        # Fill NaN values with the dynamically calculated month numbers
        df_date['last_year_fiscal_month_of_year'].fillna(pd.Series(list(output_month_number)), inplace=True)

        # Convert float to integer
        df_date['last_year_fiscal_month_of_year'] = df_date['last_year_fiscal_month_of_year'].astype(int)

        return df_date

    def add_fiscal_month_start_date(self, df_date):
        df_date['fiscal_month_start_date'] = pd.Series(
            np.repeat(df_date['Date'].min(), len(df_date))).apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_fiscal_month_end_date(self, df_date):
        df_date['fiscal_month_end_date'] = pd.Series(
            np.repeat(df_date['Date'].min() + pd.DateOffset(days=28 - 1), len(df_date))).apply(
            lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_fiscal_month_number_of_weeks(self, df_date):
        """
        Add a column 'fiscal_month_number_of_weeks' to the DataFrame representing the number of weeks in each fiscal month.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'Date' column.

        This method calculates and adds a new column 'fiscal_month_number_of_weeks' to the DataFrame. The values in this column
        represent the number of weeks in each fiscal month based on the provided 'Date' column.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_month_number_of_weeks' representing the number of weeks in each fiscal month.
        """
        lst_mymonths = []
        for num_days in self.lst_months:
            lst_mymonth = np.repeat(int((len(num_days) / 7)), len(num_days))
            lst_mymonths.append(lst_mymonth)
        output_lst_mymonths = np.hstack(lst_mymonths)
        df_date['fiscal_month_number_of_weeks'] = pd.Series(list(output_lst_mymonths))
        return df_date

    def add_fiscal_month_number_of_days(self, df_date):
        """
        Add a column 'fiscal_month_number_of_days' to the DataFrame representing the number of days in each fiscal month.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'Date' column.

        This method calculates and adds a new column 'fiscal_month_number_of_days' to the DataFrame. The values in this column
        represent the number of days in each fiscal month based on the provided 'Date' column.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_month_number_of_days' representing the number of days in each fiscal month.
        """
        lst_myday = []
        lst_mydays = []
        for num_days in self.lst_months:
            lst_myday = np.repeat(int(len(num_days)), len(num_days))
            lst_mydays.append(lst_myday)
        output_lst_mydays = np.hstack(lst_mydays)
        df_date['fiscal_month_number_of_days'] = pd.Series(list(output_lst_mydays))
        return df_date

    def add_fiscal_year_start_date(self, df_date):
        """
        Add a column 'fiscal_year_start_date' to the DataFrame representing the start date of the fiscal year.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'Date' column.

        This method calculates and adds a new column 'fiscal_year_start_date' to the DataFrame. The values in this column
        represent the start date of the fiscal year based on the provided 'Date' column. The calculation considers the
        cumulative count of days in each month to determine the fiscal year start date.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_year_start_date' representing the fiscal year's start date.
        """
        # counter for number of days in year
        count_days = 0
        # counter for month number in for loop
        counter_months = 0
        # container to hold start date x number of times per year in array
        lst_year_days = []
        # define start date as the minimum date found within the df_date dataframe defined by user
        my_start_date = df_date['Date'].min()

        # iterate over the list of months
        for month_iterator in self.lst_months:

            # sum the days for each month up to the 12th month
            count_days += len(month_iterator)
            counter_months += 1

            # if 12th month in loop -> determine the total number of days in year of the 12 months to update fiscal
            # start date
            if counter_months == 12:
                # repeat fiscal start date x number of times whereby x equal to days in fiscal year e.g. 364 or 371
                lst_year_days.append(np.repeat(my_start_date, count_days))
                # update start date
                my_start_date += timedelta(days=count_days)

                # reset the counters
                count_days = 0
                counter_months = 0

        # unstack the list of lists to a single list
        output_lst_start_dates = np.hstack(lst_year_days)

        # convert list of months to pandas dataframe series
        df_date['fiscal_year_start_date'] = pd.Series(list(output_lst_start_dates))

        # change format to <m/d/yyyy>
        df_date['fiscal_year_start_date'] = df_date['fiscal_year_start_date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_fiscal_year_end_date(self, df_date):
        """
        Add a column 'fiscal_year_end_date' to the DataFrame representing the end date of the fiscal year.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'Date' column.

        This method calculates and adds a new column 'fiscal_year_end_date' to the DataFrame. The values in this column
        represent the end date of the fiscal year based on the provided 'Date' column. The calculation considers the
        cumulative count of days in each month to determine the fiscal year end date.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_year_end_date' i.e. fiscal year's end date.
        """
        count_days = 0
        counter_months = 0
        lst_num_days = []

        # Use the minimum date from df_date as the initial my_start_date
        my_start_date = df_date['Date'].min()
        my_end_date = my_start_date

        for i in self.lst_months:
            count_days += len(i)
            counter_months += 1
            if counter_months == 12:
                # Use my_end_date as the starting point for the fiscal year end date
                lst_num_days.append(np.repeat((my_end_date + timedelta(days=(count_days - 1))), count_days))
                my_end_date += timedelta(days=count_days)
                count_days = 0
                counter_months = 0

        output_lst_end_dates = np.hstack(lst_num_days)
        df_date['fiscal_year_end_date'] = pd.Series(list(output_lst_end_dates))
        df_date['fiscal_year_end_date'] = df_date['fiscal_year_end_date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date

    def add_fiscal_year_number_of_weeks(self, df_date):
        """
        Add a column 'fiscal_year_number_of_weeks' to the DataFrame based on the configured fiscal months.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the date information.

        This method adds a new column 'fiscal_year_number_of_weeks' to the DataFrame. The values in this column
        represent the number of fiscal weeks in each corresponding fiscal year. The calculation is based on the
        configured fiscal months and assumes either 364 or 371 days in a fiscal year.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_year_number_of_weeks' representing the number
                          of fiscal weeks in each corresponding fiscal year.
        """
        # container to hold end date repeated x number of times per year in array with x equal to 364 or 371
        lst_num_weeks = []
        # counter for number of days in year
        count_days = 0
        # counter for month number in for loop
        counter_months = 0

        # iterate over the list of months
        for i in self.lst_months:
            # sum the days for each month up to the 12th month
            count_days += len(i)
            # increment the counter for the number of months
            counter_months += 1

            # if 12 months are iterated over add all the days to check if 364 or 371 days
            if counter_months == 12:
                # Check if count_days is equal to 364 or 371
                if count_days == 364:
                    # Repeat fiscal end date x number of times whereby x equal to days in fiscal year e.g. 364 or 371
                    lst_num_weeks.append(np.repeat(52, count_days))
                elif count_days == 371:
                    lst_num_weeks.append(np.repeat(53, count_days))

                # Reset the counters after every fiscal year (e.g., every 12 months)
                count_days = 0
                counter_months = 0

        # unstack the list of lists to a single list
        output_lst_num_weeks = np.hstack(lst_num_weeks)

        # convert list of months to pandas dataframe series
        df_date['fiscal_year_number_of_weeks'] = pd.Series(list(output_lst_num_weeks))
        return df_date

    def add_fiscal_year_number_of_days(self, df_date):
        """
        Add a column 'fiscal_year_number_of_days' to the DataFrame based on 'fiscal_year_number_of_weeks'.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'fiscal_year_number_of_weeks' column.

        This method adds a new column 'fiscal_year_number_of_days' to the DataFrame. The values in this column
        are calculated by multiplying the corresponding values in the 'fiscal_year_number_of_weeks' column by 7,
        assuming each week has 7 days.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'fiscal_year_number_of_days' calculated from
                          'fiscal_year_number_of_weeks'.
        """
        df_date['fiscal_year_number_of_days'] = df_date['fiscal_year_number_of_weeks'].apply(lambda x: x * 7)
        return df_date

    def add_time_day_id_pk_int(self, df_date):
        """
        Add an integer version of 'time_day_id_pk' to the DataFrame as 'time_day_id_pk_int'.

        Parameters:
            df_date (pd.DataFrame): DataFrame containing the 'time_day_id_pk' column to be converted.

        This method adds a new column 'time_day_id_pk_int' to the DataFrame, which is a converted version
        of the existing 'time_day_id_pk' column. The conversion is done by casting the 'time_day_id_pk'
        column to the 'int64' data type.

        Returns:
            pd.DataFrame: DataFrame with an additional column 'time_day_id_pk_int' containing integer values.
        ```
        """
        df_date['time_day_id_pk_int'] = df_date['time_day_id_pk'].astype('int64')
        return df_date
