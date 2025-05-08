# go to git bash
# git config --global user.name "rabina thapa"
#git config --global user.email "rabinathapa38@gmail.comf"

#git init =>initialize git
#git status=> if you want to check what are the status of files
#git diff=> if you want to check what are the changes
#git add .=> track all the files
#git commit -m "Your message"



import json
import sqlite3
import requests  
from bs4 import BeautifulSoup 


URL = "http://books.toscrape.com/"


def create_table():
    con = sqlite3.connect("books.sqlite3")
    cur = con.cursor()
    cur.execute(
            """
                CREATE TABLE if not exists books(
            
                 id integer primary key autoincrement,
                 title text,
                 price real,
                 currency text
                );
             """
 )
    con.commit()
    con.close()

def insert_book(title,currency,price):
        conn = sqlite3.connect("books.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title,currency,price) VALUES(?,?,?)",
            (title,currency,price),
        )

        conn.commit()
        conn.close()




def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    books= []
    

    
    
    #set encoding explicity to handle special character correctly
    response.encoding = response.apparent_encoding
   
    soup = BeautifulSoup(response.text, "html.parser") 
    book_elements = soup.find_all("article", class_ = "product_pod")
    for book in book_elements:
        title = book.h3.a['title']
        price_text=    book.find('p', class_ = "price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
       
        books.append(
                        {
                             'title': title,
                             "currency": currency,
                             "price": price
                        }
                   )




    print("ALL books have been scrapped and saved to the database.")
    return books


#json file ma rakhna lai

def save_to_json(books):
     

     with open("books.json","w", encoding="utf-8") as f:
          json.dump(books, f,indent =4, ensure_ascii = False)


create_table()
books = scrape_books(URL)
save_to_json(books)

#csv ma rakhera aune assigment
