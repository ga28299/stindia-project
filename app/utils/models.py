from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base=declarative_base()

class DealFact(Base):
    __tablename__ = 'deal_fact'

    deal_id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    pitch_id = Column(UUID(as_uuid=True), ForeignKey('pitch.pitch_id'))
    shark_id = Column(UUID(as_uuid=True), ForeignKey('shark.shark_id'))
    amount_invested = Column(Numeric)
    equity_acquired = Column(Numeric)
    condition = Column(Boolean)
    debt_amount = Column(Numeric)
    royalty = Column(Boolean)
    advisory_share = Column(Numeric)

    pitch = relationship("Pitch", back_populates="deals")
    shark = relationship("Shark", back_populates="deals")



class Pitch(Base):
    __tablename__ = 'pitch'
    
    pitch_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )
    season_id = Column(Numeric)
    company_name = Column(String)
    industry_id = Column(UUID(as_uuid=True), ForeignKey('industry.industry_id'),default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey('location.location_id'),default=uuid.uuid4)
    description = Column(Text)
    ask_amount = Column(Numeric)
    equity_asked = Column(Numeric)
    yearly_revenue = Column(Numeric)
    monthly_revenue = Column(Numeric)
    gross_margin = Column(Numeric)
    net_margin = Column(Numeric)
    bootstrapped = Column(Boolean)
    ebitda = Column(Numeric)
    cash_burn = Column(Boolean)
    has_patent = Column(Boolean)
    sku = Column(Numeric)
    got_offer = Column(Boolean)
    accept_offer = Column(Boolean)
    site = Column(Text)
    
    location = relationship("Location", back_populates="pitches")
    industry = relationship("Industry", back_populates="pitches")
    deals = relationship("DealFact", back_populates="pitch")


class Location(Base):
    __tablename__ = 'location'
    
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(Text)
    state = Column(Text)
    
    pitches = relationship("Pitch", back_populates="location")

class Industry(Base):
    __tablename__ = 'industry'
    
    industry_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    industry_name = Column(Text)
    
    pitches = relationship("Pitch", back_populates="industry")

class Shark(Base):
    __tablename__ = 'shark'
    
    shark_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shark_name = Column(Text)

    deals = relationship("DealFact", back_populates="shark")