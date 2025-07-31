import pandas as pd
import numpy as np

df = pd.read_csv('ebay_prices.csv')

results = []

upc_place                     = 0
asin_place                    = 1
amazon_place                  = 2
walmart_place                 = 3
my_list_price_amz_wal_upc_pos = 4
ebay_price_start_place        = 5   # first eBay-price column

for _, row in df.iterrows():
    upc   = row[upc_place]
    asin  = row[asin_place]
    amz_p = row[amazon_place]
    wal_p = row[walmart_place]
    my_lp = row[my_list_price_amz_wal_upc_pos]

    # --------------------------------------------
    # ❶ Keep the very first eBay value for display
    # --------------------------------------------
    price_slice     = row[ebay_price_start_place : ebay_price_start_place + 5]  # 5 values → cols 5-9
    ebay_prices_raw = pd.to_numeric(price_slice, errors='coerce').dropna()

    ebay_prices      = ebay_prices_raw.tolist()          # values used in stats
    first_ebay_price = ebay_prices[0] if len(ebay_prices) else np.nan
    last_ebay_price  = ebay_prices[-1] if len(ebay_prices) else np.nan

    if len(ebay_prices) >= 2:            # need ≥2 for stdev(ddof=1)
        prices          = np.array(ebay_prices, dtype=float)
        mean_price      = prices.mean()
        stdev_price     = prices.std(ddof=1)
        cv              = stdev_price / mean_price * 100
        q1, q3          = np.percentile(prices, [25, 75])
        iqr             = q3 - q1
        median_price    = np.median(prices)
        mad             = np.median(np.abs(prices - median_price))
        range_to_mean   = (prices.max() - prices.min()) / mean_price * 100

        cv_conf         = 'Confident' if cv <= 10 else 'Cautious' if cv <= 20 else 'Review'
        iqr_conf        = 'Confident' if (iqr / mean_price) * 100 <= 10 else \
                          'Cautious'  if (iqr / mean_price) * 100 <= 20 else 'Review'
        mad_conf        = 'Confident' if (mad / median_price) * 100 <= 10 else \
                          'Cautious'  if (mad / median_price) * 100 <= 20 else 'Review'
        range_conf      = 'Confident' if range_to_mean <= 10 else \
                          'Cautious'  if range_to_mean <= 20 else 'Review'
    else:
        # Fallback when <2 values remain
        mean_price = stdev_price = cv = iqr = mad = range_to_mean = np.nan
        cv_conf = iqr_conf = mad_conf = range_conf = 'Review, not enough listings'

    results.append({
        'UPC'                     : upc,
        'ASIN'                    : asin,
        'Amazon_Price'            : amz_p,
        'Walmart_Price'           : wal_p,
        'My_List_Price_UPC/Amz/Wal': my_lp,
        'Lowest_Ebay_Price'       : first_ebay_price,
        'Highest_Ebay_Price'      : last_ebay_price,
        'Mean_eBay_Price'         : mean_price,
        'Std_Dev'                 : stdev_price,
        'Coeff_of_Variation_%'    : cv,
        'CV_Confidence'           : cv_conf,
        'IQR'                     : iqr,
        'IQR_Confidence'          : iqr_conf,
        'Median_Abs_Deviation'    : mad,
        'MAD_Confidence'          : mad_conf,
        'Range_to_Mean_%'         : range_to_mean,
        'Range_Confidence'        : range_conf,
        'eBay_Prices_Used'        : ebay_prices          # list without the first value
    })

results_df = pd.DataFrame(results)
results_df.to_csv('pricing_analysis_first_five.csv', index=False)

print('Pricing analysis complete. Results saved to pricing_analysis.csv')
