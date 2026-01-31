import FinanceDataReader as fdr

df = fdr.StockListing('KRX')
row = df[df['Code'] == '005380']

if not row.empty :
    print(row.iloc[0]['Name'])