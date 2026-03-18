
import logging
from threading import Lock
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.exc import DataError, IntegrityError
from fastapi_backend.app.services.market_data import MarketDataService
from prometheus_client import Counter, Gauge
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.auth import require_read_permission, require_write_permission
from app.schemas.market_data import (
    MarketDataCreate,
    MarketDataInDB,
    MarketData,
)
from app.db.session import get_db

router = APIRouter()


# In-memory polling job store and lock
polling_jobs = {}
job_counter = [0]
jobs_lock = Lock()

# Background task management
background_tasks = {}

# Prometheus metrics
market_data_points_total = Counter(
    "market_data_points_total", "Total number of market data points"
)
symbols_tracked = Gauge("symbols_tracked", "Number of symbols being tracked")
polling_jobs_active = Gauge("polling_jobs_active", "Number of active polling jobs")

logger = logging.getLogger(__name__)


@router.get("/",response_model=List[MarketData])
async def get_market_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1,len=100),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_read_permission)
)-> List[MarketData]:
    """Fetch market data with optional symbol filtering."""
    try:
        if symbol:
            data = MarketDataService.get_market_data_by_symbol(db, symbol, skip, limit)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        


@router.post("/", response_model=MarketDataInDB, status_code=201)
async def create_market_data(
    market_data: MarketDataCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_write_permission)
)-> MarketDataInDB:
    """Create a new market data entry."""
    try:
        result = MarketDataService.create_market_data(db, market_data)

        #increment Prometheus counter
        market_data_points_total.inc()
        return result
    except (DataError,IntegrityError) as e:
        # Handle database constraint violations (e.g., symbol too long)
        raise HTTPException(status_code=422, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        if e.status_code == 422:
            raise HTTPException(status_code=422, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/latest")
async def get_latest_price(
    symbol: str = Query(..., description="Symbol to fetch latest price for"),
    provider: Optional[str] = Query(None, description="Optional provider filter"),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_read_permission)
):
    """Fetch the latest price for a given symbol."""
    try:
        latest_data = MarketDataService.get_lateste_price_static(db, symbol, skip=0, limit=1)
        if not latest_data:
            raise HTTPException(status_code=404, detail="Symbol not found")
        return {
            "symbol": latest_data[0].symbol,
            "price": latest_data[0].price,
            "timestamp": latest_data[0].timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as e:
        raise e


