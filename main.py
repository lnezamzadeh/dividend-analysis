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


def percentage_positive(d):
    count = sum(1 for v in d.values() if v is not None and v > 0)
    return 100.0 * count / len(d)


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

    # Now process the data

    # We will create 2 dictionaries where the key is the ticker and the value is the 10th year DPS
    eight_straight = {}
    nine_straight = {}

    for ticker, dps_list in dps_dict.items():
        counter = 0
        for index, dps in enumerate(dps_list):
            if dps is not None and dps > 0:
                counter += 1
            else:
                counter = 0

            if counter == 8 and index + 2 < len(dps_list):
                # If we found 8 straight and there is a tenth month in the data...
                eight_straight[ticker] = dps_list[index + 2]

            if counter == 9 and index + 1 < len(dps_list):
                # if we found 9 straight and there is a tenth month in the data...
                nine_straight[ticker] = dps_list[index + 1]
                break  # Only record the first streak we find, not possible in 15 years to get 2

    print("Amount of Tickers with 8 straight profitable quarters:", len(eight_straight))
    print("Amount of Tickers with 9 straight profitable quarters:", len(nine_straight))

    print(eight_straight["AAPL"])

    # Now with these two lists calculate what percentage of them have a positive value
    eight_percent = percentage_positive(eight_straight)
    nine_percent = percentage_positive(nine_straight)

    print(f"Percentage of 8-straight tickers with positive DPS after streak: {eight_percent:.2f}%")
    print(f"Percentage of 9-straight tickers with positive DPS after streak: {nine_percent:.2f}%")
