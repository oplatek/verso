# print markdown table with current next three dates and days of the week
from datetime import datetime, timedelta

# Get today's date
today = datetime.now()
# Get the next three dates
next_dates = [today + timedelta(days=i) for i in range(1, 4)]
# Print the markdown table header
print("| Date       | Day of the Week |")
print("|------------|-----------------|")
# Print the markdown table rows
for date in next_dates:
    # Format the date and day of the week
    date_str = date.strftime("%Y-%m-%d")
    day_of_week = date.strftime("%A")
    # Print the row
    print(f"| {date_str} | {day_of_week} |")
# Print the markdown table footer
print("|------------|-----------------|")
# Output:
# | Date       | Day of the Week |
# |------------|-----------------|
# | 2023-10-01 | Sunday          |
# | 2023-10-02 | Monday          |
# | 2023-10-03 | Tuesday         |
# |------------|-----------------|
