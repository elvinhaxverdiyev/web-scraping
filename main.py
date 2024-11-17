import httpx
from selectolax.parser import HTMLParser
import json
import smtplib

url_address = "https://www.keychron.com/?srsltid=AfmBOoo1f3MLzdm4USGifTNNAIrUSWfBAfoAI5HCUfkPmXneMpdJ1rVt"
css_class = "div.card__info"


def get_html(url: str, css_selector: str) -> list:
    resp = httpx.get(url)
    html = HTMLParser(resp.text)
    return html.css(css_selector)

def get_info(*, source: list, **dict_data) -> list:
    web_info = [ ]
    for element in source:
        item = { }
        for key, selector in dict_data.items():
            node = element.css_first(selector)
            item[key] = node.text(strip=True) if node else "tapilmadi"
        web_info.append(item)
    return web_info
        

def write_to_json_file(data: list, file_name: str):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(file_name)
    
def read_json_file(file_name: str) -> str:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"JSON xeta: {e}")
        return ""


def send_mail(sender: str, password: str, receiver: str, subject: str, body: str):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender, receiver, message)
        print("Gmail gonderildi!")
    except Exception as e:
        print(f"Xeta: {e}")
    finally:
        server.quit()

data_source = get_html(url_address, css_class)
info = get_info(source=data_source, name=".card__title", price=".price__current")
write_to_json_file(info, "output.json")
json_content = read_json_file("output.json")
sender_email = "elvinhaqverdiyev717@gmail.com"
sender_password = "ypaqhsabfisjwolb" 
receiver_email = "elvinhaxverdiyev777@gmail.com"
subject = "Mehsul melumatlari:"
body = f"JSON filesi:\n{json_content}"

send_mail(sender_email, sender_password, receiver_email, subject, body)


# resp = httpx.get(url)
# html = HTMLParser(resp.text)

# data = html.css(css_class)

# web_info = []

# for item in data:
#     info = { }
#     title_element = item.css_first(".card__title")
#     price_element = item.css_first(".price__current")
    
#     if title_element:
#         info["title"] = title_element.text().strip()
#     else:
#         info["title"] = "Basliq tapilmadi"
    
#     if price_element:
#         info["price"] = price_element.text().strip()
#     else:
#         info["price"] = "Qiymet tapilmadi"
    
#     web_info.append(info)
    
# print(web_info)
        
            
