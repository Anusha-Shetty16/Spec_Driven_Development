## Context

The Reports dashboard serves an interactive financial reporting table from a FastAPI backend. Currently, sorting, filtering, and pagination are fully functional, powered by the backend query layer in `app/reports.py`. The design calls for exposing a matching `/reports/csv` endpoint and wiring up the existing but inactive "Export CSV" button to download the currently visible (filtered/sorted) report dataset in standard CSV format.

## Goals / Non-Goals

**Goals:**
- Implement a streaming `/reports/csv` endpoint in FastAPI that uses the shared `app/reports.py:query` layer.
- Format timestamps, currency amounts, and text fields in accordance with the specifications.
- Hook up the frontend CSV button via JavaScript in `app/templates/index.html` to pass the correct active filter and sorting states.

**Non-Goals:**
- Altering the backend `app/reports.py` query engine or sorting rules.
- Redesigning the visual styles of the dashboard.
- Pagination for the CSV export (the export should return all records matching the current filters).

## Decisions

### 1. Endpoint Architecture: `/reports/csv`
- **Choice**: Implement the GET `/reports/csv` endpoint returning a `StreamingResponse` from a generator function using Python's standard `csv` module with `io.StringIO`.
- **Alternatives considered**: 
  - *Generate full CSV string in memory*: Simpler, but incurs memory overhead proportional to the dataset size. Streaming is more scalable and standard for report generation.
- **Rationale**: Streaming avoids high memory spikes when exporting very large lists of reports.

### 2. Logic Sharing
- **Choice**: Direct import and invocation of `app.reports.query` inside the new `/reports/csv` endpoint.
- **Rationale**: Reusing `query` ensures perfect parity in sorting and filtering logic between the paginated browser grid and the full CSV export.

### 3. Frontend Triggering Mechanism
- **Choice**: Utilize standard `window.location.href = '/reports/csv?' + params` in JavaScript.
- **Alternatives considered**:
  - *AJAX fetch with Blob download*: Allows custom header management in JS, but adds complexity and manual browser-specific download hacks.
- **Rationale**: Navigating directly to the GET URL relies on browser-native content-disposition handling, providing the most reliable and simple download experience.

## Risks / Trade-offs

- **[Risk] Date Handling Parity** -> *Mitigation*: Make sure the frontend converts simple date inputs to complete ISO 8601 strings (e.g., setting the "Date To" field to the end of the selected day) to match backend date logic exactly.
- **[Risk] Field Inadvertent Exposure** -> *Mitigation*: The CSV streaming writer explicitly creates rows using a fixed list of public attributes, preventing private database fields (`internal_id`, `owner_email`) from leaking.
