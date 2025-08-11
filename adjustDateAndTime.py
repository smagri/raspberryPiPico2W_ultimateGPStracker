def is_leap_year(year):
    # Leap year rule: divisible by 4, but centuries must be divisible by 400
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def adjust_gps_datetime(utcDate, utcTime, utcCorrect):
    """
    Convert GPS UTC date/time to local date/time by applying a UTC offset.
    Handles leap years and day/month/year rollovers.

    utcDate: 'ddmmyy'
    utcTime: 'hhmmss.sss'
    utcCorrect: integer or float hours offset from UTC (e.g., +10, -5, +5.5)
    """

    # --- 1. Parse NMEA date/time strings into integers ---
    year = 2000 + int(utcDate[4:])    # Convert 'yy' to '20yy'
    month = int(utcDate[2:4])         # Month as int
    day = int(utcDate[0:2])           # Day as int
    hour = int(utcTime[0:2])          # Hour in UTC
    minute = int(utcTime[2:4])        # Minutes
    second = int(utcTime[4:6])        # Seconds

    # --- 2. Apply UTC offset to hours ---
    # (can be positive or negative; fractions like +5.5 work too)
    hour += utcCorrect

    # --- 3. Days in each month (adjust February for leap year) ---
    month_days = [31, 28 + is_leap_year(year), 31, 30, 31, 30,
                  31, 31, 30, 31, 30, 31]

    # --- 4. Adjust forward in time if hour >= 24 ---
    while hour >= 24:
        hour -= 24
        day += 1
        # If day goes past the end of the month → move to next month
        if day > month_days[month - 1]:
            day = 1
            month += 1
            # If month goes past December → move to January of next year
            if month > 12:
                month = 1
                year += 1
            # Update February days for new year
            month_days[1] = 28 + is_leap_year(year)

    # --- 5. Adjust backward in time if hour < 0 ---
    while hour < 0:
        hour += 24
        day -= 1
        # If day goes before the start of the month → move to previous month
        if day < 1:
            month -= 1
            # If month goes before January → move to December of previous year
            if month < 1:
                month = 12
                year -= 1
            # Update February days for new year
            month_days[1] = 28 + is_leap_year(year)
            # Set day to last day of the new month
            day = month_days[month - 1]

    # --- 6. Format date/time strings with leading zeros ---
    myTime = f"{hour:02d}:{minute:02d}:{second:02d}"
    myDate = f"{month:02d}/{day:02d}/{year}"

    return myDate, myTime

