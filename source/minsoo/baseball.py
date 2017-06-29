
import datetime as dt
import urlparse
import urllib
import json

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

Base = declarative_base()


"""
datatime 사용해서 url 출력하기
"""
urls = "http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date="

def date_count(interval = 1):
    date_list = []

    for i in range(interval):
        yesterday = dt.datetime.now() - dt.timedelta(days=i+1)
        date_list.append(yesterday.strftime('%Y%m%d'))

    return date_list

urls = urls + date_count(5)[1]


"""
json file 다운로드 및 변수에 저장하기
"""
raw_json = urllib.urlopen(urls)
loaded_json = json.load(raw_json)


"""
'cp_game_id' 리스트 만들어서 받기
"""
castlist_id=[]
for i in range(len(highlight_json)):
    castlist_id.append(highlight_json[i]['cp_game_id'])

cast_url1 = 'http://data.cast.sports.media.daum.net/bs/kbo/'
cast_url = cast_url1 + castlist_id[0]
raw_cast_json = urllib.urlopen(cast_url)
cast_json = json.load(raw_cast_json)


"""
DBMS 설치하기
"""
engine = sqlalchemy.create_engine('postgresql://postgres:1234@127.0.0.1:5432/baseball')
engine.connect()


"""
livetext에 테이블 만들고 데이터 넣기
"""
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

        def __repr__(self):
            return "Done"

Base.metadata.create_all(engine)

texts = []

for i in range(len(cast_json['livetext'])):
    txt = cast_json['livetext'][i]  # 코드가 너무 길어져서
    texts.append(Livetext(batorder=txt['batorder'], batter=txt['batter'], btop=txt['btop'], inning=txt['inning'], pitcher=txt['pitcher'], text=txt['text'], textstyle=txt['textstyle']))

Session = sessionmaker()
Session.configure(bind=engine) # once engine is available
session = Session()
session.add_all(texts)
session.commit()


"""
테이블 만들기
"""
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

Base.metadata.create_all(engine)


"""
team 테이블에 데이터 추가하기
"""
team_key_list = cast_json['registry']['team'].keys()

team_list = []
for i in team_key_list:
    if 'season' in cast_json['registry']['team'][i].keys() :
        team_list.append(i)

texts = []
for i in range(len(team_list)):
    texts.append(Team(tcode=team_list[i]))

Session = sessionmaker()
Session.configure(bind=engine) # once engine is available
session = Session()
session.add_all(texts)
session.commit()

"""
team_season에 데이터 추가하기
"""
