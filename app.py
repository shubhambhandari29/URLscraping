from flask import Flask, render_template, request , send_file
import pickle
import pdfkit
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

ref = []



@app.route('/')
def index():
    links = pickle.load(open('links.pkl', 'rb'))
    return render_template('home.html',data=links)




@app.route("/1",methods=['POST'])
def submit_data():
    
    links = pickle.load(open('links.pkl', 'rb'))


    out = request.form.getlist("n")
    


    if(len(out)<1): 
        return render_template('home.html',data=links)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    s=Service('C:/Program Files/webdriver/chromedriver')
    browser = webdriver.Chrome(service=s,options=options)
    url= 'https://www.smilefoundationindia.org/'
    




    pdfs = []    
    for i in range(len(out)): 
        browser.get(out[i])
        print(out[i])
        content = browser.page_source
        soup = BeautifulSoup(content,"html.parser" )
        try:
            for a in soup.findAll('a'):
                a['href'] = url+a['href']
        except:
            pass
        try:
            for img in soup.findAll('img'):
                img['src'] = url+img['src']
        except:
            pass
        remove_tags = ['header', 'footer','nav']
    
        for tag in remove_tags: 
          for match in soup.findAll(tag):
             match.replaceWith('')
        for match in soup.findAll(class_="subscribe"):
              match.replaceWith('')
        for match in soup.findAll(class_="row display-none"):
                match.replaceWith('')
        for match in soup.findAll(class_="row display-none-large-screen"):
                match.replaceWith('')       
        for match in soup.findAll(class_="modal fade"):
              match.replaceWith('')
        for match in soup.findAll(class_="bottom-footer text-center"):
             match.replaceWith('')
        for match in soup.findAll(class_="container spacer"):
             match.replaceWith('')



        with open("output1.html", "a", encoding='utf-8') as file:
            file.write(str(soup))
     
        options = {'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in'} 

    try:                
        pdfkit.from_file("output1.html", "result.pdf",options=options)
    except:
        pass

    f = open("output1.html","w")
    f.close()
    print("ITS DONE")

    path = 'C:/workbook/smilefoundation/result.pdf'
    return render_template('home.html',data=links,path=path)




@app.route("/2")
def download():
    path = 'C:/workbook/smilefoundation/result.pdf'
    return send_file(path,as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)