import tushare as ts
# # trade_cal = ts.trade_cal()
# # trade_cal.to_csv("trade_cal",index=False)
df=ts.get_h_data("601318","1991-03-01","2017-08-01")
df.to_csv("601318.csv")