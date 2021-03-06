import pandas as pd

def merge_csv(csv_list, col_list, newname):
    """Merges csv files in csv_list
       csv_list: list of csv filenames to merge
       col_list: list of columns in the 'right' order
       newname: name of the merged file """

    # Initialize empty dataframe
    merged_df = pd.DataFrame()
    for filename in csv_list:
        print("current file: ", filename)
        to_merge = pd.read_csv(filename, usecols = col_list, encoding = 'latin')

        if(len(to_merge.columns) != len(col_list)):
            print("Error: wrong number of columns for ", filename,". Only", len(to_merge.columns), "columns in this file.\n")
            return -1
        
        # Making sure that the columns are in the right order
        to_merge = to_merge[col_list]

        # Merge the file in the list to merged_df. 
        # Append method is enough because each data we have is unique
        print("Merging " + filename + " to dataframe...\n")
        merged_df = merged_df.append(to_merge)
        #merged_df = merged_df[1:]

    print("Merged!")
    merged_df = merged_df.reset_index(drop = True)

    merged_df.to_csv(newname)
    return 0



if __name__ == "__main__":
    # scraping_path = "~/Documents/KITE/Scraping"
    # marionnaud_path = scraping_path + "/Marionnaud/marionnaud_"
    # folie_path = scraping_path + "/Folie/folie_"    
    # loreal_path = scraping_path + "/L'Oréal Paris/lorealparis_"
    # sephora_path = scraping_path + "/Sephora/sephora_"
    # amazon_path = scraping_path + "/Amazon/amazon_"
  
    # retailer_list = [marionnaud_path, folie_path, loreal_path, sephora_path, amazon_path]

    path = "~/Documents/KITE/New merged/"
    amazon_path = "~/Documents/KITE/amazon/amazon/spiders/"
    
    # Create the list of csv files for each table
    product_list = [path + "product_merged.csv", path + "cleaned_amazon_product.csv"]
    review_list = [path + "review_merged.csv", path + "amazon_review.csv"]
    consumer_list = [path + "consumer_merged.csv", path + "amazon_consumer.csv"]

    # Create the list of attributes in a fixed order
    product_col = ["product_id", "brand", "product_name", "price", "avg_mark", "product_type", "retailer_id"]
    review_col = ["retailer_id", "product_id", "author_id", "mark", "review_date", "review_title", "review_txt", "useful_review", "useless_review"]
    consumer_col = ["author_id", "gender", "eye_color", "hair_color", "skin_concerns", "skintone", "skintype"]

    # Merge
    #merge_csv(product_list, product_col, path + "/product_merged_new.csv")
    merge_csv(review_list, review_col, path + "/review_merged_new.csv")
    merge_csv(consumer_list, consumer_col, path + "/consumer_merged_new.csv")

    # Create directly the retailer table
    # retailer = {"retailer_id" : ["marionnaud_fr", "foliecosmetic_com", "loreal-paris_fr", "amazon_fr", "sephora_fr"],\
    #             "retailer_name" : ["Marionnaud", "Folie Cosmetic", "L'Oréal Paris France", "Amazon France", "Sephora France"]}
    # retailer = pd.DataFrame(data = retailer)
    # retailer.to_csv(scraping_path + "/retailer_merged.csv")
                
