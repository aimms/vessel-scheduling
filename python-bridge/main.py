# This is a sample Python script.
# The purpose of this script is to demo the aimmspy Python bridge,
# see https://pypi.org/project/aimmspy/

# Remarks: 
# - an element not in the set that is the range of parameter - difficult to find the typo.
# + LoggerConfig.xml output opened in folder of .py file.
# - Superfluous DEBUG: type of 'self.project.aimms_api' is <class 'aimmspy_cpp.AimmsAPI'>

import time
import pandas as pd
import datetime
import os
import pathlib
import sys

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
    aimms_project_file=os.path.join('..', 'AIMMSProject', 'VesselScheduling.aimms'),

    # the name of an aimms set containing identifiers. 
    exposed_identifier_set_name="AllIdentifiers",  # Limit access to specific identifiers,

    # default data type when retrieving multi-dimensional data
    data_type_preference=DataReturnTypes.PANDAS,
    
    # Fill license URL if needed.
)
aimms_model : Model = project.get_model(__file__)

def process_vessel_schedule( datainput: str ):
    # Determine the input file.
    datainput_path = pathlib.Path(datainput)
    if not datainput_path.exists():
        print(f"File {datainput} does not exist.")
        sys.exit()


    # The horizon defines the start date for planning.
    datainput_pd_horizon = pd.read_excel(datainput,sheet_name='Horizon')
    ep_startHorizonDate = datainput_pd_horizon.loc[0,'StartDate']
    aimms_model.ep_startHorizonDate = datainput_pd_horizon.loc[0,'StartDate']

    # Get the location data from the LocationData sheet and 
    # copy it over to the AIMMS project, parameters p_latitude, and p_longitude.

    # Read Excel sheet:
    datainput_pd_location = pd.read_excel(datainput,sheet_name='LocationData')

    # Rename the columns to AIMMS identifiers:
    datainput_pd_location.rename(columns={        
        'Location'     : 'i_loc',                 
        'Latitude'     : 'p_latitude',            
        'Longitude'    : 'p_longitude',           
        'Idle Cost'    : 'p_idleCostLocation',    
        'Admin Cost'   : 'p_adminCostAtLocation', 
        'Loading Cost' : 'p_loadingCostAtLocation'
        }, inplace=True)

    # Actually assign to AIMMS identifiers:
    aimms_model.multi_assign(datainput_pd_location)


    # Get the cargo data and copy it over to the AIMMS model:

    # Read Excel sheet:
    datainput_pd_cargo=pd.read_excel(datainput,sheet_name='CargoData')

    # Rename the columns to AIMMS identifiers:
    datainput_pd_cargo.rename(columns={                     
        'Cargo'                : 'i_cargo',                 
        'Loading Port'         : 'ep_loadingPortsCargo',    
        'Delevering Port'      : 'ep_deliveringPortsCargo', 
        'Spot Cost'            : 'p_spotCostVessel',        
        'Minimum Loading Time' : 'ep_minTimeWindow',        
        'Maximum Loading Time' : 'ep_maxTimeWindow',        
        'Fixed Cost'           : 'p_cargoCost'              
        }, inplace=True)

    # Actually assign to AIMMS identifiers:
    aimms_model.multi_assign(datainput_pd_cargo)


    # Get the vessel data and copy it over to the AIMMS model:

    # Read Excel sheet:
    datainput_pd_vessel=pd.read_excel(datainput,sheet_name='VesselData')

    # Rename the columns to AIMMS identifiers:
    datainput_pd_vessel.rename(columns={              
        'Vessel'         : 'i_vessel',                
        'Port of Origin' : 'ep_originPortOfVessel',   
        'Sailing Cost'   : 'p_sailingCost'            
        }, inplace=True)

    # Actually assign to AIMMS identifiers:
    aimms_model.multi_assign(datainput_pd_vessel)


    # Execute the optimization logic.
    aimms_model.pr_GenRoutesSolve()


    # Retrieving the Vessel overview:

    # Getting data from AIMMS model:
    df_vessel_overview = aimms_model.multi_data(["i_vessel","mm::ep_calc_routeOfVessel","mm::p_calc_operationalCostPerVessel","mm::p_calc_totalTravelDaysPerVessel"])

    # Renaming columns Vessel overview for Excel Sheet:
    df_vessel_overview.rename(columns={
        'i_vessel'                            : 'Vessel',
        'mm::ep_calc_routeOfVessel'           : 'Route',
        'mm::p_calc_operationalCostPerVessel' : 'Route Cost',
        'mm::p_calc_totalTravelDaysPerVessel' : 'Route Period'
        },inplace=True)


    # Retrieving the Cargo overview:

    # Getting data from AIMMS model:
    df_cargo_overview = aimms_model.multi_data(["i_act_cargo","mm::ep_calc_vesselOfCargo","mm::p_calc_totalCostPerCargo","mm::sp_calc_loadingTimePerCargo","mm::sp_calc_deleveringTimePerCargo"])

    # Renaming columns Cargo overview for Excel Sheet:
    df_cargo_overview.rename(columns={
        'i_act_cargo'                        : 'Cargo',
        'mm::ep_calc_vesselOfCargo'          : 'Vessel Used',
        'mm::p_calc_totalCostPerCargo'       : 'Cargo Cost',
        'mm::sp_calc_loadingTimePerCargo'    : 'Loading Time',
        'mm::sp_calc_deleveringTimePerCargo' : 'Delivery Time'
        },inplace=True)


    # Retrieving the Route overview:

    # Getting data from AIMMS model:
    df_route_overview = aimms_model.multi_data(["i_act_cargo","mm::ep_calc_vesselOfCargo","mm::p_calc_totalCostPerCargo","mm::sp_calc_loadingTimePerCargo","mm::sp_calc_deleveringTimePerCargo"])

    # Renaming columns Route overview for Excel Sheet:
    df_route_overview.rename(columns={
        'i_used_route'                       : 'Route',
        'i_leg'                              : 'Leg',
        'mm::ep_post_vesselActivityType'     : 'ActionType',
        'mm::ep_post_vesselActivityLocation' : 'Location',
        'mm::ep_post_vesselActivityFirst'    : 'First',
        'mm::ep_post_vesselActivityLast'     : 'Last'
        },inplace=True)


    # Exporting the three data frames each to a separate sheet:
    excel_file_path = datainput.replace("Cargo","Solution")
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df_vessel_overview.to_excel(writer, sheet_name='Vessel Overview', index=False)
        df_cargo_overview.to_excel( writer, sheet_name='Cargo Overview',  index=False)
        df_route_overview.to_excel( writer, sheet_name='Route overview',  index=False)

    
if __name__=="__main__":
    datainput=os.path.join(projectroot,'AIMMSProject', 'data', 'VS_5Vessel_15Cargo.xlsx')
    process_vessel_schedule(datainput)
    now = datetime.datetime.now()
    print(f"finish: {now} cwd: {cwd}")
