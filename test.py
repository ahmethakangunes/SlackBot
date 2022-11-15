import pandas as pd

gsheetid = "1stsF9NlDYDeBKyJ1Vchmpr__sSllot0bu2NUAWuXavM"
sheet_name = ""
gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
df = pd.read_csv(gsheet_url)
print(df)