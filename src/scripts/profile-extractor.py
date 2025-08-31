import os
import requests
from pathlib import Path
import concurrent.futures

# Constants
BASE_DIR = Path(__file__).parent.parent.parent
BASE_URL = "https://onlinecde.annauniv.edu"
max_workers = os.cpu_count() * 2 if os.cpu_count() else 4 

def get_single_profile(id):
    endpoint = f"user/profile.php?id={id}"
    headers = {
        "cookie": "<>"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 200:
        if "Public profile" not in response.content.decode():
            print(id, "doesn't exist")
        else:
            out_file = os.path.join(BASE_DIR, "outputs", f"profile_{id}.html")
            with open(out_file, "w") as out_file_object:
                out_file_object.write(response.content.decode())
    else:
        print(id, "doesn't exist")
    
def main():
    id_start_range = 10000
    id_end_range = 20000
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_single_profile, id): id for id in range(id_start_range, id_end_range)}
        for future in concurrent.futures.as_completed(futures):
            item_id = futures[future]
            try:
                result = future.result()
                print(f"Received {result} for item {item_id}.")
            except Exception as exc:
                print(f"Item {item_id} generated an exception: {exc}")
    print("Execution Completed")
    
if __name__ == "__main__":
    main()