#Author: John Ferlic
#Created: 1/12/2020

from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    file = open("stocks.txt", "r")
    contents = file.readlines()
    y = "{"
    for x in range(2):
        y += '"name": "{}"'.format(contents[x])
        print(x)
        if x != len(contents)-1:
            y += ","
    y += "}"
    return y
        
    

if __name__ == "__main__":
  app.run()