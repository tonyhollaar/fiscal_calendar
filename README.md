![Fiscal Calendar Logo](fiscal_calendar_logo.png)

# Fiscal Retail Calendar - 4-5-4 week retail calendar
The Fiscal Retail Calendar is structured based on the 4-5-4 week schema and the 4-5-5 week schema, 
accommodating a 53rd week every 5 or 6 years, contingent on leap years (i.e., an additional day). 
In this fiscal calendar, we assume 364 days in a standard year or 371 days in a leap year with a 53rd week.

# Notes
- With a 53rd week (e.g., 4-5-5 calendar if applicable), 
exemplified in years such as 2006, 2012, 2017, 2023 (totaling 371 days), the code also considers leap years. 
The 53rd week adjusts for the fact that each fiscal year comprises 364 days versus the standard ~365 days. 
Consequently, the fiscal start date for each subsequent year begins either -1 day earlier or -2 days earlier in the case of a leap year. 
To rectify this, an additional week (+7 days) is added if the fiscal year-end date is before January 28th, which is >-4 days from 01-31-year. Conn's fiscal year concludes on the last Saturday of the fiscal month, and the new fiscal start date commences on Sunday.

- Fiscal calendar below can be set with dynamic start-date and end-date.
Currently successfully tested with start-date assumption of 364 days in first year up to dynamic end-date.

## Installation
You can install the package using pip:
```bash
pip install fiscal_calendar
```

## Usage
```python
from fiscal_calendar import FiscalCalendarGenerator

# Instantiate the FiscalCalendarGenerator class
fiscal_calendar_generator = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2031-01-04')

# Generate the fiscal calendar
df_fiscal_calendar = fiscal_calendar_generator.create_dataframe()

# Print the DataFrame
print(df_fiscal_calendar)

# Save the DataFrame to a CSV file
df_fiscal_calendar.to_csv('fiscal_calendar_old.csv', index=False)
```

## Features
Dynamic Start and End Dates: The fiscal calendar can be generated with dynamic start and end dates.
Dataframe Output: The calendar is returned as a pandas DataFrame for easy integration into your data pipeline.
Leap Year Handling: The package takes leap years into account and adjusts for the discrepancy in the number of days.

## Reference Materials:
- [Wikipedia 4–4–5 calendar](https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar)
- [National Retail Federation (NFR)](https://nrf.com/resources/4-5-4-calendar)

## Data Dictionary
Here is a data dictionary describing the columns in the generated fiscal calendar DataFrame.

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

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The 4-5-4 calendar concept was derived in the 1930s during an informal inter-industry discussion. It has since become widely followed by retailers for sales reporting purposes.
Feel free to contribute, report issues, or suggest improvements!