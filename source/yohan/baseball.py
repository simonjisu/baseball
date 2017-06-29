import urllib
import json
import datetime as dt
import time
import sys
import config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

# 환경설정
MATCH_URL = "http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date="
CAST_URL = "http://data.cast.sports.media.daum.net/bs/kbo/"

# DB 환경설정
DB_TYPE = config.DB_TYPE
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_URL = config.DB_URL
DB_PORT = config.DB_PORT
DB_NAME = config.DB_NAME
QUERY_ECHO = config.QUERY_ECHO

Base = declarative_base()

"""
설명 : 어제 날짜로 부터 며칠 동안의 경기 데이터를 가져올 것인지
"""
def date_count(interval = 1):
    date_list = []
    for i in range(interval):
        yesterday = dt.datetime.now() - dt.timedelta(days=i+1)
        date_list.append(yesterday.strftime('%Y%m%d'))
        
    return date_list

def get_game_id():
	castlist_id = []
	for i in range(len(highlist_json)):
	    castlist_id.append(highlist_json[i]['cp_game_id'])

	return castlist_id

def db_conn():
	engine = sqlalchemy.create_engine(DB_TYPE + DB_USER + ":" + DB_PASSWORD + "@" + DB_URL + ":" + DB_PORT + "/" + DB_NAME, echo=QUERY_ECHO)
	engine.connect()

# DB Table (class) 활성화

class Livetext(Base):
    __tablename__ = 'livetext'

    id = Column(Integer, primary_key=True)
    batorder = Column(String)
    batter = Column(String)
    btop = Column(String)
    inning = Column(String)
    pitcher = Column(String)
    text = Column(String)
    textstyle = Column(String)

class Team(Base):
    __tablename__ = 'team'
    tcode = Column(String, primary_key=True)
    
class Team_season(Base):
    __tablename__ = 'team_season'
    idx = Column(Integer, primary_key=True)
    ab = Column(Float)
    bb = Column(Float)
    bra = Column(Float)
    dra = Column(Float)
    er = Column(Float)
    
    era = Column(Float)
    err = Column(Float)
    game = Column(Float)
    h2 = Column(Float)
    h3 = Column(Float)
    
    hit = Column(Float)
    hp = Column(Float)
    hr = Column(Float)
    hra = Column(Float)
    lose = Column(Float)
    
    lra = Column(Float)
    r = Column(Float)
    rank = Column(Float)
    run = Column(Float)
    same = Column(Float)
    
    sb = Column(Float)
    sf = Column(Float)
    win = Column(Float)
    wra = Column(Float)
    
    dates = Column(DateTime)
    f_name = Column(String)
    tcode = Column(String, ForeignKey('team.tcode'))
    

class Player(Base):
    __tablename__ = 'player'
    player_id = Column(Integer, primary_key=True)
    tcode = Column(String, ForeignKey('team.tcode'))
    
class Player_profile(Base):
    __tablename__ = 'player_profile'
    profile_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    backnum = Column(Integer)
    bat = Column(String)
    height = Column(Integer)
    name = Column(String)
    position = Column(String)
    throw = Column(String)
    weight = Column(Integer)
    dates = Column(DateTime)
    
class Pitcher_stats(Base):
    __tablename__ = 'pitcher_stats'
    pitcher_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('player_profile.profile_id'))
    s_era = Column(Float)
    s_gyear = Column(Float)
    s_hit = Column(Float)
    s_hld = Column(Float)
    s_hr = Column(Float)
    s_kk = Column(Float)
    s_lose = Column(Float)
    s_save = Column(Float)
    s_total_era = Column(Float)
    s_win = Column(Float)
    t_b = Column(Float)
    t_bb = Column(Float)
    t_er = Column(Float)
    t_era = Column(Float)
    t_hbp = Column(Float)
    t_hit = Column(Float)
    t_hr = Column(Float)
    t_ip = Column(Float)
    t_np = Column(Float)
    t_r = Column(Float)
    t_s = Column(Float)
    t_so = Column(Float)
    
class Batter_stats(Base):
    __tablename__ = 'batter_stats'
    batter_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('player_profile.profile_id'))
    h_1 = Column(Float)
    h_2 = Column(Float)
    h_3 = Column(Float)
    h_4 = Column(Float)
    h_5 = Column(Float)
    h_6 = Column(Float)
    h_7 = Column(Float)
    h_8 = Column(Float)
    h_9 = Column(Float)
    h_10 = Column(Float)
    h_11 = Column(Float)
    h_12 = Column(Float)
    h_13 = Column(Float)
    s_ab = Column(Float)
    s_avg = Column(Float)
    s_bbhp = Column(Float)
    s_cs = Column(Float)
    s_game = Column(Float)
    s_h2 = Column(Float)
    s_h3 = Column(Float)
    s_hit = Column(Float)
    s_hr = Column(Float)
    s_kk = Column(Float)
    s_rbi = Column(Float)
    s_run = Column(Float)
    s_sb = Column(Float)
    s_shf = Column(Float)
    t_ab = Column(Float)
    t_avg = Column(Float)
    t_bb = Column(Float)
    t_bbhp = Column(Float)
    t_h = Column(Float)
    t_hr = Column(Float)
    t_pa = Column(Float)
    t_r = Column(Float)
    t_rbi = Column(Float)
    t_sb = Column(Float)
    t_so = Column(Float)

#db_conn()

#Base.metadata.create_all(engine)



interval = str(sys.argv)
MATCH_URL += date_count()[0]
print(MATCH_URL)
print(DB_TYPE + DB_USER + ":" + DB_PASSWORD + "@" + DB_URL + ":" + DB_PORT + "/" + DB_NAME)




#highlist_json = json.load(urllib.urlopen(MATCH_URL))