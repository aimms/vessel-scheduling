# This is a sample Python script.
# The purpose of this script is to demo the aimmspy Python bridge,
# see https://pypi.org/project/aimmspy/

import time
import pandas as pd
import datetime
import os
import pathlib
import sys

# , DataReturnTypes
from aimmspy.project.project import DataReturnTypes, Project, AimmsException, AimmsPyException, Model
from aimmspy.utils import find_aimms_path


# # Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
# os.chdir(script_dir)
now = datetime.datetime.now()
cwd = os.getcwd()
 

projectroot=script_dir.replace("\\python-bridge","") 

# Initialize required paths.
print(f"Start: {now} cwd: {cwd}")


# Initialize the AIMMS project
project = Project(
    # path to the AIMMS Bin folder (on linux the Lib folder)
    aimms_path=find_aimms_path("25.4"),

    # path to the AIMMS project file
    aimms_project_file="..\\AIMMSProject\\VesselScheduling.aimms",

    # the name of an aimms set containing identifiers. 
    exposed_identifier_set_name="AllIdentifiers",  # Limit access to specific identifiers,

    # default data type when retrieving multi-dimensional data
    data_type_preference=DataReturnTypes.PANDAS,
)
my_aimms : Model = project.get_model(__file__)

# Determine the input file.
datainput=projectroot+"\\AIMMSProject\\data\\VS_5Vessel_15Cargo.xlsx"
datainput_path = pathlib.Path(datainput)
if not datainput_path.exists():
    print(f"File {datainput} does not exist.")
    sys.exit()

# The horizon defines the start date for planning.
datainput_pd_horizon = pd.read_excel(datainput,sheet_name='Horizon')
ep_startHorizonDate = datainput_pd_horizon.loc[0,'StartDate']
my_aimms.ep_startHorizonDate = datainput_pd_horizon.loc[0,'StartDate']


# Get the location data from the LocationData sheet and 
# copy it over to the AIMMS project, parameters p_latitude, and p_longitude.
# Read Excel sheet:
datainput_pd_location = pd.read_excel(datainput,sheet_name='LocationData')
# Split it into multiple dataframes:
# df_lat   = datainput_pd_location[['Location','Latitude']].copy()
# df_lon   = datainput_pd_location[['Location','Longitude']].copy()
# df_idle  = datainput_pd_location[['Location','Idle Cost']].copy()
# df_admin = datainput_pd_location[['Location','Admin Cost']].copy()
# df_load  = datainput_pd_location[['Location','Loading Cost']].copy()
# # Rename the columns to AIMMS identifiers:
datainput_pd_location.rename(columns={         \
    'Location'     : 'i_loc',                  \
    'Latitude'     : 'p_latitude',             \
    'Longitude'    : 'p_longitude',            \
    'Idle Cost'    : 'p_idleCostLocation',     \
    'Admin Cost'   : 'p_adminCostAtLocation',  \
    'Loading Cost' : 'p_loadingCostAtLocation' \
    }, inplace=True)
# df_lat.rename(columns={'Location':'i_loc','Latitude':'p_latitude'},inplace=True)
# df_lon.rename(columns={'Location':'i_loc','Longitude':'p_longitude'},inplace=True)
# df_idle.rename(columns={'Location':'i_loc','Idle Cost':'p_idleCostLocation'},inplace=True)
# df_admin.rename(columns={'Location':'i_loc','Admin Cost':'p_adminCostAtLocation'},inplace=True)
# df_load.rename(columns={'Location':'i_loc','Loading Cost':'p_loadingCostAtLocation'},inplace=True)
# # Actually assign to AIMMS identifiers:
# my_aimms.p_latitude.assign(df_lat)
# my_aimms.p_longitude.assign(df_lon)
# my_aimms.p_idleCostLocation.assign(df_idle)
# my_aimms.p_adminCostAtLocation.assign(df_admin)
# my_aimms.p_loadingCostAtLocation.assign(df_load)
my_aimms.multi_assign(datainput_pd_location)

# Get the cargo data and copy it over to the AIMMS model:
# Read Excel sheet:
datainput_pd_cargo=pd.read_excel(datainput,sheet_name='CargoData')
# Split it into multiple dataframes:
# df_LoadingPort=datainput_pd_cargo[['Cargo','Loading Port']].copy()
# df_DeleveringPort=datainput_pd_cargo[['Cargo','Delevering Port']].copy()
# df_SpotCost=datainput_pd_cargo[['Cargo','Spot Cost']].copy()
# df_MinimumLoadingTime=datainput_pd_cargo[['Cargo','Minimum Loading Time']].copy()
# df_MaximumLoadingTime=datainput_pd_cargo[['Cargo','Maximum Loading Time']].copy()
# df_FixedCost=datainput_pd_cargo[['Cargo','Fixed Cost']].copy()
# # Rename the columns to AIMMS identifiers:
datainput_pd_cargo.rename(columns={                     \
    'Cargo'                : 'i_cargo',                 \
    'Loading Port'         : 'sp_loadingPortsCargo',    \
    'Delevering Port'      : 'sp_deliveringPortsCargo', \
    'Spot Cost'            : 'p_spotCostVessel',        \
    'Minimum Loading Time' : 'ep_minTimeWindow',        \
    'Maximum Loading Time' : 'ep_maxTimeWindow',        \
    'Fixed Cost'           : 'p_cargoCost'              \
    }, inplace=True)
print(datainput_pd_cargo)
# df_LoadingPort.rename(columns={'Cargo':'i_cargo','Loading Port':'ep_loadingPortsCargo'},inplace=True)
# df_DeleveringPort.rename(columns={'Cargo':'i_cargo','Delevering Port':'ep_deliveringPortsCargo'},inplace=True)
# df_SpotCost.rename(columns={'Cargo':'i_cargo','Spot Cost':'p_spotCostVessel'},inplace=True)
# df_MinimumLoadingTime.rename(columns={'Cargo':'i_cargo','Minimum Loading Time':'ep_minTimeWindow'},inplace=True)
# df_MaximumLoadingTime.rename(columns={'Cargo':'i_cargo','Maximum Loading Time':'ep_maxTimeWindow'},inplace=True)
# df_FixedCost.rename(columns={'Cargo':'i_cargo','Fixed Cost':'p_cargoCost'},inplace=True)
# # Actually assign to AIMMS identifiers:
# my_aimms.ep_loadingPortsCargo.assign(df_LoadingPort)
# my_aimms.ep_deliveringPortsCargo.assign(df_DeleveringPort)
# my_aimms.p_spotCostVessel.assign(df_SpotCost)
# my_aimms.ep_minTimeWindow.assign(df_MinimumLoadingTime)
# my_aimms.ep_maxTimeWindow.assign(df_MaximumLoadingTime)
# my_aimms.p_cargoCost.assign(df_FixedCost)
my_aimms.multi_assign(datainput_pd_cargo)


# Get the vessel data and copy it over to the AIMMS model:
# Read Excel sheet:
datainput_pd_vessel=pd.read_excel(datainput,sheet_name='VesselData')
# Split it into multiple dataframes:
# df_PortOfOrigin=datainput_pd_vessel[['Vessel','Port of Origin']].copy()
# df_SailingCost=datainput_pd_vessel[['Vessel','Sailing Cost']].copy()
# # Rename the columns to AIMMS identifiers:
datainput_pd_vessel.rename(columns={              \
    'Vessel'         : 'i_vessel',                \
    'Port of Origin' : 'ep_originPortOfVessel',   \
    'Sailing Cost'   : 'p_sailingCost'            \
    }, inplace=True)
# df_PortOfOrigin.rename(columns={'Vessel':'i_vessel','Port of Origin':'ep_originPortOfVessel'},inplace=True)
# df_SailingCost.rename(columns={'Vessel':'i_vessel','Sailing Cost':'p_sailingCost'},inplace=True)
# my_aimms.ep_originPortOfVessel.assign(df_PortOfOrigin)
# my_aimms.p_sailingCost.assign(df_SailingCost)
my_aimms.multi_assign(datainput_pd_vessel)


my_aimms.pr_processPythonInput()

# Running the AIMMS model, EchoInput and EchoOutput are only for debugging purposes.
my_aimms.pr_EchoInput()
my_aimms.pr_GenRoutesSolve()
my_aimms.pr_EchoOutput()

# Retrieving the Vessel overview:
# Getting data from AIMMS model:
df_vessel_overview_route  = my_aimms.mm.ep_calc_routeOfVessel.data()
df_vessel_overview_opcost = my_aimms.mm.p_calc_operationalCostPerVessel.data()
df_vessel_overview_travel = my_aimms.mm.p_calc_totalTravelDaysPerVessel.data()
# Merge the Vessel overview dataframes:
df_vessel_overview_temp=pd.merge(df_vessel_overview_route,df_vessel_overview_opcost, on='i_vessel', how='inner')
df_vessel_overview=pd.merge(df_vessel_overview_temp, df_vessel_overview_travel, on='i_vessel', how='inner')
# Renaming columns Vessel overview for Excel Sheet:
df_vessel_overview.rename(columns={
    'i_vessel':'Vessel',
    'mm::ep_calc_routeOfVessel':'Route',
    'mm::p_calc_operationalCostPerVessel':'Route Cost',
    'mm::p_calc_totalTravelDaysPerVessel':'Route Period'
    },inplace=True)


# Retrieving the Cargo overview:
# Getting data from AIMMS model:
df_cargo_overview_vessel_used    = my_aimms.mm.ep_calc_vesselOfCargo.data()
df_cargo_overview_cargo_cost     = my_aimms.mm.p_calc_totalCostPerCargo.data()
df_cargo_overview_loading_time   = my_aimms.mm.sp_calc_loadingTimePerCargo.data()
df_cargo_overview_delivery_time  = my_aimms.mm.sp_calc_deleveringTimePerCargo.data()
# Merge the Cargo overview dataframes:
df_cargo_overview_temp1 = pd.merge( df_cargo_overview_vessel_used, df_cargo_overview_cargo_cost, on='i_act_cargo', how='inner')
df_cargo_overview_temp2 = pd.merge( df_cargo_overview_temp1, df_cargo_overview_loading_time,     on='i_act_cargo', how='inner')
df_cargo_overview       = pd.merge( df_cargo_overview_temp2, df_cargo_overview_delivery_time,    on='i_act_cargo', how='inner')
# Renaming columns Cargo overview for Excel Sheet:
df_cargo_overview.rename(columns={
    'i_act_cargo':'Cargo',
    'mm::ep_calc_vesselOfCargo':'Vessel Used',
    'mm::p_calc_totalCostPerCargo':'Cargo Cost',
    'mm::sp_calc_loadingTimePerCargo':'Loading Time',
    'mm::sp_calc_deleveringTimePerCargo':'Delivery Time'
    },inplace=True)


# Retrieving the Route overview:
# Getting data from AIMMS model:
df_route_overview_action_type = my_aimms.mm.ep_post_vesselActivityType.data()
df_route_overview_location    = my_aimms.mm.ep_post_vesselActivityLocation.data()
df_route_overview_first       = my_aimms.mm.ep_post_vesselActivityFirst.data()
df_route_overview_last        = my_aimms.mm.ep_post_vesselActivityLast.data()
# Merge the Cargo overview dataframes:
df_route_overview_temp1 = pd.merge( df_route_overview_action_type, df_route_overview_location, on=['i_used_route','i_leg'], how='inner')
df_route_overview_temp2 = pd.merge( df_route_overview_temp1, df_route_overview_first,          on=['i_used_route','i_leg'], how='inner')
df_route_overview       = pd.merge( df_route_overview_temp2, df_route_overview_last,           on=['i_used_route','i_leg'], how='inner')
df_route_overview.rename(columns={
    'i_used_route':'Route',
    'i_leg':'Leg',
    'mm::ep_post_vesselActivityType':'ActionType',
    'mm::ep_post_vesselActivityLocation':'Location',
    'mm::ep_post_vesselActivityFirst':'First',
    'mm::ep_post_vesselActivityLast':'Last'
    },inplace=True)


excel_file_path = datainput.replace("Cargo","Solution")

with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    df_vessel_overview.to_excel(writer, sheet_name='Vessel Overview', index=False)
    df_cargo_overview.to_excel( writer, sheet_name='Cargo Overview',  index=False)
    df_route_overview.to_excel( writer, sheet_name='Route overview',  index=False)


now = datetime.datetime.now()
print(f"finish: {now} cwd: {cwd}")