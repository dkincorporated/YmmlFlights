# YmmlFlights
Simple Python script that fetches departures or arrivals from Melbourne Airport (MEL, YMML), Australia. 

Maybe use it to build your own flight board!

**Note: It uses the API endpoint used by the airport's website, which is not an officially published API, so it may change or break without notice. It, of course, also means there is no official licence – use with caution.**

## Parameters
The `fetch_flights` function allows a choice of
- direction (departure or arrival)
- minutes in the past to fetch from
- minutes in the future to fetch to
- number of flights to fetch.

## Dependencies
- `prettytable` (to print in table format) – available from `pip`