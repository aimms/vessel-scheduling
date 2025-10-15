import searoute as sr
import pandas as pd
from typing import Tuple
from singleton import aimms_model, DataReturnTypes

def searoute_route(fromLat:float,fromLon:float,toLat:float,toLon:float):
    # fromLon = aimms_model.p_origLon.data()
    # fromLat = aimms_model.p_origLat.data()
    # toLon   = aimms_model.p_destLon.data()
    # toLat   = aimms_model.p_destLat.data() 
    origin=[fromLon,fromLat]
    destination=[toLon,toLat]
    route = sr.searoute(origin,destination)

    # Pass total travel length to AIMMS model
    route_length = route.properties["length"]
    aimms_model.p_totlen.assign(route_length)

    # Pass Waypoints to AIMMS model
    route_columns = ['p_wayLon','p_wayLat']
    route_df = pd.DataFrame(route.geometry.coordinates,columns=route_columns)
    route_len = len(route_df)
    aimms_model.p_nowaypoints.assign(route_len)
    
    # add column i_wayno
    route_df['i_wayno']=route_df.index
    # reorder columns, making i_wayno first.
    route_columns=route_df.columns.tolist()
    route_columns=route_columns[-1:]+route_columns[:-1]
    route_df=route_df[route_columns]
    # and copying data to AIMMS.
    aimms_model.multi_assign(route_df,options={"return_type": DataReturnTypes.PANDAS})

def test_scalar(parName:str):
    df = pd.DataFrame({parName:[1234.5678]})
    aimms_model.multi_assign(df,options={"return_type": DataReturnTypes.PANDAS})

def searoute_route2(fromLat:float,fromLon:float,toLat:float,toLon:float,
    indexName:str,latParName:str,lonParName:str,lenParName:str):
    # fromLon = aimms_model.p_origLon.data()
    # fromLat = aimms_model.p_origLat.data()
    # toLon   = aimms_model.p_destLon.data()
    # toLat   = aimms_model.p_destLat.data() 
    origin=[fromLon,fromLat]
    destination=[toLon,toLat]
    route = sr.searoute(origin,destination)

    # Pass total travel length to AIMMS model
    route_length = route.properties["length"]
    route_length_df = pd.DataFrame({lenParName:[route_length]})
    aimms_model.multi_assign(route_length_df,options={"return_type": DataReturnTypes.PANDAS})

    # Pass Waypoints to AIMMS model
    route_columns = [lonParName,latParName]
    route_df = pd.DataFrame(route.geometry.coordinates,columns=route_columns)
    route_len = len(route_df)
    # aimms_model.p_nowaypoints.assign(route_len) # test if needed.
    
    # add column i_wayno
    route_df[indexName]=route_df.index
    # reorder columns, making i_wayno first.
    route_columns=route_df.columns.tolist()
    route_columns=route_columns[-1:]+route_columns[:-1]
    route_df=route_df[route_columns]
    # and copying data to AIMMS.
    aimms_model.multi_assign(route_df,options={"return_type": DataReturnTypes.PANDAS})
    



def searoute_distance_matrix():
    # Getting data from AIMMS model:
    distance_mat_list = []
    df_location_overview = aimms_model.multi_data(["i_loc","p_latitude","p_longitude"])
    location_overview_no_rows = len( df_location_overview )
    for from_pos in range(location_overview_no_rows):
        for to_pos in range(from_pos+1,location_overview_no_rows):
            from_location_row = df_location_overview.iloc[from_pos]
            to_location_row   = df_location_overview.iloc[  to_pos]
            fromLoc =  from_location_row['i_loc']
            fromLon =  from_location_row['p_longitude']
            fromLat =  from_location_row['p_latitude']
            toLoc   =  to_location_row['i_loc']
            toLon   =  to_location_row['p_longitude']
            toLat   =  to_location_row['p_latitude']
            origin=[fromLon,fromLat]
            destination=[toLon,toLat]
            route = sr.searoute(origin,destination)
            route_length = route.properties["length"]
            route_tuple = (fromLoc, toLoc, route_length)
            distance_mat_list.append( route_tuple )

    distance_columns = ['i_loc_from','i_loc_to','p_distance_searoute']
    distance_df = pd.DataFrame(distance_mat_list,columns=distance_columns)
    aimms_model.p_distance_searoute.assign(distance_df)
