import requests
import os
import json

master = {"references": []}

def download_file(url, type_of, id):
    if url:
        local_filename = os.path.join(os.getcwd(), type_of, url.split('/')[-1])
        master['references'].append({str(id): local_filename})
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            check_folder(type_of)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
        return local_filename

def check_folder(path):
    if os.path.exists(os.path.join(os.getcwd(), path)):
        return

    else:
        os.makedirs(os.path.join(os.getcwd(), path))

def generate_type_url(data):
    for x in data:
        try:
            yield (x["attributes"]["item_type"], x["attributes"]["cdn_asset_path"], x["id"])

        except KeyError:
            print(f"FAILED: {x}")

if __name__ == '__main__':
    with open("item_data.json", encoding="utf-8") as f:
        item_data = json.loads(f.read())

    type_url_data = [x for x in generate_type_url(item_data)]

    for t, p, i in type_url_data:
        print(f"{t}: Saving file from {p}")
        download_file(p, t, i)

    with open("image_reference.json", "w") as o:
        json.dump(master, o)

