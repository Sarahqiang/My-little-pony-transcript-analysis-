import json
import os,sys
from datetime import datetime
import re
import pytz

outputfile = sys.argv[4]
def validate_tittle(line):
    line = json.dumps(line)
    if('title' in line):
        #with open(outputfile, 'a') as json_file:
        #    newline = json.dumps(line)
        #    json_file.write(newline+"\n")
        return True
    else:
        return False
def change_tittle(line):
        newline = json.dumps(line)
        newline = newline.replace('title_text','tittle')
        return newline
        #print(newline)
def standadise_time(line):
    if('createdAt' in line):
        line['createdAt'] =datetime.strptime(line['createdAt'],'%Y-%m-%dT%H:%M:%S%z')
        line['createdAt'] = line['createdAt'].astimezone(pytz.UTC).isoformat()
def validate_author(line):
    if('author' in line):
     if(line["author"]=="N/A" or line["author"]=="null" or line["author"] == None):
         return False
     else:
         return True
    return False
def count_validate(line):
    if('total_count'in line):
     count = line["total_count"]
     if(type(count)==str):
        if(count.isnumeric()):
            line["total_count"] = int(count)
            return True
        else:
            return False
     if(type(count)==float):
        line["total_count"]=int(count)
        return True
     if(type(count)== int):
         return True

    else:
        return False
def tag_modified(line):
    newtag =[]
    if("tags"in line):
        tag = line["tags"]
        #print(tag)
        for i in tag:
            if (' 'in i):
                #print(i)
                newelement =i.split(' ')
                for j in newelement:
                 newtag.append(j)
            else:
                newtag.append(i)
        #print(newtag)
        line["tags"]=newtag

     #line["tags"]=[x.replace(' ',',')for x in line["tags"]]

def validate_isodatetime(line):
    format_string ='%Y-%m-%dT%H:%M:%S%z'
    dt = line["createdAt"]
    colon = dt[-3]
    if colon != ':':
        # print(colon)
        line["createdAt"] = dt[:-2] + ':' + dt[-2:]

    try:
        #print(line["createdAt"])
        #datetime.fromisoformat(line["createdAt"])
        datetime.strptime(line["createdAt"], format_string)
        line['createdAt'] = datetime.strptime(line['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
        line['createdAt'] = line['createdAt'].astimezone(pytz.UTC).isoformat()
        #print(datetime.fromisoformat(line["createdAt"]))
        return True
    except  ValueError:
                        return False





def main():
     inputfile = sys.argv[2]
     with open(inputfile) as f:
         for json_line in f:
             try:
                 line = json.loads(json_line)
                 #print(validate_tittle(line))
                 #print(validate_isodatetime(line))
                 if (validate_tittle(line) & validate_author(line) & count_validate(line) & validate_isodatetime(line)):
                     #standadise_time(line)
                     tag_modified(line)
                     result = change_tittle(line)
                     with open(outputfile, 'a') as json_file:
                        #newline = json.dumps(result)
                        json_file.write(result+"\n")
                     #standadise_time(line)
                     print (result)

             except ValueError:
                 continue
if __name__ ==  "__main__":
    main()