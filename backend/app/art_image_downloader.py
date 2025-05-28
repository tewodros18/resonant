import requests
import os
import json


def download_objects_by_department():
    try:
        response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId=11&artistOrCulture=true&q=Rembrandt")
        response.raise_for_status()

        data = response.json()

        with open('rembrant_objects_id.json', 'w') as file:
            json.dump(data, file, indent=4)

    except:
        print ("Error: Unable to connect to the server.")

def download_art_object_from_ids():
    with open('art_objects_id.json', 'r') as file:
        data = json.load(file)
    for object_id in data['objectIDs'][5:11]:
        try:
            response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}")
            response.raise_for_status()

            os.makedirs(f"./static/{object_id}", exist_ok=True)
            
            object_data = response.json()

            f_name = f"./static/{object_id}/{object_id}.json"
            with open(f_name, 'w') as file:
                json.dump(object_data, file, indent=4)

            image_url = object_data.get('primaryImage')
            if image_url:
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                file_name = f"static/{object_id}/{object_id}.jpg"
                with open(file_name, 'wb') as img_file:
                    img_file.write(image_response.content)
                print(f"Downloaded {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading object {object_id}: {e}")

download_art_object_from_ids()


#download_objects_by_department()