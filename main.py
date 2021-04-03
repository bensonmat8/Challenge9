# CreateTempDB just creates temporary database, for production
# this will be bringing required tables from prod database
# as SQLAlchemy table class
from CreateTempDB import * 
import json
from sqlalchemy import between

def dwelling_rate(x) -> float:
    '''
    Takes the DewellingCoverage value and looks up
    the rating factor from the tbl_Factor_Dwelling_Coverage
    table. If there is no perfect match, do a linear interpolation
    of the closest rating factor.
    Result will be rounded to three decimal places
    '''
    if x < 0:
        raise ValueError("Dwelling_Coverage cannot be negative")
    
    d = Dwelling_Coverage.query.get(x)
    if d != None:
        return d.Rating_Factor
    
    if 100000 < x < 350000:
        fltr = between(Dwelling_Coverage.Dwelling_Coverage
                    , x-50000, x+50000)
        d = Dwelling_Coverage.query.filter(fltr)
    else:
        order_col = Dwelling_Coverage.Dwelling_Coverage
        d = Dwelling_Coverage.query.order_by(order_col).all()
    x0 = d[0].Dwelling_Coverage
    y0 = d[0].Rating_Factor
    x1 = d[-1].Dwelling_Coverage
    y1 = d[-1].Rating_Factor
    result = (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)
    return round(result, 3)

def prem_quotes(j_text):
    j_dict = json.loads(j_text)
    dwelling_factor = dwelling_rate(j_dict['DwellingCoverage'])
    
    
    

if __name__ == "__main__":
    test1 = {
        'CustomerID' : 1,
        'DwellingCoverage' : 100000,
        'HomeAge' : 5,
        'RoofType' : 'Asphalt Shingles',
        'NumberOfUnits' : 3,
        'PartnerDiscount' : 'Y'
    }

    test1_json = json.dumps(test1)