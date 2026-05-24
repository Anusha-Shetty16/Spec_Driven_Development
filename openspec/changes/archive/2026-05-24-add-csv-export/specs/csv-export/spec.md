## ADDED Requirements

### Requirement: CSV Export Endpoint
The system SHALL expose a GET endpoint at `/reports/csv` that generates and streams a CSV file containing matching report records.
It MUST support query parameters to filter by `status` (pending, approved, rejected, archived), `date_from` (inclusive lower bound), and `date_to` (inclusive upper bound), and sort by `id`, `title`, `status`, `owner`, `amount`, or `created_at` with an optional `descending` toggle.
The streamed CSV file MUST:
- Comply with RFC 4180 (including column header row).
- Contain only the public fields: `id`, `title`, `status`, `owner`, `amount`, and `created_at`.
- Exclude internal-only fields such as `internal_id` or `owner_email`.
- Format `created_at` as an ISO 8601 string.
- Have a filename starting with `reports_export_` followed by the current local datetime timestamp and ending with `.csv`.

#### Scenario: Request CSV export without parameters
- **WHEN** a GET request is sent to `/reports/csv` with no query parameters
- **THEN** the system streams a CSV file containing all reports sorted by `created_at` descending

#### Scenario: Request CSV export with filters and custom sort
- **WHEN** a GET request is sent to `/reports/csv` with `status=approved`, `sort=amount`, and `descending=false`
- **THEN** the system streams a CSV file containing only approved reports sorted by amount in ascending order

### Requirement: Dashboard CSV Export Trigger
The dashboard UI SHALL feature an "Export CSV" button in the control panel.
When clicked, the application MUST query the active filter states (status, date ranges) and sorting configuration (sort by field, sort direction), construct matching HTTP query parameters, and trigger a native browser file download from the `/reports/csv` endpoint.

#### Scenario: Click Export CSV button on dashboard
- **WHEN** the user selects "Approved" status, sets a "Date From" filter, and clicks the "Export CSV" button
- **THEN** the browser triggers a file download pointing to the matching `/reports/csv` endpoint with the active filters passed as query parameters
