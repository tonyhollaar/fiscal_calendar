# -*- coding: utf-8 -*-
"""Fiscal Calendar

# Create Fiscal Calendar - 4-5-4 week retail calendar dynamic start/end-dates** **Goal:** Create Retail Calendar
which is based on the 4-5-4 week schema and 4-5-5 week schema in case of a 53rd week every 5 or 6 years (dependent on
leap year e.g. additional day) e.g. fiscal calendar assumes 364 days in a year or 371 days in a year with 53rd week.

Note1: with 53rd week e.g. 4-5-5 calendar if applicable -> for example years: 2006, 2012, 2017,
2023 all have 53rd week e.g. 371 days. <br> Additionally code takes leap years into account. <br> 53rd week adjusts
for fact each fiscal year has 364 days versus ~365 days in year. Therefore every next year's fiscal start date is
starting -1 day earlier or -2 if leap year. To adjust for the discrepency an additional week (+7 days) is added if
fiscal year end date is before e.g. 28th of jan which is >-4 days from 01-31-year. Conn's fiscal year ends on last
saturday of fiscal month and new fiscal start date starts sunday.

<br> **Note2:** Fiscal calendar below can be set with dynamic start-date and end-date.
Currently successfully tested with start-date assumption of 364 days in first year up to dynamic end-date.

<br> **Reference Materials:**
- https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar
- https://nrf.com/resources/4-5-4-calendar

DATA DICTIONARY

| #  | Name                                     | Definition                                                                                                                                                                                | Data Type | Possible Values                                                                                                   |
|----|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------|
| 1  | time_day_id_pk                           | Primary key of date in format yyyymmdd, e.g., 20220130                                                                                                                                    | object    | <yyyymmdd>                                                                                                        |
| 2  | day_date                                 | Date in format m/d/yyyy, e.g., 1/30/2022                                                                                                                                                  |           | <m/d/yyyy>                                                                                                        |
| 3  | day_of_week_short_name                   | 3-letter weekday capitalized, e.g., SUN for Sunday                                                                                                                                        |           | <SUN, MON, TUE, WED, THU, FRI, SAT>                                                                               |
| 4  | day_of_week_name                         | Day of the week name capitalized, e.g., SUNDAY                                                                                                                                            |           | <SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY>                                                  |
| 5  | day_of_week_letter                       | Unique day of the week letter, e.g., U for Sunday, S for Saturday, H for Thursday etc.                                                                                                    |           | <U, M, T, W, H, F, S> *Sunday = U, Monday = M, Tuesday = T, Wednesday = W, Thursday = H, Friday = F, Saturday = S |
| 6  | fiscal_day_of_week                       | Fiscal day of the week with Sunday equal to 1 up to Saturday equal to 7                                                                                                                   |           | <1, 2, 3, 4, 5, 6, 7 > *Sunday=1, Monday=2, Tuesday=3, Wednesday=4, Thursday=5, Friday=6, Saturday=7              |
| 7  | fiscal_week_of_year                      | Fiscal week of the fiscal year number with either every week in the year numbered 1 through 52 or 1 through 53 (if 53rd week in the year)                                                 |           | <1, 2, 3…52, 53>                                                                                                  |
| 8  | fiscal_week_of_season                    | Fiscal week of the season with every year divided into two seasons. Each week of the season is numbered 1 through 26 weeks or 1 through 27 weeks (if 53rd week in the year)               |           | <1, 2, 3…26, 27>                                                                                                  |
| 9  | fiscal_week_of_quarter                   | Fiscal week of the fiscal quarter with every year divided into four quarters. Each week of the quarter is numbered 1 through 13 weeks or 1 through 14 weeks (if 53rd week in the year)    |           | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14>                                                                   |
| 10 | fiscal_week_of_month                     | Fiscal week of the fiscal month with every month having either 4 weeks or 5 weeks based on the 4-5-4 schema and 4-5-5 schema if 53rd week                                                 |           | <4, 5>                                                                                                            |
| 11 | fiscal_week_start_date                   | Fiscal week start date of every fiscal week in format m/d/yyyy, e.g., 1/29/2023                                                                                                           |           | <m/d/yyyy>                                                                                                        |
| 12 | fiscal_week_end_date                     | Fiscal week end date of every fiscal week, e.g., 2/4/2023                                                                                                                                 |           | <m/d/yyyy>                                                                                                        |
| 13 | fiscal_week_iso_code                     | Fiscal week ISO code of every fiscal week, e.g., 2005W01                                                                                                                                  |           | <yyyy><'W'><ww>                                                                                                   |
| 14 | fiscal_month_of_year                     | Fiscal month of the fiscal year with each month numbered 1 through 12 for every fiscal year                                                                                               |           | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>                                                                           |
| 15 | fiscal_month_of_season                   | Fiscal month of the fiscal season. Each year has two seasons with 6 months each, numbered 1 through 6                                                                                     |           | <1, 2, 3, 4, 5, 6>                                                                                                |
| 16 | fiscal_month_of_quarter                  | Fiscal month of the fiscal quarter. Each fiscal quarter has 3 months, and fiscal month numbered 1 through 3                                                                               |           | <1, 2, 3>                                                                                                         |
| 17 | fiscal_month_name                        | Fiscal month name with the first letter capitalized of each of the 12 fiscal months names, e.g., February                                                                                 |           | <January, February, March, April, May, June, July, August, September, October, November, December>                |
| 18 | fiscal_month_short_name                  | Fiscal month short name of the first 3 letters of the month name and the first letter capitalized for the 12 fiscal months in the year, e.g., Feb                                         |           | <Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep>                                                                     |
| 19 | fiscal_month_start_date                  | Fiscal month start date - return for fiscal_month_of_year its respective fiscal month start date in format 1/29/2023                                                                      |           | <m/d/yyyy>                                                                                                        |
| 20 | fiscal_month_end_date                    | Fiscal month end date - return for fiscal_month_of_year its respective fiscal month end date in format 2/25/2023                                                                          |           | <m/d/yyyy>                                                                                                        |
| 21 | fiscal_month_number_of_weeks             | Fiscal month number of weeks - either 4 or 5 weeks in a fiscal month based on the 4-5-4 week or 4-5-5 weeks schema if 53rd week                                                           |           | <4, 5>                                                                                                            |
| 22 | fiscal_month_number_of_days              | Fiscal month number of days - either 28 days or 35 days in a fiscal month                                                                                                                 |           | <28, 35>                                                                                                          |
| 23 | fiscal_quarter_of_year                   | Fiscal quarter of the fiscal year in format <'Q'+fiscal quarter number> e.g., with every quarter being labelled as Q1,…,Q4                                                                |           | <Q1, Q2, Q3, Q4>                                                                                                  |
| 24 | fiscal_quarter_of_year_str               | Fiscal quarter of the fiscal year as a string, e.g., 'Q1'                                                                                                                                 |           | <Q1, Q2, Q3, Q4>                                                                                                  |
| 25 | fiscal_quarter_of_season                 | Fiscal quarter of the fiscal season - equal to 1 IF 1st OR 3rd fiscal quarter of the year ELSE equal to 2 IF 2nd OR 4th fiscal quarter of the year                                        |           | <1, 2>                                                                                                            |
| 26 | fiscal_season_of_year                    | Fiscal season of the year - equal to 1 IF 1st or 2nd fiscal quarter of the year ELSE equal to 2 IF 3rd or 4th fiscal quarter of the year                                                  |           | <1, 2>                                                                                                            |
| 27 | fiscal_season_name                       | Fiscal season name - equal to SPRING IF fiscal_season_of_year = 1 ELSE equal to FALL if fiscal_season_of_year = 2                                                                         |           | <SPRING, FALL>                                                                                                    |
| 28 | fiscal_year                              | Fiscal year - running from fiscal start date to fiscal end date for each year starting on the last Sunday (unless 53rd week +7days) of the month January up to the last Saturday of January, e.g., 2022 |           | <yyyy>                                                                                              |
| 29 | fiscal_year_2_digit                      | Fiscal year 2 digits - last 2 out of 4 characters of fiscal year in yyyy format, e.g., fiscal year: 2022 becomes fiscal_year_2_digit: 22                                                  |           | <yy>                                                                                                              |
| 30 | fiscal_year_start_date                   | Fiscal year start date - return for fiscal_year its respective fiscal year start date in format 1/30/2022                                                                                 |           | <m/d/yyyy>                                                                                                        |
| 31 | fiscal_year_end_date                     | Fiscal year end date - return for fiscal_year its respective fiscal year end date in format 1/28/2023                                                                                     |           | <m/d/yyyy>                                                                                                        |
| 32 | fiscal_year_number_of_weeks              | Fiscal year number of weeks - either 52 or 53 weeks in a fiscal year based on whether there is a 53rd week in the year                                                                    |           | <52, 53>                                                                                                          |
| 33 | fiscal_year_number_of_days               | Fiscal year number of days - either 364 days or 371 days in a fiscal year                                                                                                                 |           | <364, 371>                                                                                                        |
| 34 | last_year_equiv_day_fk                   | Last year equivalent day foreign key - day_date date minus 364 days to retrieve the date from last year for comparison purposes, e.g., 20220130                                           |           | <yyyymmdd>                                                                                                        |
| 35 | last_year_equiv_week_fk                  | Last year equivalent fiscal week foreign key - lookup for the last year equivalent date (current day_date-364 days) and return the respective fiscal week, e.g., 2022W01                  |           | <yyyy><'W'><ww>                                                                                                   |
| 36 | last_year_equiv_day_date                 | Last year equivalent day date - return for the last_year_equiv_day_fk its respective date in format 1/30/2022                                                                             |           | <m/d/yyyy>                                                                                                        |
| 37 | last_year_fiscal_year                    | Last year fiscal year - return for the last_year_equiv_day_fk its respective fiscal year in format 2022                                                                                   |           | <yyyy>                                                                                                            |
| 38 | last_year_fiscal_month_of_year           | Last year fiscal month of the fiscal year - return for the last_year_equiv_day_fk its respective fiscal month of the year in format 1-12                                                  |           | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>                                                                           |
| 39 | prior_year_from_last_year_equiv_day_fk   | Prior year from the last year equivalent day foreign key - day_date date minus 730 days to retrieve the date from two years ago for comparison purposes, e.g., 20200130                   |           | <yyyymmdd>                                                                                                        |
| 40 | prior_year_from_last_year_equiv_day_date | Prior year from the last year equivalent day date - return for the prior_year_from_last_year_equiv_day_fk its respective date in format 1/30/2020                                         |           | <m/d/yyyy>                                                                                                        |
| 41 | time_fiscal_week_id_fk                   | Fiscal week ID foreign key - fiscal week ISO code of every fiscal week, e.g., 2005W01.  note:                                                                                             |           | <yyyy><'W'><ww>                                                                                                   |
| 42 | first_fiscal_week_of_fiscal_month_ind   | First fiscal week of the fiscal month indicator - equal to 1 IF fiscal_week_of_month = 1 ELSE equal to 0                                                                                   |           | <0, 1>                                                                                                            |
| 43 | last_fiscal_week_of_fiscal_month_ind    | Last fiscal week of the fiscal month indicator - equal to 1 IF fiscal_week_of_month = fiscal_month_number_of_weeks ELSE equal to 0                                                         |           | <0, 1>                                                                                                            |
| 44 | time_day_id_pk_int                       | Integer representation of time_day_id_pk, e.g., 20220130 is represented as 20220130                                                                                                       | int       | <integer value>                                                                                                   |
"""

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import calendar


class FiscalCalendarGenerator:
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

    def check_and_shift_start_date(self):
        """
        Checks if the start date is within the last 5 days of the month.
        If it is, shifts the month_name_dict by one.
        """
        start_date = pd.to_datetime(self.start_date)
        if start_date.day > calendar.monthrange(start_date.year, start_date.month)[1] - 5:
            # Shift the month_name_dict by one
            self.month_name_dict = {k-1 if k!=1 else 12: v for k, v in self.month_name_dict.items()}

    def leap_year(self, myyear):
        return 1 if ((myyear % 4 == 0 and myyear % 100 != 0) or (myyear % 400 == 0)) else 0

    def delta_days(self, mydate):
        fiscal_start_date_dt = datetime.strptime(mydate, self.date_format)
        fsd_year = fiscal_start_date_dt.year
        jan_end_date = datetime(fsd_year + 1, 1, 31)
        y = fiscal_start_date_dt + timedelta(days=364 - 1)
        delta = abs(y - jan_end_date)
        return delta.days

    def generate_fiscal_calendar(self):
        self.check_and_shift_start_date()

        fiscal_start_date = self.start_date
        fiscal_start_date_dt = datetime.strptime(fiscal_start_date, self.date_format)
        #fiscal_day = fiscal_start_date_dt.day
        fiscal_month = fiscal_start_date_dt.month
        fiscal_year = fiscal_start_date_dt.year
        self.lst_months = []
        fifthy_third_week = 0
        lst_array = []
        lst_fiscal_weeks = []
        lst_fiscalqtrs = []
        lst_years = []
        df_date = pd.DataFrame(pd.date_range(start=self.start_date, end=self.end_date), columns=['Date'])

        years_count = (df_date['Date'].max().year - df_date['Date'].min().year) + 1

        for year in range(1, years_count + 1):
            fiscal_year += 1
            if year != 1:
                month = 1
            else:
                month = fiscal_month

            for i in range(month, 12 + 1):
                if (self.delta_days(fiscal_start_date) >= 4) and (self.month_dict.get(i) == 'Dec'):
                    num_weeks = 5
                    fifthy_third_week = 7
                elif ((i - 2) % 3 == 0):
                    num_weeks = 5
                else:
                    num_weeks = 4

                my_array = np.repeat(self.month_dict.get(i), (num_weeks * self.num_days))
                lst_array.append(len(my_array))

                if len(lst_array) == 12:
                    y = np.array(list(np.arange(0, 4) + 1))
                    y = np.char.mod('%d', y)
                    y = np.char.add('Q', y)
                    lst_fiscalqtr = np.repeat(y, 91)

                    if sum(lst_array) == 364:
                        x = np.array(list(np.arange(0, 52) + 1))
                    elif sum(lst_array) == 371:
                        x = np.array(list(np.arange(0, 53) + 1))
                        lst_fiscalqtr = np.append(lst_fiscalqtr, ['Q4'] * 7)
                    else:
                        continue

                    weeknumber_lst = np.repeat(x, self.num_days)
                    lst_fiscal_weeks.append(weeknumber_lst)
                    lst_array = []
                    lst_fiscalqtrs.append(lst_fiscalqtr)

                self.lst_months.append(my_array)

            fiscal_start_date_dt = datetime.strptime(fiscal_start_date, self.date_format)
            lst_year = np.repeat((fiscal_year - 1), (364 + fifthy_third_week))
            lst_years.append(lst_year)
            fiscal_start_date = (fiscal_start_date_dt + timedelta(days=364 + fifthy_third_week)).strftime(self.date_format)
            fifthy_third_week = 0

        output_wks = np.hstack(lst_fiscal_weeks)
        df_date['Fiscal Wk'] = pd.Series(list(output_wks))
        df_date['Weekday'] = df_date['Date'].dt.day_name()
        df_date['Day'] = df_date['Weekday'].map(
            {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7})
        output_months = np.hstack(self.lst_months)
        df_date['Fiscal Month'] = pd.Series(list(output_months))
        output_qtrs = np.hstack(lst_fiscalqtrs)
        df_date['Fiscal Qtr'] = pd.Series(list(output_qtrs))
        output_years = np.hstack(lst_years)
        df_date['Fiscal Year'] = pd.Series(list(output_years)).astype('str')

        return df_date

    def create_dataframe(self):
        # Set the display option to None
        #pd.set_option('display.max_columns', None)

        df_date_copy = self.generate_fiscal_calendar()
        df_date_copy.to_csv('fiscal_calendar.csv', index=False)

        # removed changing 'Date' to 'time_day_id_pk'
        df_fiscal_calendar = self.add_time_day_id_pk(df_date_copy)  # Column 1: time_day_id_pk
        df_fiscal_calendar = self.add_day_date(df_fiscal_calendar)  # Column 2: day_date
        df_fiscal_calendar = self.add_day_of_week_short_name(df_fiscal_calendar)  # Column 3: day_of_week_short_name
        df_fiscal_calendar = self.add_day_of_week_name(df_fiscal_calendar)  # Column 7: day_of_week_name
        df_fiscal_calendar = self.add_day_of_week_letter(df_fiscal_calendar)  # Column 9: day_of_week_letter
        df_fiscal_calendar = self.add_fiscal_day_of_week(df_fiscal_calendar)  # Column 4: fiscal_day_of_week
        df_fiscal_calendar = self.add_fiscal_week_of_year(df_fiscal_calendar)  # Column 10: fiscal_week_of_year
        df_fiscal_calendar = self.add_fiscal_week_of_season(df_fiscal_calendar)  # Column 11: fiscal_week_of_season
        df_fiscal_calendar = self.add_fiscal_week_of_quarter(df_fiscal_calendar)  # Column 12: fiscal_week_of_quarter
        df_fiscal_calendar = self.add_fiscal_week_of_month(df_fiscal_calendar)  # Column 13: fiscal_week_of_month
        df_fiscal_calendar = self.add_fiscal_week_start_date(df_fiscal_calendar)  # Column 5: fiscal_week_start_date
        df_fiscal_calendar = self.add_fiscal_week_end_date(df_fiscal_calendar)  # Column 8: fiscal_week_end_date
        df_fiscal_calendar = self.add_fiscal_week_iso_code(df_fiscal_calendar)  # Column 6: fiscal_week_iso_code
        df_fiscal_calendar = self.add_fiscal_month_of_year(df_fiscal_calendar)  # Column 14: fiscal_month_of_year
        df_fiscal_calendar = self.add_fiscal_month_of_season(df_fiscal_calendar)  # Column 15: fiscal_month_of_season
        df_fiscal_calendar = self.add_fiscal_month_of_quarter(df_fiscal_calendar)  # Column 16: fiscal_month_of_quarter
        df_fiscal_calendar = self.add_fiscal_month_name(df_fiscal_calendar)  # Column 17: fiscal_month_name
        df_fiscal_calendar = self.add_fiscal_month_short_name(df_fiscal_calendar)  # Column 18: fiscal_month_short_name
        df_fiscal_calendar = self.add_fiscal_month_start_date(df_fiscal_calendar)  # Column 36: fiscal_month_start_date
        df_fiscal_calendar = self.add_fiscal_month_end_date(df_fiscal_calendar)  # Column 37: fiscal_month_end_date
        df_fiscal_calendar = self.add_fiscal_month_number_of_weeks(df_fiscal_calendar)  # Column 38: fiscal_month_number_of_weeks
        df_fiscal_calendar = self.add_fiscal_month_number_of_days(df_fiscal_calendar)  # Column 39: fiscal_month_number_of_days
        df_fiscal_calendar = self.add_fiscal_quarter_of_year(df_fiscal_calendar)  # Column 19: fiscal_quarter_of_year
        df_fiscal_calendar = self.add_fiscal_quarter_of_year_str(df_fiscal_calendar) # Column 20: fiscal_quarter_of_year_str
        df_fiscal_calendar = self.add_fiscal_quarter_of_season(df_fiscal_calendar)  # Column 21: fiscal_quarter_of_season
        df_fiscal_calendar = self.add_fiscal_season_of_year(df_fiscal_calendar)  # Column 22: fiscal_season_of_year
        df_fiscal_calendar = self.add_fiscal_season_name(df_fiscal_calendar)  # Column 23: fiscal_season_name
        df_fiscal_calendar = self.add_fiscal_year(df_fiscal_calendar)  # Column 24: fiscal_year
        df_fiscal_calendar = self.add_fiscal_year_2_digit(df_fiscal_calendar)  # Column 25: fiscal_year_2_digit
        df_fiscal_calendar = self.add_fiscal_year_start_date(df_fiscal_calendar)  # Column 40: fiscal_year_start_date
        df_fiscal_calendar = self.add_fiscal_year_end_date(df_fiscal_calendar)  # Column 41: fiscal_year_end_date
        df_fiscal_calendar = self.add_fiscal_year_number_of_weeks(df_fiscal_calendar)  # Column 42: fiscal_year_number_of_weeks
        df_fiscal_calendar = self.add_fiscal_year_number_of_days(df_fiscal_calendar)  # Column 43: fiscal_year_number_of_days
        df_fiscal_calendar = self.add_last_year_equiv_day_fk(df_fiscal_calendar)  # Column 26: last_year_equiv_day_fk
        df_fiscal_calendar = self.calculate_last_year_equiv_week_fk(df_fiscal_calendar)  # Column 27: last_year_equiv_week_fk
        df_fiscal_calendar = self.add_last_year_equiv_day_date(df_fiscal_calendar)  # Column 30: last_year_equiv_day_date
        df_fiscal_calendar = self.add_last_year_fiscal_year(df_fiscal_calendar)  # Column 34: last_year_fiscal_year
        df_fiscal_calendar = self.add_last_year_fiscal_month_of_year(df_fiscal_calendar)  # Column 35: last_year_fiscal_month_of_year
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_day_fk(
            df_fiscal_calendar)  # Column 29: prior_year_from_last_year_equiv_day_fk
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_week_fk(
            df_fiscal_calendar)  # Column 30: prior_year_from_last_year_equiv_week_fk
        df_fiscal_calendar = self.add_prior_year_from_last_year_equiv_day_date(
            df_fiscal_calendar)  # Column 31: prior_year_from_last_year_equiv_day_date
        df_fiscal_calendar = self.add_time_fiscal_week_id_fk(df_fiscal_calendar)  # Column 28: time_fiscal_week_id_fk
        df_fiscal_calendar = self.add_first_fiscal_week_of_fiscal_month_ind(
            df_fiscal_calendar)  # Column 32: first_fiscal_week_of_fiscal_month_ind
        df_fiscal_calendar = self.add_last_fiscal_week_of_fiscal_month_ind(
            df_fiscal_calendar)  # Column 33: last_fiscal_week_of_fiscal_month_ind
        df_fiscal_calendar = self.add_time_day_id_pk_int(df_fiscal_calendar)  # Column 44: time_day_id_pk_int

        # drop temporary columns that were needed to calculate above columns
        df_fiscal_calendar = df_fiscal_calendar.drop(
            columns=['Date', 'Fiscal Wk', 'Weekday', 'Day', 'Fiscal Month', 'Fiscal Qtr', 'Fiscal Year'])

        return df_fiscal_calendar

    def add_time_day_id_pk(self, df_date):
        """
        This method adds a new column 'time_day_id_pk' and formats the dates in 'Date' to 'yyyymmdd'.

        Args:
            df_date (pd.DataFrame): DataFrame that contains the 'Date' column.

        Returns:
            pd.DataFrame: The updated DataFrame with the new 'time_day_id_pk' column.
        """
        df_date['time_day_id_pk'] = df_date['Date'].apply(lambda x: x.strftime('%Y%m%d'))
        return df_date

    def add_day_date(self, df_date):
        df_date['day_date'] = df_date['Date'].copy()
        df_date['day_date'] = df_date['day_date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        return df_date
    def add_day_of_week_short_name(self, df_date):
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
            elif fiscal_year_counts.iloc[daysyear] == 366:
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

        Examples:
            df = add_fiscal_month_name(df)
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
        df_date['last_year_equiv_week_fk'] = df_date['fiscal_week_iso_code'].shift(364)

        # iterate over all rows of the dataframe
        for i in range(len(df_date)):
            # e.g. start from 0 so it will be for 364 days iterate 364 times
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
        # Convert 'Fiscal Year' to numeric
        df_date['Fiscal Year'] = pd.to_numeric(df_date['Fiscal Year'], errors='coerce')

        # Assuming 'Fiscal Year' is the column containing the fiscal year
        df_date['last_year_fiscal_year'] = df_date['Fiscal Year'] - 1

        # Check for leap year
        is_leap_year = pd.to_datetime(df_date['Date']).dt.is_leap_year

        # Adjust for leap year
        df_date.loc[is_leap_year, 'last_year_fiscal_year'] = df_date['last_year_fiscal_year'] - 1

        return df_date

    # def add_last_year_fiscal_month_of_year(self, df_date):
    #     # shift 364 places all the months to get the last year fiscal month of year
    #     # however first year will have NAN and need to fill out the 4-5-4 schema for 1st year e.g. for 28 days first month 1 repeated 28 times, then 2nd month 35 times, 3rd month 28 times, 4th month 28 times, 5th month 35 times etc, 6th month 28 times
    #     df_date['last_year_fiscal_month_of_year'] = df_date['fiscal_month_of_year'].shift(364)
    #
    #     # set variables needed
    #     month_counter = 1
    #     lst_last_fiscal_month = []
    #     lst_last_fiscal_months = []
    #
    #     # iterate over the array which contains if 28 days or 35 days created at top of notebook and slice only first 12 numbers to get the 4-5-4 schema for first year
    #     for num_days in self.lst_months[0:12]:
    #         lst_last_fiscal_month = np.repeat([month_counter], [len(num_days)])
    #         month_counter += 1
    #         # append to new list for each month the array of month number e.g. 1,2,3,4,5,6,7,8,9,10,11 or 12 -> either 28 or 35 repeated in a list
    #         lst_last_fiscal_months.append(lst_last_fiscal_month)
    #
    #     # unstack the list of lists to a single list
    #     output_monthnumber = np.hstack(lst_last_fiscal_months)
    #
    #     # convert list of months to pandas dataframe series e.g. add 1st year of last_year_fiscal_month_of_year numbers
    #     #df_date['last_year_fiscal_month_of_year'][0:364] = pd.Series(list(output_monthnumber))
    #
    #     df_date.loc[0:364, 'last_year_fiscal_month_of_year'] = pd.Series(list(output_monthnumber))
    #     # convert float to integer
    #     df_date['last_year_fiscal_month_of_year'] = df_date[
    #         'last_year_fiscal_month_of_year'].astype(int)
    #     return df_date
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

            # Append to a new list for each month the array of month number e.g., 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, or 12
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
        lst_mymonth = []
        lst_mymonths = []
        for num_days in self.lst_months:
            lst_mymonth = np.repeat(int((len(num_days)/7)), len(num_days))
            lst_mymonths.append(lst_mymonth)
        output_lst_mymonths = np.hstack(lst_mymonths)
        df_date['fiscal_month_number_of_weeks'] = pd.Series(list(output_lst_mymonths))
        return df_date

    def add_fiscal_month_number_of_days(self, df_date):
        lst_myday = []
        lst_mydays = []
        for num_days in self.lst_months:
            lst_myday = np.repeat(int(len(num_days)), len(num_days))
            lst_mydays.append(lst_myday)
        output_lst_mydays = np.hstack(lst_mydays)
        df_date['fiscal_month_number_of_days'] = pd.Series(list(output_lst_mydays))
        return df_date

    def add_fiscal_year_start_date(self, df_date):
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
            # if 12th month in loop -> determine the total number of days in year of the 12 months to update fiscal start date
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
        df_date['fiscal_year_number_of_days'] = df_date['fiscal_year_number_of_weeks'].apply(lambda x: x*7)
        return df_date

    def add_time_day_id_pk_int(self, df_date):
        df_date['time_day_id_pk_int'] = df_date['time_day_id_pk'].astype('int64')
        return df_date
