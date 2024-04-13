import pandas as pd
import pdfplumber
import pathlib
import argparse

def parse_table(page_text, current_df=None, file_name=None):
    begin = False
    heads = None
    my_df = None if current_df is None else current_df.copy()
    
    for s in page_text:
        if not begin and s.startswith('Type B/S Trade Date Settle Date QTY SYM PRICE Principal'):
            a = s.replace('Type', 'Acct-Type')
            # 以下两行用来修正2021-01-04的异常账单。对其他账单应该无影响
            a = a.replace('TranFee', 'Tran-Fee')
            a = a.replace('Number Net AmountTrade#', 'Number Net Amount Trade#')
            a = a.replace('Trade Date', 'Trade-Date')
            a = a.replace('Settle Date', 'Settle-Date')
            a = a.replace('Tran Fee', 'Tran-Fee')
            a = a.replace('Fees', "Add’l-Fees")
            a = a.replace('Number', "Tag-Number")
            a = a.replace('Net Amount', "Net-Amount")
            a = a.replace(' T P', " MKT CAP")
            begin = True
            heads = a.split(' ')
            if my_df is None:
                my_df = pd.DataFrame(columns=heads)
            continue
        if not begin:
            continue
        if s.startswith('2'):
            items = s.split(' ')
            if len(items) != len(heads):
                raise Exception(f"{'无名文件' if file_name is None else file_name}: 数字和表头对不上\n内容:{items}\n表头:{heads}")
            else:
                my_df.loc[my_df.shape[0]] = items
    return my_df

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--file-path', type=str, default = '*.pdf')
args = parser.parse_args()

files = [f for f in pathlib.Path().glob(args.file_path)]
my_df = None

for file in files:
    pdf = pdfplumber.open(file)
    for page in pdf.pages:
        my_df = parse_table(page_text=page.extract_text().split('\n'), current_df=my_df, file_name=file)

copy_df = None if my_df is None else my_df.copy()
if copy_df is not None:
    copy_df['Principal'] = copy_df['Principal'].apply(lambda x: float(x.replace(',', '')))
    copy_df['Net-Amount'] = copy_df['Net-Amount'].apply(lambda x: float(x.replace(',', '')))
    copy_df['Principal'] = pd.to_numeric(copy_df.Principal)
    copy_df['Net-Amount'] = pd.to_numeric(copy_df['Net-Amount'])
    copy_df.to_csv('oprations.csv', encoding='utf-8-sig', index=False)

print(f'done. {args.file_path} 下共处理了{len(files)}个文件, {0 if copy_df is None else copy_df.shape[0]}条记录')
