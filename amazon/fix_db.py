import pandas as pd 
import re

def fix_client_id(input, output):
    df = pd.read_csv(input)
    # size = df.shape[0]
    # for i in range(size):
    #     if df['client_id'][i] == to_match:
    #         df['client_id'][i] = new_id
    df.rename(index=str, columns = {'client_id': 'brand'})
    df.to_csv(output)

def fix_price(input, output):
    df = pd.read_csv(input)
    size = df.shape[0]
    LOrealP = False 

    # If the file is from LOreal
    if re.search("lorealparis", input) != None:
        LOrealP = True

    for i in range(size):
        price = df['price'][i]
        # if LOrealP:
        #     price= re.sub("Γé¼", "", price).group()
        
        if re.search(",", price) != None:
            price = re.sub(",", ".", price)
            
        # # Max 2 decimals after the decimal point. 
        # price = round(float(price),2)
        
        df['price'][i] = price
    df.to_csv(output)

def fix_avgmark(input, output):
    df = pd.read_csv(input)
    size = df.shape[0]
    for i in range(size):
        mark = df['avg_mark'][i]
        if re.search(",", mark) != None:
            mark = re.sub(",", ".", mark)
        df['avg_mark'] = mark
    
    df.to_csv(output)


def useless_review(input, output):
    df = pd.read_csv(input)
    size = df.shape[0]
    useless = [0] * size
    df['useless_review'] = useless
    df.to_csv(output)

def remove_duplicates(input, output):

    df = pd.read_csv(input)

    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=None, inplace=True)

    # Reindex the rows
    df = df.reset_index(drop = True)

    # Write the results to a different file
    df.to_csv(output)


if __name__ == '__main__':
    amazon_path = "~/Documents/KITE/New merged/"
    #fix_price(path + "amazon_product.csv", path + "fixedprice_amazon_product.csv")
    #fix_client_id(path + "fixedprice_amazon_product.csv", path + "fixedbrand_amazon_product.csv")
    #useless_review(path + "amazon_review.csv", path + "fixed_amazon_review.csv")
    #remove_semicolon(path + "fixed_amazon_review.csv", path+"fixedtxt_amazon_review.csv", "review_txt")
    #remove_semicolon(path + "fixedtxt_amazon_review.csv", path + "fixedauthor_amawon_review.csv", "author_id")
    remove_duplicates(amazon_path + "amazon_product.csv", amazon_path + "cleaned_amazon_product.csv")
