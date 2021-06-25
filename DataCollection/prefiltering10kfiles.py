
import pandas as py

def takedata():
    RawData = py.read_csv(r"top10kjsfiles.csv");
    counter = 0;
    Defaulter_Websites = [];

    for row in RawData.index:
        CurrentURL = RawData['DataURLs'][row]
        # print(CurrentURL)
        if isinstance(CurrentURL,float) == False : #len(CurrentURL) != 0:
            print(CurrentURL)
            if CurrentURL.startswith("https://") and CurrentURL.find('.js') != -1:
                counter+=1;
                Defaulter_Websites.append(CurrentURL);

    print(counter);
    Defaulter_Websites_Data = py.DataFrame(Defaulter_Websites, columns=['URL'])
    Defaulter_Websites_Data.to_csv('prefilteredtop10kjsfiles.csv')


def removeduplicates():
    RawData = py.read_csv(r"prefilteredtop10kjsfiles.csv");
    RawData.drop_duplicates(subset="URL", inplace=True);
    Defaulter_Websites_Data = py.DataFrame(RawData, columns=['URL'])
    Defaulter_Websites_Data.to_csv('prefilteredtop10kjsfiles.csv')

if __name__ == '__main__':
    takedata();
    removeduplicates();