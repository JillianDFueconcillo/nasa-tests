
from playwright.sync_api import expect


def test_nasa_image_details(page):
    # Open the details page for a known NASA image.
    page.goto(
        "https://images.nasa.gov/details/PIA12235",
        wait_until="domcontentloaded"
    )

    # Check that the page heading contains the image title.
    heading = page.locator("h1:visible")
    expect(heading).to_contain_text("Nearside of the Moon")

    # Find the preview image by its descriptive alt text.
    # Select the actual NASA preview image, not the placeholder.
    preview = page.locator("#details_img")

    # Check that the image is visible.
    expect(preview).to_be_visible()

    # Check that the image has a source URL.
    image_source = preview.get_attribute("src")
    assert image_source, "The preview image should have a source URL"

    # Check that the browser successfully loaded the image.
    image_loaded = preview.evaluate(
        "(img) => img.complete && img.naturalWidth > 0"
    )
    assert image_loaded, "The preview image did not load successfully"

    # Confirm the NASA ID appears in the page URL.
    assert "PIA12235" in page.url

    # Print a short success message.
    print("\nVerified NASA image: Nearside of the Moon")
    print("NASA ID: PIA12235")
    print("Preview image loaded successfully")

import json
import urllib.request
from urllib.parse import quote
 

def test_nasa_api_result_matches_ui(page):
    # Search NASA's API for moon images.
    api_url = (
        "https://images-api.nasa.gov/search"
        "?q=moon&media_type=image&page=1"
    )

    # Send the API request and read its JSON response.
    with urllib.request.urlopen(api_url) as response:
        api_data = json.load(response)

    # Get the search results from the API response.
    items = api_data["collection"]["items"]

    # Find the first result with a title and NASA ID.
    selected_result = None

    for item in items:
        # Get the metadata for this result.
        metadata_list = item.get("data", [])

        if not metadata_list:
            continue

        metadata = metadata_list[0]
        title = metadata.get("title")
        nasa_id = metadata.get("nasa_id")

        # Choose a result with both required values.
        if title and nasa_id:
            selected_result = {
                "title": title,
                "nasa_id": nasa_id
            }
            break

    # Make sure the API returned a usable result.
    assert selected_result is not None, (
        "NASA API returned no results with a title and NASA ID"
    )

    api_title = selected_result["title"]
    nasa_id = selected_result["nasa_id"]

    # Open the same NASA item in the browser.
    encoded_id = quote(nasa_id, safe="")
    details_url = f"https://images.nasa.gov/details/{encoded_id}"

    page.goto(
        details_url,
        wait_until="domcontentloaded"
    )

    # Find the visible page heading.
    heading = page.locator("h1:visible")
    expect(heading).to_contain_text(api_title)

    # Check that the NASA ID is in the details URL.
    assert nasa_id in page.url

    # Verify that the actual preview image loads.
    preview = page.locator("#details_img")
    expect(preview).to_be_visible()

    image_loaded = preview.evaluate(
        "(img) => img.complete && img.naturalWidth > 0"
    )
    assert image_loaded, "The NASA preview image did not load"

    # Print the values compared by this integration test.
    print("\nAPI title:", api_title)
    print("NASA ID:", nasa_id)
    print("UI heading:", heading.inner_text().strip())
    print("API result matches the UI")
