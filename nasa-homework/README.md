# NASA Image Library — Automated Tests

## Project Overview

This project contains automated tests for the NASA Image and Video Library using Python and pytest. It checks the NASA public API, the website's image details page, and consistency between API results and the UI.

## Technologies

- Python 3.12
- pytest
- Playwright
- NASA Image and Video Library API

## Project Structure

```text
nasa-homework/
├── tests/
│   ├── test_nasa_api.py
│   └── test_nasa_ui.py
├── check_nasa.py
└── README.md
```

The `.venv` folder contains the local Python virtual environment and installed packages.

## Test Coverage

### API Tests

The API tests verify:

1. Search requests return HTTP 200.
2. Search results are returned.
3. Result titles and NASA IDs are present.
4. Result fields have valid values and IDs are unique.
5. Asset requests return downloadable links.
6. Searches with no matching results are handled correctly.
7. The first two result pages do not contain duplicate NASA IDs.

### UI Test

The UI test opens the NASA details page for an image and checks its title, visibility, successful image loading, and NASA ID.

### Integration Test

The integration test retrieves an image title and NASA ID from the NASA API, opens the corresponding website details page, and verifies that the UI matches the API result.

## How to Run the Tests

Activate the virtual environment in Windows Command Prompt:

```bat
.venv\Scripts\activate
```

Run all tests:

```bat
python -m pytest tests -v
```

Run only API tests:

```bat
python -m pytest tests/test_nasa_api.py -v
```

Run only UI and integration tests:

```bat
python -m pytest tests/test_nasa_ui.py -v
```

## Latest Test Results

The complete test suite ran successfully:

- API tests: 7 passed
- UI tests: 2 passed
- Total: 9 passed

Execution time: 30.28 seconds.

## Notes

These tests use the live NASA API and website. Results and website behavior may change over time, and an internet connection is required.
