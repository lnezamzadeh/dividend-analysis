def read_csv_to_dict(file_path):
    import csv

    result = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the header row
        for row in reader:
            key = row[0]
            values = {headers[i]: row[i] for i in range(1, len(headers))}
            result[key] = values
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    # This dictionary contains all the data in the CSV. Not necessary for this question but might be useful.
    data_dict = read_csv_to_dict(csv_file_path)

    # Now I want to add a function that reduces that dictionary to the useful information.
    # I want to make a new dictionary that only contains the stock ticker as a key, and the all the DPS values as a list with the 0th value being the value of dps 10 and the last being DPS 25

    dps_dict = {}
    for ticker, values in data_dict.items():
        dps_list = []
        for i in range(10, 26):  # From 10 to 25
            dps_key = f"DPS {i}"  # Calculate the DPS string that would go in the index...
            val = values.get(dps_key, None)  # Get the value or None
            if val == "#N/A" or val == "":  # If the value is #N/A or empty then just put none
                val = None
            else:
                try:
                    val = float(val)  # If the value is not convertable to a float then just put none
                except (TypeError, ValueError):
                    val = None
            dps_list.append(val)  # Add it to the list in order.
        dps_dict[
            ticker] = dps_list  # Once the list is made, then append the list to the dict as a value for the ticker key.

    # print("-----")
    print(dps_dict["AGO"])
    print("Total number of stocks examined:", len(dps_dict)) # Total tickers loaded from the CSV file

    # Now process the data

    # Initialize tracking dictionaries
    eight_year_candidates = {}
    eight_year_successes = {}
    nine_year_candidates = {}
    nine_year_successes = {}

    for ticker, dps_list in dps_dict.items():
        counter = 0 # Tracks how many years in a row the DPS has grown
        for index in range(1, len(dps_list)):
            prev = dps_list[index - 1]
            curr = dps_list[index]

            # If both current and previous DPS are valid and show growth, increase streak
            if prev is not None and curr is not None and curr > prev:
                counter += 1
            else:
                counter = 0 # Reset if no growth or invalid data

            # 8-year streak
            if counter == 8 and index + 2 < len(dps_list): # Need room for year 9 and 10
                year8 = dps_list[index]
                year9 = dps_list[index + 1]
                year10 = dps_list[index + 2]
                eight_year_candidates[ticker] = year10 # Add to total set of 8-year growers

                # If years 9 and 10 both show continued growth, it's a success
                if (
                    year8 is not None and year9 is not None and year10 is not None
                    and year9 > year8 and year10 > year9
                ):
                    eight_year_successes[ticker] = year10 # Count as dividend achiever (10 years)

            # 9-year streak
            if counter == 9 and index + 1 < len(dps_list): # Need room for year 10
                year9 = dps_list[index]
                year10 = dps_list[index + 1]
                nine_year_candidates[ticker] = year10 # Add to total set of 9-year growers

                # If year 10 shows continued growth, it's a success
                if year9 is not None and year10 is not None and year10 > year9:
                    nine_year_successes[ticker] = year10 # # Count as dividend achiever (10 years)
                    break  # Only record the first streak we find, not possible in 15 years to get 2

    # Output counts
    print("Tickers with 8 years of dividend growth:", len(eight_year_candidates))
    print("→ of those, number that grew in year 9 & 10:", len(eight_year_successes))

    print("Tickers with 9 years of dividend growth:", len(nine_year_candidates))
    print("→ of those, number that grew in year 10:", len(nine_year_successes))

    # Calculate probabilities
    if len(eight_year_candidates) > 0:
        eight_prob = 100 * len(eight_year_successes) / len(eight_year_candidates)
    else:
        eight_prob = 0

    if len(nine_year_candidates) > 0:
        nine_prob = 100 * len(nine_year_successes) / len(nine_year_candidates)
    else:
        nine_prob = 0

    print(f"Probability (8-year growers → 10-year achievers): {eight_prob:.2f}%")
    print(f"Probability (9-year growers → 10-year achievers): {nine_prob:.2f}%")
