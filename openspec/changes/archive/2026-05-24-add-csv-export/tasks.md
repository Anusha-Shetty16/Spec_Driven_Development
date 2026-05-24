## 1. Backend Implementation

- [x] 1.1 Expose the GET `/reports/csv` endpoint in `app/main.py` to stream reports as a CSV
- [x] 1.2 Implement the `generate_csv` generator to stream data chunks in memory using `StringIO` and `csv.writer`
- [x] 1.3 Ensure proper RFC 4180 standard headers and public field filtering (excluding `internal_id` and `owner_email`)
- [x] 1.4 Format the CSV filename dynamically with the current local datetime timestamp

## 2. Frontend Integration

- [x] 2.1 Bind the "Export CSV" button click event in `app/templates/index.html`
- [x] 2.2 Construct the matching query parameters based on the currently selected filter and sort options in the dashboard
- [x] 2.3 Set `window.location.href` to trigger the native browser download seamlessly

## 3. Verification

- [x] 3.1 Verify the `/reports/csv` endpoint functions correctly and returns standard CSV text under default parameters
- [x] 3.2 Verify the endpoint correctly filters and sorts CSV output when passing query parameters
- [x] 3.3 Verify that internal-only fields are completely excluded from the exported CSV rows
