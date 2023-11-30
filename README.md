<div align="center">

![PyPI Version](https://img.shields.io/pypi/v/fiscal-calendar.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fiscal-calendar)
![GitHub last commit](https://img.shields.io/github/last-commit/tonyhollaar/fiscal_calendar)
![GitHub Repo stars](https://img.shields.io/github/stars/tonyhollaar/fiscal_calendar?style=social)

  <img src="https://raw.githubusercontent.com/tonyhollaar/fiscal_calendar/master/img/fiscal_calendar_logo.svg"><br>
  <img src="https://github.com/tonyhollaar/fiscal_calendar/blob/master/img/img_fiscal_calendar.jpg?raw=true" width="70%" height="70%"><br>

# Table of Contents

[Getting Started](#getting-started)<br>
[Description](#description)<br>
[Tutorial](#tutorial)<br>
[Installation](#installation)<br>
[Usage](#usage)<br>
[Key Features](#key-features)<br>
[Reference Materials](#reference-materials)<br>
[License](#license)<br>
[Acknowledgments](#acknowledgments)<br>
[Examples](#examples)<br>
[Data Dictionary](#data-dictionary)<br>

</div>

## Getting Started
Welcome to Fiscal Retail Calendar! This section will guide you through the basic steps to get started with the package.

![promo](https://raw.githubusercontent.com/tonyhollaar/fiscal_calendar/master/img/fiscal_calendar_promo.gif)

## Description
The Fiscal Retail Calendar is structured based on the 4-5-4 week schema and the 4-5-5 week schema, 
accommodating a 53rd week every 5 or 6 years, contingent on leap years (i.e., an additional day). 
In this fiscal calendar, we assume 364 days in a standard year or 371 days in a leap year with a 53rd week.

- With a 53rd week (e.g., 4-5-5 calendar if applicable), 
exemplified in years such as 2006, 2012, 2017, 2023 (totaling 371 days), the code also considers leap years. 
The 53rd week adjusts for the fact that each fiscal year comprises 364 days versus the standard ~365 days. 
Consequently, the fiscal start date for each subsequent year begins either -1 day earlier or -2 days earlier in the case of a leap year. 
To rectify this, an additional week (+7 days) is added if the fiscal year-end date is before January 28th, which is >-4 days from 01-31-year. Conn's fiscal year concludes on the last Saturday of the fiscal month, and the new fiscal start date commences on Sunday.

- Fiscal calendar below can be set with dynamic start-date and end-date.
Currently successfully tested with start-date assumption of 364 days in first year up to dynamic end-date.

## Tutorial
<a target="_blank" href="https://colab.research.google.com/github/tonyhollaar/fiscal_calendar/blob/master/notebooks/fiscal_calendar_tutorial.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Learn how to use Fiscal Retail Calendar in Google Colab with our tutorial notebook:

- **[Fiscal Retail Calendar Tutorial](notebooks/fiscal_calendar_tutorial.ipynb)**: This notebook provides step-by-step instructions on getting started with the Fiscal Retail Calendar package in Google Colab.

## Installation

You can install the package using pip:

```bash
pip install fiscal_calendar
```

## Usage
```python
from fiscal_calendar import FiscalCalendarGenerator

# Example: Create a fiscal calendar generator object for the fiscal year 2021 up to fiscal year 2024
fc = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

# Generate the fiscal calendar DataFrame
df = fc.create_dataframe()

# Save the DataFrame to a CSV file
df.to_csv('fiscal_calendar.csv', index=False)

# Pretty print the table of the fiscal calendar for user defined year (e.g. 2024)
fc.pretty_print_year(df_date=df, year=2024)

# Print the fiscal calendar as a grid for user defined year (e.g. 2024)
fiscal_calendar = fc.print_fiscal_calendar(df, columns=3, week_number=True, year=2024)
print(fiscal_calendar)

# Save the fiscal calendar for a user defined year (e.g. 2024) to a PDF file
fc.save_fiscal_calendar_to_pdf(df, columns=3, week_number=True, year=2024, filename="fiscal_calendar_2024.pdf")

```

## Key Features

- Dynamic Start and End Dates
- Dataframe Output for easy integration
- Leap Year Handling

## Reference Materials:
- [Wikipedia 4–4–5 calendar](https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar)
- [National Retail Federation (NFR)](https://nrf.com/resources/4-5-4-calendar)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The 4-5-4 calendar concept was derived in the 1930s during an informal inter-industry discussion. It has since become widely followed by retailers for sales reporting purposes.
Feel free to contribute, report issues, or suggest improvements!

## Examples
### 1. Output of method: .pretty_print_year()
```python
+------+----------------+------------+------------------------+------------------+--------------------+--------------------+---------------------+-----------------------+------------------------+----------------------+------------------------+----------------------+----------------------+----------------------+------------------------+-------------------------+-------------------+-------------------------+-------------------------+-----------------------+------------------------------+-----------------------------+------------------------+----------------------------+--------------------------+-----------------------+--------------------+-------------+---------------------+------------------------+----------------------+-----------------------------+----------------------------+------------------------+-------------------------+--------------------------+-----------------------+--------------------------------+----------------------------------------+------------------------------------------+------------------------+---------------------------------------+--------------------------------------+--------------------+
|      | time_day_id_pk |  day_date  | day_of_week_short_name | day_of_week_name | day_of_week_letter | fiscal_day_of_week | fiscal_week_of_year | fiscal_week_of_season | fiscal_week_of_quarter | fiscal_week_of_month | fiscal_week_start_date | fiscal_week_end_date | fiscal_week_iso_code | fiscal_month_of_year | fiscal_month_of_season | fiscal_month_of_quarter | fiscal_month_name | fiscal_month_short_name | fiscal_month_start_date | fiscal_month_end_date | fiscal_month_number_of_weeks | fiscal_month_number_of_days | fiscal_quarter_of_year | fiscal_quarter_of_year_str | fiscal_quarter_of_season | fiscal_season_of_year | fiscal_season_name | fiscal_year | fiscal_year_2_digit | fiscal_year_start_date | fiscal_year_end_date | fiscal_year_number_of_weeks | fiscal_year_number_of_days | last_year_equiv_day_fk | last_year_equiv_week_fk | last_year_equiv_day_date | last_year_fiscal_year | last_year_fiscal_month_of_year | prior_year_from_last_year_equiv_day_fk | prior_year_from_last_year_equiv_day_date | time_fiscal_week_id_fk | first_fiscal_week_of_fiscal_month_ind | last_fiscal_week_of_fiscal_month_ind | time_day_id_pk_int |
+------+----------------+------------+------------------------+------------------+--------------------+--------------------+---------------------+-----------------------+------------------------+----------------------+------------------------+----------------------+----------------------+----------------------+------------------------+-------------------------+-------------------+-------------------------+-------------------------+-----------------------+------------------------------+-----------------------------+------------------------+----------------------------+--------------------------+-----------------------+--------------------+-------------+---------------------+------------------------+----------------------+-----------------------------+----------------------------+------------------------+-------------------------+--------------------------+-----------------------+--------------------------------+----------------------------------------+------------------------------------------+------------------------+---------------------------------------+--------------------------------------+--------------------+
| 1099 |    20240204    | 02/04/2024 |          SUN           |      SUNDAY      |         U          |         1          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230205        |         2023W02         |        02/05/2023        |         2023          |               1                |                20220206                |                02/06/2022                |        2024W01         |                   1                   |                  0                   |      20240204      |
| 1100 |    20240205    | 02/05/2024 |          MON           |      MONDAY      |         M          |         2          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230206        |         2023W02         |        02/06/2023        |         2023          |               1                |                20220207                |                02/07/2022                |        2024W01         |                   1                   |                  0                   |      20240205      |
| 1101 |    20240206    | 02/06/2024 |          TUE           |     TUESDAY      |         T          |         3          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230207        |         2023W02         |        02/07/2023        |         2023          |               1                |                20220208                |                02/08/2022                |        2024W01         |                   1                   |                  0                   |      20240206      |
| 1102 |    20240207    | 02/07/2024 |          WED           |    WEDNESDAY     |         W          |         4          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230208        |         2023W02         |        02/08/2023        |         2023          |               1                |                20220209                |                02/09/2022                |        2024W01         |                   1                   |                  0                   |      20240207      |
| 1103 |    20240208    | 02/08/2024 |          THU           |     THURSDAY     |         H          |         5          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230209        |         2023W02         |        02/09/2023        |         2023          |               1                |                20220210                |                02/10/2022                |        2024W01         |                   1                   |                  0                   |      20240208      |
| 1104 |    20240209    | 02/09/2024 |          FRI           |      FRIDAY      |         F          |         6          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230210        |         2023W02         |        02/10/2023        |         2023          |               1                |                20220211                |                02/11/2022                |        2024W01         |                   1                   |                  0                   |      20240209      |
| 1105 |    20240210    | 02/10/2024 |          SAT           |     SATURDAY     |         S          |         7          |          1          |           1           |           1            |          1           |       02/04/2024       |      02/10/2024      |       2024W01        |          1           |           1            |            1            |     February      |           Feb           |       01/31/2021        |      02/27/2021       |              4               |             28              |           1            |             Q1             |            1             |           1           |       SPRING       |    2024     |         24          |       02/04/2024       |      02/01/2025      |             52              |            364             |        20230211        |         2023W02         |        02/11/2023        |         2023          |               1                |                20220212                |                02/12/2022                |        2024W01         |                   1                   |                  0                   |      20240210      |
continues...
```

### 2. Output of method: .print_fiscal_calendar()
```python
February FY2024                March FY2024                   April FY2024                
W | Su Mo Tu We Th Fr Sa       W | Su Mo Tu We Th Fr Sa       W  | Su Mo Tu We Th Fr Sa   
1 |  4  5  6  7  8  9 10       5 |  3  4  5  6  7  8  9       10 |  7  8  9 10 11 12 13   
2 | 11 12 13 14 15 16 17       6 | 10 11 12 13 14 15 16       11 | 14 15 16 17 18 19 20   
3 | 18 19 20 21 22 23 24       7 | 17 18 19 20 21 22 23       12 | 21 22 23 24 25 26 27   
4 | 25 26 27 28 29  1  2       8 | 24 25 26 27 28 29 30       13 | 28 29 30  1  2  3  4   
                               9 | 31  1  2  3  4  5  6                                   
                                                                                          

May FY2024                     June FY2024                    July FY2024                 
W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa   
14 |  5  6  7  8  9 10 11      18 |  2  3  4  5  6  7  8      23 |  7  8  9 10 11 12 13   
15 | 12 13 14 15 16 17 18      19 |  9 10 11 12 13 14 15      24 | 14 15 16 17 18 19 20   
16 | 19 20 21 22 23 24 25      20 | 16 17 18 19 20 21 22      25 | 21 22 23 24 25 26 27   
17 | 26 27 28 29 30 31  1      21 | 23 24 25 26 27 28 29      26 | 28 29 30 31  1  2  3   
                               22 | 30  1  2  3  4  5  6                                  
                                                                                          

August FY2024                  September FY2024               October FY2024              
W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa   
27 |  4  5  6  7  8  9 10      31 |  1  2  3  4  5  6  7      36 |  6  7  8  9 10 11 12   
28 | 11 12 13 14 15 16 17      32 |  8  9 10 11 12 13 14      37 | 13 14 15 16 17 18 19   
29 | 18 19 20 21 22 23 24      33 | 15 16 17 18 19 20 21      38 | 20 21 22 23 24 25 26   
30 | 25 26 27 28 29 30 31      34 | 22 23 24 25 26 27 28      39 | 27 28 29 30 31  1  2   
                               35 | 29 30  1  2  3  4  5                                  
                                                                                          

November FY2024                December FY2024                January FY2024              
W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa      W  | Su Mo Tu We Th Fr Sa   
40 |  3  4  5  6  7  8  9      44 |  1  2  3  4  5  6  7      49 |  5  6  7  8  9 10 11   
41 | 10 11 12 13 14 15 16      45 |  8  9 10 11 12 13 14      50 | 12 13 14 15 16 17 18   
42 | 17 18 19 20 21 22 23      46 | 15 16 17 18 19 20 21      51 | 19 20 21 22 23 24 25   
43 | 24 25 26 27 28 29 30      47 | 22 23 24 25 26 27 28      52 | 26 27 28 29 30 31  1   
                               48 | 29 30 31  1  2  3  4                                  
```                                                                                          

### 3. Output of method: .save_fiscal_calendar_to_pdf()
![Example Output](https://github.com/tonyhollaar/fiscal_calendar/blob/master/img/example_fiscal_calendar_pdf.png?raw=true)

## Data Dictionary
Here is a data dictionary describing the columns in the generated fiscal calendar DataFrame.

| #  | Name                                      | Definition                                                                                                                                                                                              | Possible Values                                                                                                   |
|----|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 1  | time_day_id_pk                            | Primary key of date in format yyyymmdd, e.g., 20220130                                                                                                                                                  | <yyyymmdd>                                                                                                        |
| 2  | day_date                                  | Date in format m/d/yyyy, e.g., 1/30/2022                                                                                                                                                                | <m/d/yyyy>                                                                                                        |
| 3  | day_of_week_short_name                    | 3-letter weekday capitalized, e.g., SUN for Sunday                                                                                                                                                      | <SUN, MON, TUE, WED, THU, FRI, SAT>                                                                               |
| 4  | day_of_week_name                          | Day of the week name capitalized, e.g., SUNDAY                                                                                                                                                          | <SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY>                                                  |
| 5  | day_of_week_letter                        | Unique day of the week letter, e.g., U for Sunday, S for Saturday, H for Thursday etc.                                                                                                                  | <U, M, T, W, H, F, S> *Sunday = U, Monday = M, Tuesday = T, Wednesday = W, Thursday = H, Friday = F, Saturday = S |
| 6  | fiscal_day_of_week                        | Fiscal day of the week with Sunday equal to 1 up to Saturday equal to 7                                                                                                                                 | <1, 2, 3, 4, 5, 6, 7 > *Sunday=1, Monday=2, Tuesday=3, Wednesday=4, Thursday=5, Friday=6, Saturday=7              |
| 7  | fiscal_week_of_year                       | Fiscal week of the fiscal year number with either every week in the year numbered 1 through 52 or 1 through 53 (if 53rd week in the year)                                                               | <1, 2, 3…52, 53>                                                                                                  |
| 8  | fiscal_week_of_season                     | Fiscal week of the season with every year divided into two seasons. Each week of the season is numbered 1 through 26 weeks or 1 through 27 weeks (if 53rd week in the year)                             | <1, 2, 3…26, 27>                                                                                                  |
| 9  | fiscal_week_of_quarter                    | Fiscal week of the fiscal quarter with every year divided into four quarters. Each week of the quarter is numbered 1 through 13 weeks or 1 through 14 weeks (if 53rd week in the year)                  | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14>                                                                   |
| 10 | fiscal_week_of_month                      | Fiscal week of the fiscal month with every month having either 4 weeks or 5 weeks based on the 4-5-4 schema and 4-5-5 schema if 53rd week                                                               | <4, 5>                                                                                                            |
| 11 | fiscal_week_start_date                    | Fiscal week start date of every fiscal week in format m/d/yyyy, e.g., 1/29/2023                                                                                                                         | <m/d/yyyy>                                                                                                        |
| 12 | fiscal_week_end_date                      | Fiscal week end date of every fiscal week, e.g., 2/4/2023                                                                                                                                               | <m/d/yyyy>                                                                                                        |
| 13 | fiscal_week_iso_code                      | Fiscal week ISO code of every fiscal week, e.g., 2005W01                                                                                                                                                | <yyyy><'W'><ww>                                                                                                   |
| 14 | fiscal_month_of_year                      | Fiscal month of the fiscal year with each month numbered 1 through 12 for every fiscal year                                                                                                             | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>                                                                           |
| 15 | fiscal_month_of_season                    | Fiscal month of the fiscal season. Each year has two seasons with 6 months each, numbered 1 through 6                                                                                                   | <1, 2, 3, 4, 5, 6>                                                                                                |
| 16 | fiscal_month_of_quarter                   | Fiscal month of the fiscal quarter. Each fiscal quarter has 3 months, and fiscal month numbered 1 through 3                                                                                             | <1, 2, 3>                                                                                                         |
| 17 | fiscal_month_name                         | Fiscal month name with the first letter capitalized of each of the 12 fiscal months names, e.g., February                                                                                               | <January, February, March, April, May, June, July, August, September, October, November, December>                |
| 18 | fiscal_month_short_name                   | Fiscal month short name of the first 3 letters of the month name and the first letter capitalized for the 12 fiscal months in the year, e.g., Feb                                                       | <Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep>                                                                     |
| 19 | fiscal_month_start_date                   | Fiscal month start date - return for fiscal_month_of_year its respective fiscal month start date in format 1/29/2023                                                                                    | <m/d/yyyy>                                                                                                        |
| 20 | fiscal_month_end_date                     | Fiscal month end date - return for fiscal_month_of_year its respective fiscal month end date in format 2/25/2023                                                                                        | <m/d/yyyy>                                                                                                        |
| 21 | fiscal_month_number_of_weeks              | Fiscal month number of weeks - either 4 or 5 weeks in a fiscal month based on the 4-5-4 week or 4-5-5 weeks schema if 53rd week                                                                         | <4, 5>                                                                                                            |
| 22 | fiscal_month_number_of_days               | Fiscal month number of days - either 28 days or 35 days in a fiscal month                                                                                                                               | <28, 35>                                                                                                          |
| 23 | fiscal_quarter_of_year                    | Fiscal quarter of the fiscal year in format <fiscal quarter number> e.g., with every quarter being labelled as 1, 2, 3, 4                                                                               | <1, 2, 3, 4>                                                                                                      |
| 24 | fiscal_quarter_of_year_str                | Fiscal quarter of the fiscal year as a string, e.g., 'Q1'                                                                                                                                               | <Q1, Q2, Q3, Q4>                                                                                                  |
| 25 | fiscal_quarter_of_season                  | Fiscal quarter of the fiscal season - equal to 1 IF 1st OR 3rd fiscal quarter of the year ELSE equal to 2 IF 2nd OR 4th fiscal quarter of the year                                                      | <1, 2>                                                                                                            |
| 26 | fiscal_season_of_year                     | Fiscal season of the year - equal to 1 IF 1st or 2nd fiscal quarter of the year ELSE equal to 2 IF 3rd or 4th fiscal quarter of the year                                                                | <1, 2>                                                                                                            |
| 27 | fiscal_season_name                        | Fiscal season name - equal to SPRING IF fiscal_season_of_year = 1 ELSE equal to FALL if fiscal_season_of_year = 2                                                                                       | <SPRING, FALL>                                                                                                    |
| 28 | fiscal_year                               | Fiscal year - running from fiscal start date to fiscal end date for each year starting on the last Sunday (unless 53rd week +7days) of the month January up to the last Saturday of January, e.g., 2022 | <yyyy>                                                                                                            |
| 29 | fiscal_year_2_digit                       | Fiscal year 2 digits - last 2 out of 4 characters of fiscal year in yyyy format, e.g., fiscal year: 2022 becomes fiscal_year_2_digit: 22                                                                | <yy>                                                                                                              |
| 30 | fiscal_year_start_date                    | Fiscal year start date - return for fiscal_year its respective fiscal year start date in format 1/30/2022                                                                                               | <m/d/yyyy>                                                                                                        |
| 31 | fiscal_year_end_date                      | Fiscal year end date - return for fiscal_year its respective fiscal year end date in format 1/28/2023                                                                                                   | <m/d/yyyy>                                                                                                        |
| 32 | fiscal_year_number_of_weeks               | Fiscal year number of weeks - either 52 or 53 weeks in a fiscal year based on whether there is a 53rd week in the year                                                                                  | <52, 53>                                                                                                          |
| 33 | fiscal_year_number_of_days                | Fiscal year number of days - either 364 days or 371 days in a fiscal year                                                                                                                               | <364, 371>                                                                                                        |
| 34 | last_year_equiv_day_fk                    | Last year equivalent day foreign key - day_date date minus 364 days to retrieve the date from last year for comparison purposes, e.g., 20220130                                                         | <yyyymmdd>                                                                                                        |
| 35 | last_year_equiv_week_fk                   | Last year equivalent fiscal week foreign key - lookup for the last year equivalent date (current day_date-364 days) and return the respective fiscal week, e.g., 2022W01                                | <yyyy><'W'><ww>                                                                                                   |
| 36 | last_year_equiv_day_date                  | Last year equivalent day date - return for the last_year_equiv_day_fk its respective date in format 1/30/2022                                                                                           | <m/d/yyyy>                                                                                                        |
| 37 | last_year_fiscal_year                     | Last year fiscal year - return for the last_year_equiv_day_fk its respective fiscal year in format 2022                                                                                                 | <yyyy>                                                                                                            |
| 38 | last_year_fiscal_month_of_year            | Last year fiscal month of the fiscal year - return for the last_year_equiv_day_fk its respective fiscal month of the year in format 1-12                                                                | <1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>                                                                           |
| 39 | prior_year_from_last_year_equiv_day_fk    | Prior year from the last year equivalent day foreign key - day_date date minus 730 days to retrieve the date from two years ago for comparison purposes, e.g., 20200130                                 | <yyyymmdd>                                                                                                        |
| 40 | prior_year_from_last_year_equiv_day_date  | Prior year from the last year equivalent day date - return for the prior_year_from_last_year_equiv_day_fk its respective date in format 1/30/2020                                                       | <m/d/yyyy>                                                                                                        |
| 41 | time_fiscal_week_id_fk                    | Fiscal week ID foreign key - fiscal week ISO code of every fiscal week, e.g., 2005W01.  note:                                                                                                           | <yyyy><'W'><ww>                                                                                                   |
| 42 | first_fiscal_week_of_fiscal_month_ind     | First fiscal week of the fiscal month indicator - equal to 1 IF fiscal_week_of_month = 1 ELSE equal to 0                                                                                                | <0, 1>                                                                                                            |
| 43 | last_fiscal_week_of_fiscal_month_ind      | Last fiscal week of the fiscal month indicator - equal to 1 IF fiscal_week_of_month = fiscal_month_number_of_weeks ELSE equal to 0                                                                      | <0, 1>                                                                                                            |
| 44 | time_day_id_pk_int                        | Integer representation of time_day_id_pk, e.g., 20220130 is represented as 20220130                                                                                                                     | <integer value>                                                                                                   |
