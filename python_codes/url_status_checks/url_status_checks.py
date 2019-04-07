import requests
import HTML_py as HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Declare Variables
Links            = "C:\\Users\\Some Where\\Google Drive\\Python\\New folder\\My Programs\\links.txt"
subject          = "Subject"
from_address     = "xxx@gmail.com"
to_address       = "xxx@gmail.com"
url_status       = list()
Lines            = list()
resultant_colors = {
    'Connection Successfull':  '#3CB371',
    'Connection Error':        '#FFA07A'
}
htmlcode = HTML.Table(header_row=['Status','Message','URL','code'],style="border: 3px solid #000000; border-collapse: collapse;",cellpadding="8")


def sending_email_notification(html_data):
    msg            = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = from_address
    msg['To']      = to_address
    part           = MIMEText(html_data, 'html')
    msg.attach(part)
    mail           = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.sendmail(from_address, to_address, msg.as_string())
    mail.quit()

def get_site_status(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        if requests.get(url).status_code == 200:
            return ["Connection Successfull","URL is UP",r.url,r.status_code]
    except requests.exceptions.Timeout as e:
        return ["Connection Error","Timeout Error",r.url,r.status_code]
    except requests.exceptions.TooManyRedirects as e:
        return ["Connection Error","TooManyRedirects Error",r.url,r.status_code]
    except requests.exceptions.HTTPError as e:
        return ["Connection Error","HTTP Error",r.url,r.status_code]
    except requests.exceptions.RequestException as e:
        return ["Connection Error","Request Exception",url,None]
    except requests.exceptions.ConnectionError as e:
        return ["Connection Error","Connection Error : ",r.url,r.status_code]
    
def main(urls):
    for url in urls:
        url_status.append(get_site_status(url))
        #status,message,URL,,''code = get_site_status(url)
        #print (status + " - " + message + " - " + URL + " - " + str(code))
        #print ('\n'.join([str(lst) for lst in url_status]))
#print (url_status)


if __name__ == '__main__':
    with open(Links) as l:
        for line in l:
            Lines.append(line.strip())
        main(Lines)
        
    for i in url_status:
        colour = resultant_colors[i[0]]
        coloured_row = HTML.TableRow(i,attribs={'bgcolor': colour})
        htmlcode.rows.append(coloured_row)
    sending_email_notification(str(htmlcode))
