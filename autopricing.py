import pandas as pd
import numpy as np

df = pd.read_csv('ebay_prices.csv')

results = []

upc_place = 0
asin_place = 1
amazon_place = 2
walmart_place = 3
ebay_price_start_place = 4

for index, row in df.iterrows():
    upc = row[upc_place]
    asin = row[asin_place]
    walmart_price = row[walmart_place]
    amazon_price = row[amazon_place]

    ebay_prices = pd.to_numeric(row[ebay_price_start_place:], errors='coerce').dropna().tolist()
    lowest_ebay_price = row[ebay_price_start_place]
    highest_ebay_price = row[len(row)-1] 

    if len(ebay_prices) >= 2:
        prices = np.array(ebay_prices)
        mean_price = np.mean(prices)
        stdev_price = np.std(prices, ddof=1)
        cv = (stdev_price / mean_price) * 100
        q1, q3 = np.percentile(prices, [25, 75])
        iqr = q3 - q1
        median_price = np.median(prices)
        mad = np.median(np.abs(prices - median_price))
        range_to_mean_ratio = ((np.max(prices) - np.min(prices)) / mean_price) * 100

        cv_confidence = 'Confident' if cv <= 10 else 'Cautious' if cv <= 20 else 'Review'
        iqr_confidence = 'Confident' if (iqr / mean_price) * 100 <= 10 else 'Cautious' if (iqr / mean_price) * 100 <= 20 else 'Review'
        mad_confidence = 'Confident' if (mad / median_price) * 100 <= 10 else 'Cautious' if (mad / median_price) * 100 <= 20 else 'Review'
        range_confidence = 'Confident' if range_to_mean_ratio <= 10 else 'Cautious' if range_to_mean_ratio <= 20 else 'Review'
    else:
        mean_price = stdev_price = cv = iqr = mad = range_to_mean_ratio = np.nan
        cv_confidence = iqr_confidence = mad_confidence = range_confidence = 'Review'

    results.append({
        'UPC': upc,
        'ASIN': asin,
        'Amazon_Price': amazon_price,
        'Walmart_Price': walmart_price,
        'Mean_eBay_Price': mean_price,
        'Std_Dev': stdev_price,
        'Coeff_of_Variation_%': cv,
        'CV_Confidence': cv_confidence,
        'IQR': iqr,
        'IQR_Confidence': iqr_confidence,
        'Median_Abs_Deviation': mad,
        'MAD_Confidence': mad_confidence,
        'Range_to_Mean_%': range_to_mean_ratio,
        'Range_Confidence': range_confidence,
        'eBay_Prices': ebay_prices
    })

results_df = pd.DataFrame(results)
results_df.to_csv('pricing_analysis.csv', index=False)

print('Pricing analysis complete. Results saved to pricing_analysis.csv')
