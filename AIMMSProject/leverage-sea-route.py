import searoute as sr
import pandas as pd
from typing import Tuple
from singleton import aimms_model, DataReturnTypes

def searoute_work():
    fromLon = aimms_model.p_origLon.data()
    fromLat = aimms_model.p_origLat.data()
    toLon   = aimms_model.p_destLon.data()
    toLat   = aimms_model.p_destLat.data() 
    origin=[fromLon,fromLat]
    destination=[toLon,toLat]
    route = sr.searoute(origin,destination)

    # Pass total travel length to AIMMS model
    route_length = route.properties["length"]
    aimms_model.p_totlen.assign(route_length)

    # Pass Waypoints to AIMMS model
    route_columns = ['p_wayLon','p_wayLat']
    route_df = pd.DataFrame(route.geometry.coordinates,columns=route_columns)
    # add column i_wayno
    route_df['i_wayno']=route_df.index
    # reorder columns, making i_wayno first.
    route_columns=route_df.columns.tolist()
    route_columns=route_columns[-1:]+route_columns[:-1]
    route_df=route_df[route_columns]
    # and copying data to AIMMS.
    aimms_model.multi_assign(route_df,options={"return_type": DataReturnTypes.PANDAS})

