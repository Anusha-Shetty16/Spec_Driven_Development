## Why

Users of the SDD Reports Hub currently can only view financial reports in the browser interface. To enable offline data analysis, sharing, and custom processing, they require a way to export their filtered and sorted tabular reports directly as a standardized CSV file.

## What Changes

- **Add "Export CSV" Button**: Wire up the premium "Export CSV" button in the frontend dashboard control board.
- **Implement `/reports/csv` Endpoint**: Add a backend API endpoint that generates a streaming, RFC 4180-compliant CSV file with public report fields and ISO 8601 UTC timestamps.
- **Sync Filter/Sort State**: Ensure the exported CSV reflects the currently selected status, date ranges, and sorting options in the user's dashboard view.

## Capabilities

### New Capabilities
- `csv-export`: Standardized, streaming export of filtered and sorted report data to CSV format.

### Modified Capabilities
<!-- None. No existing capabilities are being modified at the specification level. -->

## Impact

- **Frontend**: `app/templates/index.html` requires JavaScript changes to correctly pass current filter/sort state to the export URL and trigger a native browser file download when the export button is clicked.
- **Backend**: `app/main.py` needs a streaming CSV generation endpoint `/reports/csv` utilizing standard library `csv` and `io.StringIO` to format reports efficiently.
- **Testing**: Automated integration tests are required to verify the CSV structure, public field compliance, and parameter-based filtering/sorting.
