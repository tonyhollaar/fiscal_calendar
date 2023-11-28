from fiscal_calendar import FiscalCalendarGenerator

# Create a fiscal calendar generator object
fiscal_calendar_generator = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

# Generate the fiscal calendar
df_fiscal_calendar = fiscal_calendar_generator.create_dataframe()

# Pretty print the fiscal calendar for the year 2022
fiscal_calendar_generator.pretty_print_year(df_date=df_fiscal_calendar, year=2024)

# Print the fiscal calendar for the year 2022
fiscal_calendar_generator.print_fiscal_calendar(df_fiscal_calendar, columns=6, week_number=False, year=2022)
