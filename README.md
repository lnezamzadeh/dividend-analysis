# How to Run

`python3 src/main.py stocks.csv`

# What this does

- First I needed to convert the excel sheet to CSV in order to parse it into python. This is easy you can just export it as a CSV from excel. 
- Then we read the CSV into a dictionary of dictionaries where the top key is the Ticker
    - This is useful because we have all the data in memory and can manipulate it to answer more than just this question
- Then we need to reduce the data to answer the question. 
    - I decided to make another dictionary where the key is the ticker and the value is a list of DPS values by year. It would look something like this:

    ```
    {"AAPL": [0.0, 0.0, 0.0, 0.1, 0.4, 0.5, 0.5, 0.5, 0.6, 0.7, 0.8, 0.8, 0.9, 0.9, 0.94, 0.98]},{"AGO": [0.0, 0.0, 0.0, 0.4, 0.4, 0.4, 0.5, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.12, 1.24]}....
  
# What main.py does

- Now it is a simple matter of reducing it once again to a the lists we are concerned with: A list of tickers that have 8 years straight and 9 years straight, and their 10th year values. 
    - This is done with yet another loop and we will make 2 more dictionaries
    - The data looks like this:
    ```
    {"AAPL": 0.9}
    ```

- Finally it is just a simple calculation of total number of items in the lists compared to items who have values over 0 and turn it into percentage
- Answers the question "Do stocks with 8 or 9 years of paying any dividend tend to keep doing so in year 10?"

# What main1.py does

- Once I have the data structured this way, I:
  - Loop through each ticker’s list of annual DPS values
  - Look for **8 or 9 consecutive years of dividend growth**
  - If a stock has 8 years of consecutive growth, we check if years 9 and 10 also increased. If yes, it's considered a "success" (a dividend achiever)
  - Similarly, if a stock has 9 years of growth, we check year 10 to see if the streak continued

# Output

The program prints:
- Total number of tickers analyzed
- Number of tickers with 8 consecutive years of dividend growth
- Number of those that grew in years 9 and 10 (i.e., became dividend achievers)
- Probability (percentage) that an 8-year streak continues to 10 years
- Same output for 9-year streaks

# Why this matters

- Dividend Achievers are companies that have consistently increased their dividends for 10+ years: they are often included in dividend ETFs and income portfolios.
    - This analysis helps us see how "reliable" an 8- or 9-year streak is in predicting eventual achiever status.