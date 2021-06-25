import requests
import pandas as py
from bs4 import BeautifulSoup

RawData = py.read_csv(r"top-1m.csv");
DataExcel = [];
count =0;
for row in RawData.index:
    if row >=10000:
        break;
    CurrentURL = RawData['URL'][row]
    print(CurrentURL)

    URL = "https://www." + CurrentURL;
    # Creating Session and Header
    try:  # Creating Session and Header
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.1847.131 Safari/537.36';
        response = s.get(URL, timeout=5.0);
    except requests.ConnectionError as e:
        continue;
    except requests.Timeout as e:
        continue;
    except requests.TooManyRedirects as e:
        continue;
    except requests.exceptions.RequestException as e:
        continue;
    except Exception:
        continue;
        # print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('script');
    for job\
            in jobs:
        if job.attrs.get('src') != None:
            count+=1;
            Exdata = [job.attrs.get('src'), URL];
            DataExcel.append((Exdata));
    print(count)
DataExcelFile = py.DataFrame(DataExcel, columns=['DataURLs','Source']);
DataExcelFile.to_csv('top10kjsfiles.csv');