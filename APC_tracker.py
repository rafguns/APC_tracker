#
# Script compares contents of two Excel files
#
# May 18, 2023
# Eric Schares

# Flow:
# Go to https://www.elsevier.com/about/policies/pricing and download the article-publishing-charge.xlsx file
# Read in yesterday's APC price list
# For each ISSN, look up the price in today's file
# Report any changes, including title, delta, old, and new price
# Report any ISSNs in yesterday's file that are no longer in today's (removed)
# 
# Read in today's APC price list
# Already did the deltas, so don't need to do that again
# Report any ISSNs in today's file that are not in yesterday's (new titles added)
# Those new titles will start getting tracked when this file turns into yesterday's
#
#

import pandas as pd
import requests


def scrape_apc_list():
    url = 'https://www.elsevier.com/books-and-journals/journal-pricing/apc-pricelist'
    filename = 'article-publishing-charge.xlsx'

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print("Failed to download the file.")


############ Main ################

if __name__ == "__main__":
    # Download Elsevier's article-publishing-charge.xlsx file
    scrape_apc_list()

    # Skip extra bits at the bottom and save file to CSV for comparison 
    df = pd.read_excel(
        'article-publishing-charge.xlsx',
        header=3,
        usecols=[0,1,2,3],
        names=['ISSN', 'Title', 'Business Model', 'USD']
    )
    df = df.dropna(subset="Title")
    df.to_csv("article-publishing-charge.csv", index=False)