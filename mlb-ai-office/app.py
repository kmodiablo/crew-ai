import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import datetime
import logging
from html import escape
from daily_picks_reporter import DailyMLBPicksReporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Oficina de AI Apuestas - Daily MLB Reporter")

# Optional: cache for report to avoid regenerating on every request
_report_cache = {
    "report": None,
    "timestamp": None
}

CACHE_DURATION_MINUTES = 60

def is_cache_valid():
    """Check if cached report is still fresh"""
    if _report_cache["timestamp"] is None:
        return False
    age = datetime.datetime.now() - _report_cache["timestamp"]
    return age.total_seconds() < (CACHE_DURATION_MINUTES * 60)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with navigation links"""
    return """
    <html>
    <head><title>Oficina de AI Apuestas</title></head>
    <body>
    <h1>🚀 Oficina de AI Apuestas Server</h1>
    <p>Daily MLB Picks Reporter is running!</p>
    <ul>
        <li><a href="/report">View Today's Report</a></li>
        <li><a href="/trigger">Manually Trigger Report Now</a></li>
        <li><a href="/health">Health Check</a></li>
    </ul>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/report", response_class=HTMLResponse)
async def get_report():
    """Get the daily report"""
    try:
        # Check if we have a valid cache
        if _report_cache["report"] and is_cache_valid():
            logger.info("Returning cached report")
            return _report_cache["report"]
        
        # Generate new report
        reporter = DailyMLBPicksReporter()
        report_text = reporter.generate_report()
        
        if report_text is None:
            report_text = "Report generated but no output available"
        
        safe_report = escape(str(report_text))
        
        html_response = f"""
        <html>
        <head><title>Daily MLB Report</title></head>
        <body>
        <h1>Daily MLB Picks Report</h1>
        <p>Generated: {datetime.datetime.now()}</p>
        <pre>{safe_report}</pre>
        <a href="/">Back to Home</a>
        </body>
        </html>
        """
        
        # Cache the response
        _report_cache["report"] = html_response
        _report_cache["timestamp"] = datetime.datetime.now()
        
        return html_response
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.post("/trigger")
async def trigger_report():
    """Manually trigger report generation and save to file"""
    try:
        reporter = DailyMLBPicksReporter()
        reporter.generate_report()
        reporter.save_report_to_file()
        
        return {
            "status": "success",
            "message": "Daily report triggered successfully",
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error triggering report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error triggering report: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)