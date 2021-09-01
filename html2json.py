#Import needed librairies
from bs4 import BeautifulSoup
import json
import re
from os import listdir
from os.path import isfile, join

file_list2 = []
my_file = open("file_list.txt", "r", encoding="utf-8")
for line in my_file:
    file_list2.append(line)
my_file.close()   
file_list = [s.replace("\n", "") for s in file_list2]

for file in file_list:
    
    #Import HTML file
    with open("original_html/" + file, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
       
    
    # Extract names list
    my_file = open("name_list.txt", "r", encoding="utf-8")
    content = my_file.read()
    name_list = content.split("\n")
    my_file.close()

    # Extract titles list
    my_file = open("title_list.txt", "r", encoding="utf-8")
    content = my_file.read()
    title_list = content.split("\n")
    my_file.close()


    # Create list of html files
    html_list = [f for f in listdir("original_html/") if isfile(join("original_html/", f))]
    html_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    # Find position of file in file list
    file_position = html_list.index(file)

    # Input name
    name = name_list[file_position]

    # Input title
    title = title_list[file_position]

    # Extract title for each section
    section_title = []
    title_box_column_create = "title-box-column-create"
    for title_box_column_create in soup.find_all('div', class_= title_box_column_create):
        section_title.append(title_box_column_create.text)


    # Extract image name for each section
    image_name = []
    for div in soup.find_all('div'): 
        if div.img:
            if div.img['alt'] == "":
                image_name.append("No name")
            else:
                image_name.append(div.img['alt']) 
    

    # Extract image url for each section
    image_url = []
    for div in soup.find_all('div'): 
        if div.img:
            if div.img['alt'] == "":
                image_url.append(div.img['src'])
            else:
                image_url.append(div.img['src']) 
    

    # Get list of captions
    array_of_captions = []
    div_list = soup.findAll("div", {"class":"imagearea-column-create"})
    for element in div_list:
        array_of_captions.append(element.find('p').text)
    
    
    # Extract body for each section
    bod1 = []
    body = []
    for x in soup.find_all('div'):
        for page in soup.find_all('p'):
            if page.get_text() != x.find('p'):
                bod1.append(page.text)
    bod2 = [s.replace("\u3000", "") for s in bod1]
    body = [s.replace("\n", "") for s in bod2]
    
    #Extract comment
    comment = body[0]

    alt_array = []
    for div in soup.find_all('div'): 
        if div.img:
            alt_array.append(div.p.text)   
    
    for i in body:
        if alt_array.count(i) > 0:
            body.remove(i)
    

    # Count number of titles
    section_count = len(section_title)

    # Count number of images
    image_count = len(image_name)
    
    # Count number of bodies
    p_count = len(body)

    
    maximum = max(section_count, image_count)

    while section_count < image_count:
            section_title.append("No title")
            section_count = len(section_title)

    while section_count > image_count:
            image_name.append("No name")
            image_url.append("No url")
            image_count = len(image_name)
    
    maximum = max(section_count, image_count)

    
    #Create data
    data = {"Name":name,
    "Title":title,
    "Comment":comment,
    "Contents":[
    
    ],
    "Profile image":[
        image_name[0],
        image_url[0],
    ]
    }
    
    contents_array = []
    for i in range(0,maximum-1):
        a = { 
        "Section Title":section_title[i],
        "Image name":image_name[i+1],
        "Image url": image_url[i+1],
        "Body":body[i],
        },
        data["Contents"] = data["Contents"] + list(a)
    
    
    #Export data to a json file
    with open('json_files/' + file + '.json', 'wb') as json_file:
        json_file.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf8"))

print("Json files successfully created in folder 'json_files' !")
