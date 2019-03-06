import pandas as pd 
import re

def create_product(input, output):
    df = pd.read_csv(input, usecols = ['product_id', 'product_name', 'price', 'avg_mark', 'product_type'])
    size = df.size

    #Add retailer_id column
    retailer = {'retailer_id' : ['amazon_fr'] * size}
    retailer = pd.DataFrame(data = retailer)
    df = pd.concat([df, retailer], axis=1)

    df.to_csv(output)

def create_retailer(id, name):
    df = {"retailer_id" : [id], "retailer_name" : [name]}
    df = pd.DataFrame(data = df)
    df.to_csv("./retailer.csv")

def create_review(input, output):
    cols = ['product_id', 'author_id', 'mark', 'review_date', 'review_title', 'review_txt', 'useful_review']
    df = pd.read_csv(input, usecols = cols)
    size = df.size

    #Add useless_review column filled with None, client_id and retailer_id
    additional = {'useless_review' : [None] * size,\
                  'client_id' : ["L'Oréal"] * size,\
                  'retailer_id' : ['amazon_fr'] * size\
                  }
    additional = pd.DataFrame(data = additional)
    df = pd.concat([df, additional], axis = 1)

    df.to_csv(output)

def create_consumer(input, output):
    df = pd.read_csv(input, usecols = ['author_id'])
    #Extract unique values of author_id to an array
    df = df['author_id'].unique()

    #Convert back to dataframe
    df = pd.DataFrame(data = {'author_id' : df})

    #Remove null values and reindex
    df = df[df.author_id.notnull()]
    df = df.reset_index(drop = True)

    #author_id is in the form "amzn1.account.[author_id]" from the user profile URL
    #Extract the id 
    size = df.size
    rule = re.compile('[A-Z0-9]+$')
    for i in range(0,size):
        #if i != 27:
        df['author_id'][i] = rule.findall(df['author_id'][i])[0]
    
    #Add the other colomns filled with null
    noneCol = [None] * size
    additional = {'gender' : noneCol,\
                  'eye_color' : noneCol,\
                  'hair_color' : noneCol,\
                  'skin_concerns' : noneCol,\
                  'skintone' : noneCol,\
                  'skintype' : noneCol}
    additional = pd.DataFrame(data = additional)
    df = pd.concat([df, additional], axis = 1)

    df.to_csv(output)




if __name__ == "__main__":
    products = "./loreal_products.csv"
    reviews = "./loreal_reviews.csv"

    #create_product(products, "./product.csv")
    #create_retailer('amazon_fr', 'Amazon France')
    #create_review(reviews, './review.csv')
    create_consumer(reviews, './consumer.csv') 