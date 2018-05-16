# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sqlalchemy as sa 
import pandas as pd 
from sqlalchemy import create_engine
import 

#engine = create_engine("mssql+pyodbc://GDXMG_GW:GDXMG_GW@192.168.1.101/HTTPDB")
#df = pd.read_sql('T_GP_RNLZZB',engine)
#print df.info()