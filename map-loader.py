import requests
import shutil
import os
import math
url = "https://api.mapbox.com/v4/mapbox.satellite/18/168524/103183@2x.webp?sku=1018DZeiAMiF9&access_token=pk.eyJ1IjoibmF2aWRzYXZhcmliIiwiYSI6ImNsM2lmdm5vdDBwZm4zaW54ZXliazcxNWkifQ.24943EDJln8CfDPmHhY2Ow"
base_url="https://api.mapbox.com/v4/mapbox.satellite/"
tail_url="?sku=1018DZeiAMiF9&access_token=pk.eyJ1IjoibmF2aWRzYXZhcmliIiwiYSI6ImNsM2lmdm5vdDBwZm4zaW54ZXliazcxNWkifQ.24943EDJln8CfDPmHhY2Ow"
payload = {}
headers = {}
base_range=7
lat, lon=35.687527,51.385785     

def lat_lon_to_tile_indices(lat, lon, zoom):
    """
    Convert latitude and longitude to tile indices at a given zoom level.

    Parameters:
    lat (float): Latitude in degrees.
    lon (float): Longitude in degrees.
    zoom (int): Zoom level.

    Returns:
    tuple: (x, y) tile indices.
    """
    x = math.floor((lon + 180) / 360 * 2**zoom)
    y = math.floor((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2**zoom)
    return (x, y)




def download_image(url,base_path='maps'):
    file_name=url.split('/')[-1].split('?')[0]
    x=url.split('/')[-2]
    z=url.split('/')[-3]

    directory = os.path.join(base_path,z, x)
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(directory, file_name)
    print(file_path)
    if not  os.path.isfile(file_path):
        response = requests.request("GET", url, headers=headers, data=payload, stream=True)
        if response.status_code == 200:
            # Open a local file with write-binary mode
            with open(file_path, 'wb') as out_file:
                # Copy the response data to the local file
                shutil.copyfileobj(response.raw, out_file)
            print("File downloaded successfully")
        else:
            print(f"Failed to retrieve the file. Status code: {response.status_code}")
        response.close()
    else:
        print("File existed")


for zoom in range(15,23):
    x,y=lat_lon_to_tile_indices(lat, lon, zoom)
    for rangex in range(-1*base_range,base_range+1):
        for rangey in range(-1*base_range,base_range+1):
            url=base_url+str(zoom)+'/'+str(x+rangex)+'/'+str(y+rangey)+'@2x.webp'+tail_url
            download_image(url)


        

# for key in config.keys():
#     for rangex in range(config[key]['range']):
#         for rangey in range(config[key]['range']):
#             url=base_url+key+'/'+str(config[key]['center'][0]+rangex)+'/'+str(config[key]['center'][1]+rangey)+'@2x.webp'+tail_url
#             download_image(url)
    


