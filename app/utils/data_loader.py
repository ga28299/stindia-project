import pandas as pd
from db import get_db, Base, engine
from models import *

# CSV file path
csv_file = '../../data/updated.csv'


def create_tables():
    """Creates the database tables if they don't exist."""
    Base.metadata.create_all(engine)

def populate_initial_data(csv_file):
    """Prefills the Industry and Location tables from the CSV data."""
    df = pd.read_csv(csv_file)

    unique_industries = df['Industry'].unique()
    print(unique_industries)
    unique_locations = df[['Pitchers City', 'Pitchers State']].drop_duplicates()

    with get_db() as db:
        for industry_name in unique_industries:
            industry = Industry(industry_name=industry_name)
            db.add(industry)

        for _, location_data in unique_locations.iterrows():
            city = location_data['Pitchers City']
            state = location_data['Pitchers State']

            if pd.isna(city):
                city = None
            if pd.isna(state):
                state = None

            location = Location(city=city, state=state)
            db.add(location)

        for shark in ['Namita', 'Vineeta', 'Anupam', 'Aman', 'Peyush', 'Amit',
                              'Ashneer', 'Ghazal', 'Ronnie', 'Ritesh', 'Deepinder', 'Azhar',
                              'Vikas', 'Radhika', 'Varun']:
            shark = Shark(shark_name=shark)
            db.add(shark)

        db.commit()

def load_data(csv_file):
        
    df = pd.read_csv(csv_file)

    pitches = []
    deals_to_create = []
    with get_db() as db:
        for index, row in df.iterrows():

                city='Unknown' if pd.isna(row['Pitchers City']) else row['Pitchers City']
                state='Unknown' if pd.isna(row['Pitchers State']) else row['Pitchers State']

                pitch = Pitch(
                    company_name=row['Startup Name'],
                    season_id=row['Season Number'],
                    industry_id=db.query(Industry).filter_by(industry_name=row['Industry']).first().industry_id,  # Find matching industry
                    location_id= db.query(Location).filter_by(city=city, state=state).first().location_id,
                    description=row['Business Description'],
                    ask_amount=row['Original Ask Amount'],
                    equity_asked=row['Original Offered Equity'],
                    yearly_revenue=row['Yearly Revenue'],
                    monthly_revenue=row['Monthly Sales'],
                    gross_margin=row['Gross Margin'],
                    net_margin=row['Net Margin'],
                    ebitda=row['EBITDA'],
                    cash_burn=row['Cash Burn'] == 'True',
                    sku=row['SKUs'],
                    bootstrapped=pd.notna(row['Bootstrapped']) and str(row['Bootstrapped']).lower() == 'yes',
                    has_patent=pd.notna(row['Has Patents']) and str(row['Has Patents']).lower() == 'yes',
                    got_offer=row['Received Offer'] == 1,
                    accept_offer=row['Accepted Offer'] == 1,
                    site=row['Company Website']
                )
                
                db.add(pitch)
                pitches.append((pitch,row))
        db.commit()

        for pitch, row in pitches:
            if pitch.accept_offer:
                condition = row['Deal Has Conditions'] == 1
                royalty = row['Royalty Deal'] == 1

                for shark in ['Namita', 'Vineeta', 'Anupam', 'Aman', 'Peyush', 'Amit',
                            'Ashneer', 'Ghazal', 'Ronnie', 'Ritesh', 'Deepinder', 'Azhar',
                            'Vikas', 'Radhika', 'Varun']:
                    investment_amount = row.get(f'{shark} Investment Amount')
                    if pd.notna(investment_amount) and investment_amount > 0:
                        shark_obj = db.query(Shark).filter_by(shark_name=shark).first()

                        deal = DealFact(
                            pitch_id=pitch.pitch_id,
                            shark_id=shark_obj.shark_id,
                            amount_invested=investment_amount,
                            equity_acquired=row.get(f'{shark} Investment Equity'),  
                            condition=condition,
                            royalty=royalty,
                            debt_amount=row.get(f'{shark} Debt Amount'),  
                            advisory_share=row['Advisory Shares Equity']  
                        )
                        deals_to_create.append(deal)

        for deal in deals_to_create:
                db.add(deal)
        db.commit() 

# create_tables()
# populate_initial_data(csv_file)
load_data(csv_file)