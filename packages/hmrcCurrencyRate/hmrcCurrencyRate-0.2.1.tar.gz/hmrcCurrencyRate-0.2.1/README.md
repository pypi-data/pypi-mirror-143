# hmrc_currency_rate module (Other Currency to GBP)

## v0.2.0 is released
1. the month input can be `'1'` or `'01'`

### Description
- This module convert other currencies rate to GBP from the data on HMRC
- The return result is default as pd.DataFrame
```
hmrc_to_dataframe(month, year):

dataframe

```
### How to use
Assume we would like to get the currency rate at Jan/2017
```
from hmrcCurrencyRate import hmrc

hmrc.hmrc_to_dataframe('01', '2017'):

```

![Result](https://imgur.com/oZ2zLR3)
