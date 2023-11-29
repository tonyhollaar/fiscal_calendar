from fiscal_calendar import FiscalCalendarGenerator

# Create a Fiscal Calendar Generator object
fc = FiscalCalendarGenerator(start_date='2021-01-31', end_date='2025-02-01')

# Generate the fiscal calendar DataFrame
df = fc.create_dataframe()

# Save the DataFrame to a CSV file
df.to_csv('fiscal_calendar.csv', index=False)

# Pretty print the fiscal calendar for the year 2022
fc.pretty_print_year(df_date=df, year=2024)

# Print the fiscal calendar for the year 2022
fiscal_calendar = fc.print_fiscal_calendar(df, columns=3, week_number=True, year=2024)
print(fiscal_calendar)

# Save the fiscal calendar for a user defined year to a PDF file
fc.save_fiscal_calendar_to_pdf(df, columns=3, week_number=True, year=2024, filename="fiscal_calendar_2024.pdf")
