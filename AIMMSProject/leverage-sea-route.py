import searoute as sr
import pandas as pd
from typing import Tuple, List, Dict
from singleton import aimms_model, DataReturnTypes 

def searoute_route(fromLat: float, fromLon: float, toLat: float, toLon: float):
    """Calculates sea route, length, and waypoints; assigns results to specific AIMMS parameters."""
    
    origin = [fromLon, fromLat]
    destination = [toLon, toLat]
    route = sr.searoute(origin, destination)

    # --- Assign Total Length to AIMMS (p_totlen) ---
    route_length = route.properties["length"]
    aimms_model.p_totlen.assign(route_length)

    # --- Assign Waypoints to AIMMS (p_wayLon, p_wayLat) ---
    route_columns = ['p_wayLon', 'p_wayLat']
    route_df = pd.DataFrame(route.geometry.coordinates, columns=route_columns)
    
    # Assign total number of waypoints to AIMMS scalar.
    aimms_model.p_nowaypoints.assign(len(route_df))
    
    # Add index column ('i_wayno') for AIMMS set/index.
    route_df['i_wayno'] = route_df.index
    
    # Reorder columns: Index column ('i_wayno') must be first for AIMMS assignment.
    route_columns = route_df.columns.tolist()
    route_df = route_df[route_columns[-1:] + route_columns[:-1]]
    
    # Assign waypoints DataFrame to AIMMS.
    aimms_model.multi_assign(route_df, options={"return_type": DataReturnTypes.PANDAS})


def test_scalar(parName: str):
    """Assigns a test scalar value (1234.5678) to the specified AIMMS parameter."""
    df = pd.DataFrame({parName: [1234.5678]})
    aimms_model.multi_assign(df, options={"return_type": DataReturnTypes.PANDAS})


def searoute_route2(fromLat: float, fromLon: float, toLat: float, toLon: float,
                    indexName: str, latParName: str, lonParName: str, lenParName: str):
    """Calculates sea route and assigns results to dynamically named AIMMS parameters."""

    origin = [fromLon, fromLat]
    destination = [toLon, toLat]
    route = sr.searoute(origin, destination)

    # --- Assign Dynamic Length Parameter ---
    route_length = route.properties["length"]
    route_length_df = pd.DataFrame({lenParName: [route_length]})
    aimms_model.multi_assign(route_length_df, options={"return_type": DataReturnTypes.PANDAS})

    # --- Assign Dynamic Waypoint Parameters ---
    route_columns = [lonParName, latParName]
    route_df = pd.DataFrame(route.geometry.coordinates, columns=route_columns)
    
    # Add dynamic index column.
    route_df[indexName] = route_df.index
    
    # Reorder columns: Index column must be first.
    route_columns = route_df.columns.tolist()
    route_df = route_df[route_columns[-1:] + route_columns[:-1]]
    
    # Assign waypoints DataFrame to AIMMS.
    aimms_model.multi_assign(route_df, options={"return_type": DataReturnTypes.PANDAS})


def searoute_distance_matrix():
    """Calculates a distance matrix for all locations retrieved from AIMMS and assigns it back."""
    
    # Step 1: Retrieve location data from the AIMMS model
    # Gets location index ('i_loc'), latitude, and longitude for all known locations.
    df_location_overview = aimms_model.multi_data(["i_loc","p_latitude","p_longitude"])
    distance_mat_list = []
    
    location_overview_no_rows = len( df_location_overview )
    
    # Iterate over unique pairs (from_pos < to_pos) to calculate the distance matrix (upper triangle).
    for from_pos in range(location_overview_no_rows):
        for to_pos in range(from_pos+1,location_overview_no_rows):
            from_location_row = df_location_overview.iloc[from_pos]
            to_location_row   = df_location_overview.iloc[to_pos]
            
            fromLoc = from_location_row['i_loc']
            fromLon = from_location_row['p_longitude']
            fromLat = from_location_row['p_latitude']
            toLoc  = to_location_row['i_loc']
            toLon  = to_location_row['p_longitude']
            toLat  = to_location_row['p_latitude']
            
            # Calculate distance using searoute.
            origin=[fromLon,fromLat]
            destination=[toLon,toLat]
            route = sr.searoute(origin,destination)
            route_length = route.properties["length"]
            
            # Append result: (from_index, to_index, distance)
            route_tuple = (fromLoc, toLoc, route_length)
            distance_mat_list.append( route_tuple )

    # Step 2: Build a DataFrame with the calculated distances
    # Structure columns to match the AIMMS 2D parameter: indices first, then the value.
    distance_columns = ['i_loc_from','i_loc_to','p_distance_searoute']
    distance_df = pd.DataFrame(distance_mat_list,columns=distance_columns)

    # Step 3: Pass the DataFrame back to the AIMMS model
    # Assigns the distance matrix to the parameter 'p_distance_searoute'.
    aimms_model.p_distance_searoute.assign(distance_df)