"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query

app = FastAPI(title="SDD Workshop — Reports API", version="0.1.0")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


@app.get("/", response_class=HTMLResponse)
def get_reports_page() -> str:
    """Serve the interactive reports interface."""
    template_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Interface template not found")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> ReportListResponse:
    """Return a paginated list of reports.

    Public fields only — `internal_id` and `owner_email` are stripped via
    `ReportPublic.from_internal`.
    """

    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    page = rows[offset : offset + limit]
    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )


@app.get("/reports/csv")
def export_reports_csv(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
) -> StreamingResponse:
    """Return a streaming CSV file of the filtered and sorted reports.

    Omits internal-only fields to comply with specifications.
    """
    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    def generate_csv():
        output = StringIO()
        writer = csv.writer(output, lineterminator="\n")
        
        # Write RFC 4180 headers
        writer.writerow(["id", "title", "status", "owner", "amount", "created_at"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for r in rows:
            # Format datetime as ISO string
            created_at_str = r.created_at.isoformat()
            writer.writerow([r.id, r.title, r.status, r.owner, r.amount, created_at_str])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = f"reports_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )

