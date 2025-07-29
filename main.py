import numpy as np
import pandas as pd


def clean_price(x):
    # REMOVES THE UNECCECARY CHARACTERS and Whitespaces with strip
    return int(x.replace('₹', '').replace(',', '').strip())


def clean_ratings(x):
    try:
        return float(x.strip())
    except:
        return None


def clean_num_ratings(x):
    try:
        return int(x.replace(',', '').strip())
    except:
        return None


def main():
    # STEP 1: DATA ANALYSIS
    df = pd.read_csv("Air Conditioners.csv");
    print(df.head())  # shows first 5 rows
    print(df.info())  # shows info
    # STEP 2: CLEANING THE DATA

    # Drop the rows with missing field entry - Inplaces = true ensures updating of the dataset
    df.dropna(subset=['ratings', 'no_of_ratings', 'discount_price', 'actual_price'], inplace=True)
    print("- Removed the rows with the missing fields")

    # Remove ₹ and commas, convert to float/int
    df['discount_price'] = df['discount_price'].apply(clean_price)
    df['actual_price'] = df['actual_price'].apply(clean_price)
    df['ratings'] = df['ratings'].apply(clean_ratings)
    df['no_of_ratings'] = df['no_of_ratings'].apply(clean_num_ratings)

    # Confirm the applied changes
    print("[ CHANGING OF TYPES ]")
    print(df[['ratings', 'no_of_ratings', 'discount_price', 'actual_price']].dtypes)

    # STEP 3: EXTRACT Brand from Product Name
    df['brand'] = df['name'].apply(lambda x: x.split()[0])
    print(df['brand'].value_counts().head(10))

    # STEP 4: Analyze the Data

    # TO SHOW THE LIST OF TOP 10 BRANDS
    top_brand = df['brand'].value_counts().head(10)
    print(top_brand)
    # AVERAGE RATING Per Brand
    avg_rating = df.groupby('brand')['ratings'].mean().sort_values(ascending=False).head(10)
    print(avg_rating)
    # Best Value Products (Price ÷ Rating)
    df['value_score'] = df['discount_price'] / df['ratings']
    best_value = df.sort_values('value_score').head(10)
    print(best_value[['name', 'brand', 'discount_price', 'ratings', 'value_score']])
    df.to_csv("cleaned_ac_data.csv", index=False)


if __name__ == '__main__':
    main()
