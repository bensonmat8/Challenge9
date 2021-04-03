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
    
    d = DwellingCoverage.query.get(x)
    if d != None:
        return d.Rating_Factor
    
    if 100000 < x < 350000:
        fltr = between(DwellingCoverage.Dwelling_Coverage
                    , x-50000, x+50000)
        d = DwellingCoverage.query.filter(fltr)
    else:
        order_col = DwellingCoverage.Dwelling_Coverage
        d = DwellingCoverage.query.order_by(order_col).all()
    x0 = d[0].Dwelling_Coverage
    y0 = d[0].Rating_Factor
    x1 = d[-1].Dwelling_Coverage
    y1 = d[-1].Rating_Factor
    result = (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)
    return round(result, 3)

def home_age_rate(age):
    '''
    Takes the age, queries the 'tbl_Factor_Home_Age' table
    and returns the rating factor
    '''
    if 0 <= age <= 10:
        result = HomeAge.query.get('0-10')
    elif 11 <= age <= 35:
        result = HomeAge.query.get('11-35')
    elif 36 <= age <= 100:
        result = HomeAge.query.get('36-100')
    else:
        result = HomeAge.query.get('100+' )

    return result.Rating_Factor

def roof_type(roof):
    '''
    Takes the roof type, queries the 'tbl_Factor_Roof_Type' table
    and returns the rating factor
    '''
    result = Roof.query.get(roof)
    return result.Rating_Factor

def num_units(units):
    '''
    Takes the number of units, queries the 'tbl_Factor_Num_Units'
    table and returns the rating factor
    '''
    result = NumUnits.query.get(units)
    return result.Rating_Factor

def prem_quotes(j_text):
    '''
    Considers the base rate and all the other factors and
    returns the premium rate rounded to two decimals.
    '''
    j_dict = json.loads(j_text)
    base_amt = Base.query.first().Base_Premium

    dwelling_factor = dwelling_rate(j_dict['DwellingCoverage'])
    age_factor = home_age_rate(j_dict['HomeAge'])
    roof_factor = roof_type(j_dict['RoofType'])
    num_units_factor = num_units(j_dict['NumberOfUnits'])

    premium = base_amt * dwelling_factor * age_factor * roof_factor * num_units_factor

    if j_dict['PartnerDiscount'] == 'Y':
        premium = premium - (premium * 0.05)

    return round(premium,2)    

if __name__ == "__main__":
    test1 = {
        'CustomerID' : 1,
        'DwellingCoverage' : 100000,
        'HomeAge' : 5,
        'RoofType' : 'Asphalt Shingles',
        'NumberOfUnits' : 3,
        'PartnerDiscount' : 'Y'
    }

    test1 = json.dumps(test1, indent=4)
    print(f'Test 1:\n{test1}\n\nPremium: ${prem_quotes(test1)}')
    print('--------------------------')

    test2 = {
        'CustomerID' : 2,
        'DwellingCoverage' : 275000,
        'HomeAge' : 2,
        'RoofType' : 'Wood',
        'NumberOfUnits' : 1,
        'PartnerDiscount' : 'Y'
    }
    test2 = json.dumps(test2, indent=4)
    print(f'Test 2:\n{test2}\n\nPremium: ${prem_quotes(test2)}')
    print('------------------------')

    test3 = {
        'CustomerID' : 3,
        'DwellingCoverage' : 300200,
        'HomeAge' : 108,
        'RoofType' : 'Tin',
        'NumberOfUnits' : 4,
        'PartnerDiscount' : 'N'
    }

    test3 = json.dumps(test3, indent=4)
    print(f'Test 3:\n{test3}\n\nPremium: ${prem_quotes(test3)}')
    print('------------------------')
    print('\n\nFor further testing, call "prem_quotes" function on the test json string.')