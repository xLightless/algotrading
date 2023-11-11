from dataclasses import dataclass
from typing import Optional
import datetime

from .enums import *

"""

This module contains all the request objects to send to the api (if applicable).
Not all API requests contain a dataclass object but a response will typically contain a generator of a record.

For example:

- REQUEST:
{
	"command": "getChartRangeRequest",
	"arguments": {
		"info": CHART_RANGE_INFO_RECORD
	}
}

- RESPONSE:
{
	"status": true,
	"returnData": {
		"digits": 4,
		"rateInfos": [RATE_INFO_RECORD, RATE_INFO_RECORD, ...]
	}	
}


"""

@dataclass
class ChartLastInfoRecord:
    period: PeriodCode # Period code
    start: Optional[datetime.datetime] # Start of chart block (rounded down to the nearest interval and excluding)
    symbol: str
    
@dataclass
class ChartRangeInfoRecord:
    end: Optional[datetime.datetime] # End of chart block (rounded down to the nearest interval and excluding)
    period: PeriodCode # Period code
    start: Optional[datetime.datetime] # Start of chart block (rounded down to the nearest interval and excluding)
    symbol: str # Symbol
    ticks: Optional[int] # Number of ticks needed, this field is optional, please read the description above


@dataclass
class TradeTransInfo:
    cmd: TradeCmd # Operation code
    customComment: str # The value the customer may provide in order to retrieve it later.
    expiration: datetime.datetime # Pending order expiration time
    offset: int # Trailing offset
    order: int # 0 or position number for closing/modifications
    price: float # Trade price
    sl: float # Stop loss
    symbol: str # Trade symbol
    tp: float # Take profit
    type: TradeType # Trade transaction type
    volume: float # Trade volume
    
    
@dataclass
class StepRecord:
    fromValue: float # Lower border of the volume range
    step: float # lotStep value in the given volume range