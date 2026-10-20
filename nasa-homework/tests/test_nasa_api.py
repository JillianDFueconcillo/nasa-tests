# Imports Python's built-in tool for sending web requests. We need it to contact NASA.
import urllib.request
import json

# This defines a test function
def test_nasa_search_status():
    # Ask NASA to search for moon images
    url = "https://images-api.nasa.gov/search?q=moon&media_type=image&page=1"

    # Send the request and check NASA's response
    with urllib.request.urlopen(url) as response:
        # The request should succeed with status 200
        assert response.status == 200


def test_nasa_search_returns_results():
    # Ask NASA for moon images
    url = "https://images-api.nasa.gov/search?q=moon&media_type=image&page=1"

    # Send the request and read NASA's JSON response
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    # Get the list of search results
    items = data["collection"]["items"]

    # Check that NASA returned at least one result
    assert len(items) > 0

def test_nasa_search_result_has_title_and_id():
    # Ask NASA for moon images
    url = "https://images-api.nasa.gov/search?q=moon&media_type=image&page=1"

    # Send the request and read NASA's JSON response
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    # Get the search results
    items = data["collection"]["items"]

    # Check that at least one result exists
    assert len(items) > 0

    # Get the first result's metadata
    first_result = items[0]["data"][0]

    # Check that its title and NASA ID are present
    assert first_result.get("title")
    assert first_result.get("nasa_id")


def test_nasa_search_results_have_valid_fields_and_unique_ids():
    # ask for NASA for moon images
      url = "https://images-api.nasa.gov/search?q=moon&media_type=image&page=1"

      # Send the request and read the JSON response
      with urllib.request.urlopen(url) as response:
        data = json.load(response)

      # Get the search results
      items = data["collection"]["items"]

      # Check that NASA returned several results
      assert len(items) >= 5

      # Store NASA IDs so we can check for duplicates
      nasa_ids = []

      # Check each results
      for item in items:
        # each result should contain a metadata list
        assert "data" in item
        assert len(item["data"]) > 0

        # Get the metadata for this result
        metadata = item["data"][0]

        # Check that title and NASA ID are non-empty strings
        assert isinstance(metadata.get("title"), str)
        assert metadata["title"].strip() != ""

        assert isinstance(metadata.get("nasa_id"), str)
        assert metadata["nasa_id"].strip() != ""

        # Remember this result's NASA ID
        nasa_ids.append(metadata["nasa_id"])

    # Check that every NASA ID is unique
        assert len(nasa_ids) == len(set(nasa_ids))  


def test_nasa_asset_returns_downloadable_links():
    # First, search NASA for moon images
    search_url = "https://images-api.nasa.gov/search?q=moon&media_type=image&page=1"

    # Ask NASA for the search results
    with urllib.request.urlopen(search_url) as response:
        search_data = json.load(response)

    # Get the NASA ID of the first image
    items = search_data["collection"]["items"]
    nasa_id = items[0]["data"][0]["nasa_id"]

    # Use that ID to ask NASA for the image's asset links
    asset_url = f"https://images-api.nasa.gov/asset/{nasa_id}"

    # Send the asset request and read the response
    with urllib.request.urlopen(asset_url) as response:
        asset_data = json.load(response)

    # Get the list of downloadable asset files
    asset_items = asset_data["collection"]["items"]

    # Check that NASA returned at least one asset
    assert len(asset_items) > 0

    # Check that every asset has a usable web address
    for asset in asset_items:
        assert isinstance(asset.get("href"), str)
        assert asset["href"].startswith("http")


# how it handles a search with no matching results
def test_nasa_search_with_no_matching_results():
    # Search for a phrase that should not match any images
    url = "https://images-api.nasa.gov/search?q=xyznonexistentcheese8093&media_type=image&page=1"

    # Send the request and read NASA's response
    with urllib.request.urlopen(url) as response:
        # even a search with no matches can be a successful request
        assert response.status == 200
        data = json.load(response)

    # Get the search response from NASA's response
    items = data["collection"]["items"]

    # Check that NASA returned a list, even if it is empty. Provide as a list
    assert isinstance(items,list)

    # If no images match, the list should be empty. CHecks that NASA returned no results.
    assert len(items) == 0


# pagination
def test_nasa_search_pages_have_no_duplicate_ids():
    # Prepare a list to store the NASA IDs from each page
    page_ids = []

    # Check the first two pages of moon image results
    # Tells Python to check page 1 and then page 2
    for page_number in [1, 2]:
        # Build a search URL for the current page

        url = f"https://images-api.nasa.gov/search?q=moon&media_type=image&page={page_number}"

        # Ask NASA for this page of results
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

            # Get the search results from NASA's response
            items = data["collection"]["items"]

            # Coillect the NASA ID from each result
            # Collects the NSAA IDs for that page
            ids_on_this_page = []
            for item in items:
                # Get the metadata for this image
                metadata = item["data"][0]

                # Save the nasa ID
                ids_on_this_page.append(metadata["nasa_id"])

            # Rembember the IDs for this page
            page_ids.append(ids_on_this_page)

    # Check that the two pages have no NASA IDs in common
    # checks that two group have no IDs in common
    assert set(page_ids[0]).isdisjoint(set(page_ids[1]))

