
import json
import urllib.request
import urllib.parse

# Build a NASA API search URL for moon images.
query = urllib.parse.urlencode({
    "q": "moon",
    "media_type": "image",
    "page": 1
})

url = f"https://images-api.nasa.gov/search?{query}"

# Send the request to NASA and read the response.
with urllib.request.urlopen(url) as response:
    data = json.load(response)

# Get the search results.
items = data["collection"]["items"]

# Print the number of results returned by the API.
print("Number of API results:", len(items))

# Print the first five result titles and NASA IDs.
for item in items[:5]:
    # Some results may have no metadata, so check first.
    metadata_list = item.get("data", [])

    if metadata_list:
        metadata = metadata_list[0]
        print("\nTitle:", metadata.get("title"))
        print("NASA ID:", metadata.get("nasa_id"))
