
class MarketDataService:
    def __init__(self,db:Session):
        """Initialize MarketDataService with database session."""
        self.db = db
        self.redis_service = RedisService()
        

    def get_market_data(
            self,
            db:Session,
            skip: int = 0,
            limit: int = 100
            ):
        # Placeholder for fetching market data logic
        return db.query(MarketData).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_market_data_by_symbol(
        db: Session, 
        symbol: str,
        skip: int = 0,,
        limit: int = 100)-> List[MarketData]:
        """Fetch market data for a specific symbol."""
        return (
            db.query(MarketData)
            .filter(MarketData.symbol == symbol)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def create_market_data(
        db: Session, 
        market_data: MarketDataCreate
        ) -> MarketData:
        """Create a new market data entry."""
        db_market_data = MarketData(**market_data.model_dump())
        db.add(db_market_data)
        db.commit()
        db.refresh(db_market_data)
        return db_market_data

