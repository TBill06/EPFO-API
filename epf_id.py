from bs4 import BeautifulSoup as bs
import requests
import pandas

def table(response,pf_data):
    soup = bs(response.text,"html.parser")
    soup.prettify()

    table_row = soup.find_all("tr")[1:]
    if table_row == None:
        print("None")
        return

    for i in table_row:
        row = []
        table_data = i.find_all("td",style= lambda value: value and 'text-align: left;' in value)
        for j in table_data:
            if j.text:
                row.append(j.text)
        pf_data.append(row)

def mainFunction(filename,cookie_name,start_Index,end_Index,captcha,req_url):

    data = pandas.read_csv(f"{filename}"+".csv",on_bad_lines='skip',skipinitialspace=True)
    company_name = data['Full Name'].tolist()

    cookie = {}        
    string = str(cookie_name).split(";")
    for i in string:
        bit = i.split("=")
        cookie[bit[0]] = bit[1]

    payload = {'EstName': '','EstCode': '','captcha': f'{str(captcha)}'}
    pf_data = []
    names = []

    for i in range(int(start_Index),int(end_Index)):
        length = len(pf_data)
        payload['EstName'] = company_name[i]
        response = requests.post(str(req_url),cookies=cookie,json=payload)
        if response.ok:
            table(response,pf_data)
            if (len(pf_data) == length):
                names.append(company_name[i])
            print("Count: ",i," Length: ",len(pf_data))

    df = pandas.DataFrame(pf_data)
    print(df)
    print(names)

def main():
    filename = input("filename: ")
    url = input("URL: ")
    cookie_name = input("Cookie: ")
    captcha = input("Captcha: ")
    s_index = input("Start Index: ")
    e_index = input("End Index: ")

    mainFunction(filename,cookie_name,s_index,e_index,captcha,url)

if __name__ == "__main__":
    main()