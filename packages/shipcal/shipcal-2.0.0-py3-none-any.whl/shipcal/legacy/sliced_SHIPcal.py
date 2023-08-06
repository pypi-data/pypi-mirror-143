#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 19:54:51 2016

Version record:
    - (1.1.1) Significant change in IAM function to allow Pitch/Azimuth/Roll
    - (1.1.5) OperationOilSimple included
    - (1.1.8) 5/1/2019 Modify code to allow offline simulations with other collectors,
    a very simple cost model has been included, this simplistic model will change
    in future versions, thanks to Jose Escamilla for his comments.
    - (1.1.9) 26/6/2019 Included savings Graph. Corrected savingsFraction = solarNetFraction. 
    Included boiler_eff for tacking care of energy before boiler (Energy_Before), which is different
    to energy after the boiler (Demand)
    - (1.1.10) 9/9/2019 New finance functions
       - (28/11/2019) Rebranding to SHIPcal to avoid confusion with solatom's propetary front-end ressspi  
       
@authors (in order of involvement): 
    Miguel Frasquet Herraiz - US/SOLATOM (mfrasquetherraiz@gmail.com)
    Joey Bannenberg - FONTYS UNIVERSITY (jhabannenberg@gmail.com)
    Yago NEl Vila Gracia - ETH (yagonelvilagracia@hotmail.com)
    Juan Antonio Aramburo Pasapera  - CIMAV (ja.arpa97@gmail.com)
"""

#Standard Libs
import sys
import os
import numpy as np
import pandas as pd
from iapws import IAPWS97

#Place to import SHIPcal Libs

from General_modules.func_General import DemandData,waterFromGrid_trim,thermalOil,reportOutputOffline, moltenSalt,waterFromGrid_v3 
from General_modules.demandCreator_v1 import demandCreator
from General_modules.fromDjangotoSHIPcal import djangoReport
from Solar_modules.EQSolares import SolarData
from Solar_modules.EQSolares import theta_IAMs
from Solar_modules.EQSolares import IAM_calc
from Finance_modules.FinanceModels import SP_plant_costFunctions
from Integration_modules.integrations import offStorageSimple, operationSimple, operationDSG, outputOnlyStorageSimple, outputWithoutStorageSimple, outputStorageSimple, offSimple, outputFlowsHTF, outputFlowsWater, directopearationSimple, operationDSG_Rec, offDSG_Rec, outputDSG_Rec#, offOnlyStorageSimple, operationOnlyStorageSimple
from Plot_modules.plottingSHIPcal import SankeyPlot, mollierPlotST, mollierPlotSH, thetaAnglesPlot, IAMAnglesPlot, demandVsRadiation, rhoTempPlotSalt, rhoTempPlotOil, viscTempPlotSalt, viscTempPlotOil, flowRatesPlot, prodWinterPlot, prodSummerPlot, productionSolar, storageWinter, storageSummer, storageNonAnnual, financePlot, prodMonths, savingsMonths,SL_S_PDR_Plot,storageNonAnnualSL_S_PDR

[Turn_key, ESCO,optic_efficiency_N,solatom_param,SOL_plant_costFunctions,reportOutput, djangoReportCIMAV,CIMAV_collectors,IAM_fiteq,IAM_calc_weq,theta_IAMs_v3,CIMAV_plant_costFunctions,equiv_coll_series_o1]=[None, None,None,None,None,None,None,None,None,None,None,None,None]

def SHIPcal(origin,inputsDjango,plots,imageQlty,confReport,modificators,desginDict,simControl,pk):
    version, initial_variables_dict, coll_par, integration_Dict = SHIPcal_prep(origin,inputsDjango,confReport,modificators,simControl)
    initial_variables_dict = SHIPcal_integration(desginDict,initial_variables_dict, integration_Dict)
    coll_par.update({'auto':'off'})
    [template_vars,plotVars,reportsVar,version] = SHIPcal_auto(origin,inputsDjango,plots,imageQlty,confReport,desginDict,initial_variables_dict,coll_par,modificators,pk)
    return(template_vars,plotVars,reportsVar,version)

def SHIPcal_prep(origin,inputsDjango,confReport,modificators,simControl): #This very first part of the SHIPcal reads the parameters, TMY, and main variables
    
#%%
# ------------------------------------------------------------------------------------
# BLOCK 1 - VARIABLE INITIALIZATION --------------------------------------------------
# ------------------------------------------------------------------------------------
    
    # BLOCK 1.1 - SIMULATION CONTROL <><><><><><><><><><><><><><><><><><><><><><><><><><><>
    
    version="1.1.10" #SHIPcal version
    sender=confReport['sender'] #Sender identity. Needed for use customized modules or generic modules (Solar collectors, finance, etc.)

    
    #-->  Paths
    if sender=='solatom': #The request comes from Solatom's front-end www.ressspi.com
        sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/ressspi_solatom/') #SOLATOM
    
    elif sender=='CIMAV': #The request comes from CIMAV front-end
        sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/CIMAV/') #CIMAV collectors information databases and TMYs

    if origin==-2: #Simulation called from ReSSSPI front-end
        plotPath=os.path.dirname(os.path.dirname(__file__))+'/ressspi/ressspiForm/static/results/' #FilePath for images when called by www.ressspi.com
    elif origin==-3:
        plotPath=os.path.dirname(os.path.dirname(__file__))+'/CIMAV/results/'
    elif origin==0:
        plotPath=""
    elif origin==1: #Simulation called from other front-ends (use positive integers)
        plotPath=""
    
    global Turn_key, ESCO
    #-->  Propetary libs
    if sender=='solatom': #The request comes from Solatom's front-end www.ressspi.com
        global optic_efficiency_N,solatom_param,SOL_plant_costFunctions,reportOutput
        from Solatom_modules.solatom_param import optic_efficiency_N #noqa
        from Solatom_modules.solatom_param import solatom_param #noqa
        from Solatom_modules.Solatom_finance import SOL_plant_costFunctions #noqa
        from Solatom_modules.templateSolatom import reportOutput #noqa
        from Finance_modules.FinanceModels import Turn_key, ESCO #noqa
    elif sender=='CIMAV': #The request comes from CIMAV front-end
        global djangoReportCIMAV,CIMAV_collectors,IAM_fiteq,IAM_calc_weq,theta_IAMs_v3,CIMAV_plant_costFunctions,equiv_coll_series_o1
        from CIMAV.CIMAV_modules.fromDjangotoRessspivCIMAV import djangoReport as djangoReportCIMAV #noqa
        #Imports a CIMAV's module to return the parameters of collectors supported by CIMAV
        from CIMAV.CIMAV_modules.CIMAV_collectors import CIMAV_collectors #noqa
        from CIMAV.CIMAV_modules.CIMAV_financeModels import Turn_key,ESCO,CIMAV_plant_costFunctions #noqa
        from Solar_modules.iteration_process import equiv_coll_series_o1
        from Solar_modules.EQSolares import theta_IAMs_v3, IAM_fiteq,IAM_calc_weq
    else:
        from Finance_modules.FinanceModels import Turn_key, ESCO
    
    #-->  Simulation options
    finance_study=simControl['finance_study'] #In order to include the financial study. 1-> Yes ; 0-> No
    
    #-->  Simulation length
    
    # Initial step of the simulation
    month_ini_sim=simControl['mes_ini_sim']   # Month in which the simulation starts 
    day_ini_sim=simControl['dia_ini_sim']   # Day in which the simulation starts 
    hour_ini_sim=simControl['hora_ini_sim'] # Hour in which the simulation starts 
    
    # Final step of the simulation
    month_fin_sim=simControl['mes_fin_sim']   # Month in which the simulation ends
    day_fin_sim=simControl['dia_fin_sim']   # Day in which the simulation ends
    hour_fin_sim=simControl['hora_fin_sim'] # Hour in which the simulation ends
    
    #%%
    # BLOCK 1.2 - PARAMETERS <><><><><><><><><><><><><><><><><><><><><><><><><><><>
    
    #--> Finance parameters
    fuelCostRaise=3.5 # Annual increase of fuel price [%]
    
    # Annual increase of the price of money through Consumer Price Index [%]
    if sender == 'CIMAV':
        CPI=5 # 5 for México
        
        #Some specific fuels increase
        if inputsDjango['fuel'] == 'electricidad':
            fuelCostRaise=7.09 #[%] From thesis :“Análisis térmico de la envolvente de naves industriales con incorporación de tecnología solar fotovoltaica” by CARLOS ARMANDO ESPINO REYES May 2019
        elif inputsDjango['fuel'] == 'gas_natural':
            fuelCostRaise=11.47 #[%] From thesis :“Análisis térmico de la envolvente de naves industriales con incorporación de tecnología solar fotovoltaica” by CARLOS ARMANDO ESPINO REYES May 2019
        elif inputsDjango['fuel'] == 'diesel':
            fuelCostRaise=6.52 # [%] Information from http://www.intermodalmexico.com.mx/Portal/AjusteCombustible/Historico#
        elif inputsDjango['fuel'] == 'gasolina_nafta':
            fuelCostRaise=9.76 # [%] Information from https://datos.gob.mx/busca/dataset/ubicacion-de-gasolineras-y-precios-comerciales-de-gasolina-y-diesel-por-estacion
        elif inputsDjango['fuel'] == 'gas_licuado_petroleo':
            fuelCostRaise=3 #[%] Information from https://datos.gob.mx/busca/dataset/precios-maximos-de-venta-de-primera-mano-en-materia-de-gas-lp
        #elif fuel == 'coque_carbon':
            #fuelCostRaise= #[%] Information from
    else:
        CPI=2.5 # 2.5 for Spain 
        
    costRaise=CPI/100+fuelCostRaise/100
    priceReduction=10 #[%] NOT USED
    
    n_years_sim=25 # Collector life in years & number of years for the simulation [years]
    
    #--> Process parameters
    
    lim_inf_DNI=200 # Minimum temperature to start production [W/m²]
    m_dot_min_kgs=0.06 #1e-10 # Minimum flowrate before re-circulation [kg/s]
    coef_flow_rec=1 # Multiplier for flowrate when recirculating [-]
    Boiler_eff=0.8 # Boiler efficiency to take into account the excess of fuel consumed [-]
    if inputsDjango.get('demandUnit',0)=='666':
        Boiler_eff=1 #If the demand was introduced as the work fluid litters required to heat up the Boiler efficiency is not taken into account
    subcooling=5 #Deegre of subcooling
    
    #%%
    # BLOCK 1.3 - SYSTEM VARIABLES <><><><><><><><><><><><><><><><><><><><><><><><><><><>    
    
    #--> Simulation modifiers (useful to control extraordinary situations)
    mofDNI=modificators['mofDNI'] # DNI modificator to take into correct Meteonorm data if necessary [-] 
    #The other modificators are called in SHIPcal_auto
    
        ## --> Solar collector 
        
    if sender=='solatom': #Using Solatom Collector
        
        ## IAM 
        IAM_file='Solatom.csv'
        IAM_folder=os.path.dirname(os.path.dirname(__file__))+"/ressspi_solatom/IAM_files/"
        IAMfile_loc=IAM_folder+IAM_file
        
        ## Solar collector characteristics
        type_coll=20 #Solatom 20" fresnel collector - Change if other collector is used
        REC_type=1
        D,Area_coll,rho_optic_0,huella_coll,Long,Apert_coll=solatom_param(type_coll)
        
        coll_par = {'type_coll':type_coll,'REC_type':REC_type,'Area_coll':Area_coll,'rho_optic_0':rho_optic_0,'IAMfile_loc':IAMfile_loc,'Long':Long}
    
    elif sender=='CIMAV': #Use one of the collectors supported by CIMAV
        type_coll=inputsDjango['collector_type']#The collector datasheet will have this name
        Area_coll,rho_optic_0,eta1,eta2,mdot_test,Long,weight,coll_optic, lon_angs_rad, lonIAMs, tran_lon_angs_rad, tranIAMs = CIMAV_collectors(type_coll)
        
        blong,nlong = IAM_fiteq(lon_angs_rad,lonIAMs)
        btrans,ntrans = IAM_fiteq(tran_lon_angs_rad, tranIAMs)
        REC_type = 1 #Dead variable to avoid crashes with the previous code
        
        m_dot_min_kgs = mdot_test*Area_coll
        coll_par = {'type_coll':type_coll,'REC_type':REC_type,'Area_coll':Area_coll,'rho_optic_0':rho_optic_0,'eta1':eta1,'eta2':eta2,'mdot_test_permeter':mdot_test,'Long':Long,'blong':blong,'nlong':nlong,'btrans':btrans,'ntrans':ntrans,'coll_weight':weight, 'coll_optic':coll_optic}
        
    else: #Using other collectors (to be filled with customized data)
        
        ## IAM 
        IAM_file='defaultCollector.csv'
        IAM_folder=os.path.dirname(__file__)+"/Collector_modules/"
        IAMfile_loc=IAM_folder+IAM_file
        
        ## Solar collector characteristics
        REC_type=1 #Type of receiver used (1 -> Schott receiver tube)
        Area_coll=26.4 #Aperture area of collector per module [m²]
        rho_optic_0=0.75583 #Optical eff. at incidence angle=0 [º]
        Long=5.28 #Longitude of each module [m]
        type_coll = 'default'
        coll_par = {'type_coll':type_coll,'REC_type':REC_type,'Area_coll':Area_coll,'rho_optic_0':rho_optic_0,'IAMfile_loc':IAMfile_loc,'Long':Long}
        
    if origin == -2:
        #Retrieve front-end inputs
        [inputs,annualConsumptionkWh,P_op_bar,monthArray,weekArray,dayArray]=djangoReport(inputsDjango)
        
        ## METEO
        meteoDB = pd.read_csv(os.path.dirname(os.path.dirname(__file__))+"/ressspi_solatom/METEO/meteoDB.csv", sep=',') #Reads the csv file where the register of the exiting TMY is.
        locationFromRessspi=inputs['location'] #Extracts which place was selected from the form 
        localMeteo=meteoDB.loc[meteoDB['Provincia'] == locationFromRessspi, 'meteoFile'].iloc[0] #Selects the name of the TMY file that corresponds to the place selected in the form
        file_loc=os.path.dirname(os.path.dirname(__file__))+"/ressspi_solatom/METEO/"+localMeteo #Stablishes the path to the TMY file
        Lat=meteoDB.loc[meteoDB['Provincia'] == locationFromRessspi, 'Latitud'].iloc[0] #Extracts the latitude from the meteoDB.csv file for the selected place
        Positional_longitude = 'Not used'
        Huso=meteoDB.loc[meteoDB['Provincia'] == locationFromRessspi, 'Huso'].iloc[0] #Extracts the time zone for the selected place
        
    elif origin == -3:
        ## METEO
        localMeteo=inputsDjango['location']#posiblemente se pueda borrar después
        file_loc_list=[os.path.dirname(os.path.dirname(__file__)),'CIMAV/meteorologic_database',inputsDjango['pais'],inputsDjango['location']] #Stores the localization of the TMY as a list=[basedir,TMYlocalizationfolder,countryfolder,TMYcity]
        file_loc='/'.join(file_loc_list) #Converts file_loc_list into a single string for later use
        
    else:
        ## METEO
        if origin == 1:
            #Retrieve front-end inputs 
            [inputs,annualConsumptionkWh,P_op_bar,monthArray,weekArray,dayArray]=djangoReport(inputsDjango)
            ## METEO (free available meteo sets)
            locationFromFrontEnd=inputs['location'] #locationFromFrontEnd
        else: #Contains origin == 0 and will be the default if no new database for a specific implementation has been added.
            #localMeteo="Fargo_SAM.dat" #Be sure this location is included in SHIPcal DB
            localMeteo="Bakersfield.dat"
        if sender=='solatom': #Use Solatom propietary meteo DB. This is only necessary to be able to use solatom data from terminal
            meteoDB = pd.read_csv(os.path.dirname(os.path.dirname(__file__))+"/ressspi_solatom/METEO/meteoDB.csv", sep=',') 
            file_loc=os.path.dirname(os.path.dirname(__file__))+"/ressspi_solatom/METEO/"+localMeteo       
            Lat=meteoDB.loc[meteoDB['meteoFile'] == localMeteo, 'Latitud'].iloc[0]
            Huso=meteoDB.loc[meteoDB['meteoFile'] == localMeteo, 'Huso'].iloc[0]
        elif sender=='SHIPcal':
            from simforms.models import Locations
            file_loc = locationFromFrontEnd
            localMeteo= Locations.objects.get(pk=locationFromFrontEnd).city
            Lat = Locations.objects.get(pk=locationFromFrontEnd).lat
            Huso = 0 #Not used currently, it is assumed to have solar hourly data
            #meteo_data.order_by('hour_year_sim').values_list('DNI',flat=True)
        else:
            locationFromFrontEnd=inputs['location']
            meteoDB = pd.read_csv(os.path.dirname(__file__)+"/Meteo_modules/meteoDB.csv", sep=',')  
            localMeteo=meteoDB.loc[meteoDB['Provincia'] == locationFromFrontEnd, 'meteoFile'].iloc[0]
            file_loc=os.path.dirname(__file__)+"/Meteo_modules/"+localMeteo
            Lat=meteoDB.loc[meteoDB['meteoFile'] == localMeteo, 'Latitud'].iloc[0]
            Huso=meteoDB.loc[meteoDB['meteoFile'] == localMeteo, 'Huso'].iloc[0]
        
        
        ## --> TO BE IMPLEMENTED Not used for the moment, it will change in future versions
    """    
    orientation="NS"
    inclination="flat" 
    shadowInput="free"
    terreno="clean_ground"
    """

    beta=0 #Pitch not implemented [rad]
    orient_az_rad=0 #Orientation not implemented [rad]
    roll=0 #Roll not implemented [rad]
    coll_par.update({'beta':beta,'orient_az_rad':orient_az_rad,'roll':roll})
    
    
    #By default water flows in closed loop
    T_in_flag=1 #Flag 1 means closed loop (water flowing from a piping closed loop); Flag 0 means open loop (water flowing from the grid)#Temperature of the make-up water
    T_in_C_AR=waterFromGrid_v3(file_loc,sender)
    #Trim the T_in_C_AR [8760] to the simulation frame 
    T_in_C_AR=waterFromGrid_trim(T_in_C_AR,month_ini_sim,day_ini_sim,hour_ini_sim,month_fin_sim,day_fin_sim,hour_fin_sim)
    
    # --> Front-end inputs
    
    if origin==-2: #Simulation called from front-end -> www.ressspi.com

        ## INDUSTRIAL APPLICATION
            #>> PROCESS
        fluidInput=inputs['fluid'] #Type of fluid 
        T_out_C=inputs['outletTemp'] #HIGH - Process temperature [ºC]
        T_in_C=inputs['inletTemp'] #LOW - Temperature at the return of the process [ºC]
            
            #>> ENERGY DEMAND
       
        if inputs['location_aux']=="":
            file_demand=demandCreator(annualConsumptionkWh,dayArray,weekArray,monthArray)
        else:
            file_demand = pd.read_csv(os.path.dirname(os.path.dirname(__file__))+"/ressspi/"+inputs['location_aux'], sep=',')

        arraysConsumption={'dayArray':dayArray,'weekArray':weekArray,'monthArray':monthArray}
        inputs.update(arraysConsumption)
            
        ## FINANCE
        businessModel=inputs['businessModel'] #Type of business model
        fuel=inputs['currentFuel'] #Type of fuel used
        Fuel_price=inputs['fuelPrice']   #Price of fossil fuel [€/kWh]
        co2TonPrice=inputs['co2TonPrice'] #[€/ton]
        co2factor=inputs['co2factor'] #[-]
         
    elif origin==-3: #Simulation called from CIMAV's front end
    
        T_in_flag=inputsDjango['T_in_flag'] #Flag 1 means closed loop (water flowing from a piping closed loop); Flag 0 means open loop (water flowing from the grid)
        if T_in_flag == 0:    #To avoid crashes with certain integrations    
            T_in_C = np.average(T_in_C_AR)
            inputsDjango['tempIN'] = T_in_C
        
        #Retrieve front-end inputs
        [inputs,annualConsumptionkWh,P_op_bar,monthArray,weekArray,dayArray]=djangoReportCIMAV(inputsDjango)
        
        ## INDUSTRIAL APPLICATION
            #>> PROCESS
        fluidInput=inputsDjango['fluid'] #Type of fluid 
        T_out_C=inputsDjango['tempOUT'] #HIGH - Process temperature [ºC]
        T_in_C=inputsDjango['tempIN'] #LOW - Temperature at the return of the process [ºC]
        
            #>> ENERGY DEMAND 
        file_demand=demandCreator(annualConsumptionkWh,dayArray,weekArray,monthArray)
       
        ## FINANCE
        businessModel=inputsDjango['businessModel'] #Type of business model
        fuel=inputsDjango['fuel'] #Type of fuel used
        Fuel_price=inputsDjango['fuelPrice'] #Price of fossil fuel [mxn/kWh] transformed the units in the views.py
        co2TonPrice= inputsDjango['co2TonPrice'] #[mxn/ton]
        co2factor=inputsDjango['co2factor'] #[-]
        
    elif origin==1: #Simulation called from external front-end. Available from 1 to inf+

        ## INDUSTRIAL APPLICATION
            #>> PROCESS
        fluidInput=inputs['fluid'] #Type of fluid 
        T_out_C=inputs['outletTemp'] #HIGH - Process temperature [ºC]
        T_in_C=inputs['inletTemp'] #LOW - Temperature at the return of the process [ºC]
        P_op_bar=P_op_bar #[bar]
            
            #>> ENERGY DEMAND
        file_demand=demandCreator(annualConsumptionkWh,dayArray,weekArray,monthArray)
       
        arraysConsumption={'dayArray':dayArray,'weekArray':weekArray,'monthArray':monthArray}
        inputs.update(arraysConsumption)
            
        ## FINANCE
        businessModel=inputs['businessModel'] #Type of business model
        fuel=inputs['currentFuel'] #Type of fuel used
        Fuel_price=inputs['fuelPrice']   #Price of fossil fuel [€/kWh]
        co2TonPrice=inputs['co2TonPrice'] #[€/ton]
        co2factor=inputs['co2factor'] #[-]
         
                  
    elif origin==0:  #Simulation called from Python file (called from the terminal)
        
        ## INDUSTRIAL APPLICATION
            #>> PROCESS
        fluidInput="steam" #"water" "steam" "oil" "moltenSalt"
        T_out_C=235 #HIGH - Process temperature [ºC]
        T_in_C=20 #LOW - Temperature at the return of the process [ºC]
        P_op_bar=30 #[bar] 
        
        # Not implemented yet
        """
        distanceInput=15 #From the solar plant to the network integration point [m]
        surfaceAvailable=500 #Surface available for the solar plant [m2]
        """
            
        ## ENERGY DEMAND
#       dayArray=[0,0,0,0,0,0,0,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,0,0,0,0,0,0] #12 hours day profile
        dayArray=[1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24,1/24] #24 hours day profile
       
        weekArray=[0.143,0.143,0.143,0.143,0.143,0.143,0.143] #No weekends
        monthArray=[1/12,1/12,1/12,1/12,1/12,1/12,1/12,1/12,1/12,1/12,1/12,1/12] #Whole year     
        totalConsumption=1875*8760 #[kWh]
        file_demand=demandCreator(totalConsumption,dayArray,weekArray,monthArray)
        # file_demand = pd.read_csv(os.path.dirname(os.path.dirname(__file__))+"/ressspi_offline/demand_files/demand_con.csv", sep=',')   

        ## FINANCE
        businessModel="turnkey"
        fuel="Gasoil-B" #Type of fuel
        Fuel_price=0.05 #Price of fossil fuel [€/kWh]
        co2TonPrice=0 #[€/TonCo2]
        co2factor=1 #Default value 1, after it will be modified [-]

        #CO2 factors of the different fuels availables (Usually it is taken care by the front-end but here, since the simulation is not called from a front-end, it has to be calculated)
        if fuel in ["NG","LNG"]:
            co2factor=.2/1000 #[TonCo2/kWh]  #https://www.engineeringtoolbox.com/co2-emission-fuels-d_1085.html
        if fuel in ['Fueloil2','Fueloil3','Gasoil-B','Gasoil-C']:
            co2factor=.27/1000 #[TonCo2/kWh]       #https://www.engineeringtoolbox.com/co2-emission-fuels-d_1085.html    
        if fuel in ['Electricity']:
            co2factor=.385/1000 #[TonCo2/kWh]  #https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
        if fuel in ['Propane','Butane','Air-propane']:
            co2factor=.22/1000 #[TonCo2/kWh]    #https://www.engineeringtoolbox.com/co2-emission-fuels-d_1085.html  
        if fuel in ['Biomass']:
            co2factor=.41/1000 #[TonCo2/kWh]  #https://www.engineeringtoolbox.com/co2-emission-fuels-d_1085.html

    #Demand of energy before the boiler
    Energy_Before=DemandData(file_demand,month_ini_sim,day_ini_sim,hour_ini_sim,month_fin_sim,day_fin_sim,hour_fin_sim) # [kWh]
    Energy_Before_annual=sum(Energy_Before) #This should be exactly the same as annualConsumptionkWh for annual simulations
    Demand=Boiler_eff*Energy_Before #Demand of energy after the boiler [kWh]
    
    # --> Meteo variables
    if sender == 'CIMAV':
        Lat,Huso,Positional_longitude,output=SolarData(file_loc,month_ini_sim,day_ini_sim,hour_ini_sim,month_fin_sim,day_fin_sim,hour_fin_sim,sender, optic_type=coll_optic)
        coll_par.update({'beta':np.radians(Lat)})
    else:
        Positional_longitude = 0 #Only used for CIMAV
        output,i_initial,i_final=SolarData(file_loc,month_ini_sim,day_ini_sim,hour_ini_sim,month_fin_sim,day_fin_sim,hour_fin_sim,sender,Lat,Huso)

    """
    Output key:
    output[0]->month of year
    output[1]->day of month
    output[2]->hour of day
    output[3]->hour of year
    output[4]->W - rad
    output[5]->SUN_ELV - rad
    output[6]->SUN AZ - rad
    output[7]->DECL - rad
    output[8]->SUN ZEN - rad
    output[9]->DNI  - W/m2
    output[10]->temp -C
    output[11]->step_sim
            
    """
    
    time_angle = output[:,4]
    SUN_ELV=output[:,5] # Sun elevation [rad]
    SUN_AZ=output[:,6] # Sun azimuth [rad]
    DNI=output[:,9] # Direct Normal Irradiation [W/m²]
    temp=output[:,10]+273 # Ambient temperature [K] 
    step_sim=output [:,11] #Array containing the simulation steps 
    steps_sim=len(output) # Number of steps in the simulation

    
    DNI=DNI*mofDNI # DNI modified if needed. This is necessary to take into account 

#%%
# ------------------------------------------------------------------------------------
# BLOCK 2 - SOLAR SIMULATION --------------------------------------------------
# ------------------------------------------------------------------------------------
    # BLOCK 2.1 - PROCESS VARIABLES <><><><><><><><><><><><><><><><><><><><><><><><><><><>      
    # IEA SHC Task 49 "Integration guidelines" http://task49.iea-shc.org/Data/Sites/7/150218_iea-task-49_d_b2_integration_guideline-final.pdf

    # --> Process variable init
    
    x_design=0 #Not used
    energStorageMax=0 #kWh
    porctSensible=0 #Not used
    T_out_HX_C=0 #Not used 
    s_process_in=0 #Not used
    h_process_in=0 #Not used
    in_s=0
    out_s=0
    h_in=0
    h_out=0
    DELTA_HX=5
    
    integration_Dict = {'P_op_Mpa':P_op_bar/10,'T_in_C':T_in_C,'T_out_C':T_out_C,'subcooling':subcooling,
                        'x_design':x_design,'h_process_in':h_process_in,'energStorageMax':energStorageMax,'T_in_flag':T_in_flag,
                        's_process_in':s_process_in,'in_s':in_s,'out_s':out_s,'h_in':h_in,'h_out':h_out,
                        'T_out_HX_C':T_out_HX_C,'porctSensible':porctSensible, 'DELTA_HX':DELTA_HX}
    
    
    # --> Simulation Loop variable init

    
    #coll_par depends of the sender so it is defined above
    #integration_Dict depends of the integration method so it is calculated before.
    meteoDict={'DNI':DNI,'localMeteo':localMeteo,'Lat':Lat,'Positional_longitude':Positional_longitude,'SUN_ELV':SUN_ELV,'SUN_AZ':SUN_AZ, 'temp':temp,'T_in_C_AR':T_in_C_AR,'time_angle':time_angle}
    financial_param = {'businessModel':businessModel,'Fuel_price':Fuel_price,'co2TonPrice':co2TonPrice,'co2factor':co2factor,'finance_study':finance_study,'costRaise':costRaise,'fuelCostRaise':fuelCostRaise,'CPI':CPI,'priceReduction':priceReduction,'n_years_sim':n_years_sim }
    process_param= {'lim_inf_DNI':lim_inf_DNI,'m_dot_min_kgs':m_dot_min_kgs,'coef_flow_rec':coef_flow_rec,'Boiler_eff':Boiler_eff,
                    'fluidInput':fluidInput,
                    'steps_sim':steps_sim,'step_sim':step_sim,'plotPath':plotPath, 'Energy_Before':Energy_Before, 'Energy_Before_annual':Energy_Before_annual,
                    'Demand':Demand}
    # initial_arrays = {'theta_i_rad':array_zeros.copy(),'theta_i_deg':array_zeros.copy(),'theta_transv_deg':array_zeros.copy(),'IAM_long':array_zeros.copy(),'IAM_t':array_zeros.copy(),'IAM':array_zeros.copy(),'T_in_K':array_zeros.copy(),'T_out_K':array_zeros.copy(),
    #                   'flowrate_kgs':array_zeros.copy(),'Perd_termicas':array_zeros.copy(),'flowrate_rec':array_zeros.copy(),'bypass':list(),'Q_prod':array_zeros.copy(),'Q_prod_lim':array_zeros.copy(), 'T_SD_K':array_zeros.copy(), 'SD_energy':array_zeros.copy(),
    #                   'Q_prod_rec':array_zeros.copy(),'Q_defocus':array_zeros.copy(),'SOC':array_zeros.copy(),'Q_charg':array_zeros.copy(),'Q_discharg':array_zeros.copy(),'Q_useful':array_zeros.copy(),'flowToHx':array_zeros.copy(),'flowToMix':array_zeros.copy(),
    #                   'flowDemand':array_zeros.copy(),'T_toProcess_K':array_zeros.copy(),'T_toProcess_C':array_zeros.copy(),'T_alm_K':array_zeros.copy(),'storage_energy':array_zeros.copy(),'x_out':array_zeros.copy(), 'Q_prod_steam':array_zeros.copy(), 
    #                   'Q_drum':array_zeros.copy()}
    initial_variables_dict = {}
    #initial_variables_dict.update(coll_par)
    initial_variables_dict.update(integration_Dict)
    initial_variables_dict.update(meteoDict)
    initial_variables_dict.update(financial_param)
    initial_variables_dict.update(process_param)
    #initial_variables_dict.update(initial_arrays)
    #initial_variables_dict.update(modificators)

    if inputs:
        initial_variables_dict.update({'inputs':inputs})
        
    return version, initial_variables_dict, coll_par, integration_Dict
    
    ## INTEGRATION
    
def SHIPcal_integration(desginDict,initial_variables_dict, integration_Dict):#This second section of SHIPcal updates the integration variables depending on the type of integrations. This will be used mainly to iterate over the storage capacity.
    
    initial_variables_dict.update(integration_Dict)
    
    P_op_Mpa=initial_variables_dict['P_op_Mpa'] #The solar field will use the same pressure than the process 
    T_in_C=initial_variables_dict['T_in_C'] #T_in_C inlet temperature to the collector #The inlet temperature towards the solar field is the same than the one of return from the process.
    T_out_C=initial_variables_dict['T_out_C'] #T_out_C outlet temperature from the collector #The outlet temperature towards the process is the same than the delivered from the collector.
    fluidInput = initial_variables_dict['fluidInput']
    Demand = initial_variables_dict['Demand']
    subcooling = initial_variables_dict['subcooling']
    T_in_C_AR = initial_variables_dict['T_in_C_AR']
    DELTA_HX=initial_variables_dict['DELTA_HX'] # Degrees for temperature delta experienced in the heat exchanger (for design) 
    type_integration=desginDict['type_integration'] # Type of integration scheme from IEA SHC Task 49 "Integration guidelines" http://task49.iea-shc.org/Data/Sites/7/150218_iea-task-49_d_b2_integration_guideline-final.pdf
    almVolumen=desginDict['almVolumen'] # Storage capacity [litres]
    
    # --> Integrations: 
        # SL_L_RF Supply level with liquid heat transfer media solar return flow boost
    
    if type_integration=="SL_L_RF": 
        ## SL_L_RF
        heatFactor=.9 # Percentage of temperature variation (T_out - T_in) provided by the heat exchanger (for design) 
        HX_eff=0.9 # Simplification for HX efficiency
        
        #Gets temperatures
        #Outlet from the process
        T_in_K=T_in_C+273 #The outlet from the process is the same as the inlet to the collectors
        
        #Inlet of the process
        
        if fluidInput=="water":    
            if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                T_out_C=IAPWS97(P=P_op_Mpa, x=0).T-273
        T_out_K=T_out_C+273

        if fluidInput=="water": #CAlculates other properties necessrry for water
            
            output_ProcessState=IAPWS97(P=P_op_Mpa, T=T_in_K)
            h_process_out=output_ProcessState.h
            
            input_ProcessState=IAPWS97(P=P_op_Mpa, T=T_out_K)
            s_process_in=input_ProcessState.s
            h_process_in=input_ProcessState.h
            
        T_av_process_K = (T_in_K+T_out_K)*0.5
        
        # --------------  STEP 1 -------------- 
        #The inlet temperature at the solar field (Afterwards it will corrected to take into account the HX) 
        #T_in_C=T_in_C #The inlet temperature at the solar field is the same than the return of the process
        #T_in_K=T_in_C+273
        
        #The outlet temperature at the solar field (Afterwards it will corrected to take into account the HX) 
        #T_out_C=T_out_C #The outlet temperature at the solar field is the same than the process temperature
        #T_out_K=T_out_C+273
        
    ##Heat Exchanger design 
            
        # --------------  STEP 2 -------------- 
        #HX inlet (process side)         
        #T_in_C=T_process_out_C #Already defined before
            
        # --------------  STEP 3 -------------- 
        #HX outlet (process side) 
        T_HX_out_K=(T_in_K+(T_out_K-T_in_K)*heatFactor)
        T_out_HX_C=T_HX_out_K-273
        if fluidInput=="water": 
            outputHXState=IAPWS97(P=P_op_Mpa, T=T_HX_out_K)
            h_HX_out=outputHXState.h
        
          # --------------  STEP 4 -------------- 
        #HX inlet (solar side) 
        T_out_P=T_HX_out_K+DELTA_HX-273  # Design point temperature at the inlet of the HX from the solar side
        T_out_C=T_out_P #T_out_C is updated
        T_out_K=T_out_C+273
        
         # --------------  STEP 5 -------------- 
            #HX outlet (solar side)        
        T_in_P=T_in_C+DELTA_HX  # Design point temperature at the outlet of the HX from the solar side
        T_in_C=T_in_P #T_in_C is updated
        T_in_K=T_in_C+273
        
        #Other auxiliar calculations necessary  (for plotting)
        if fluidInput=="water": 
            inputState=IAPWS97(P=P_op_Mpa, T=T_in_K) 
            h_in=inputState.h    
            in_s=inputState.s
            outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
            out_s=outputState.s
            h_out=outputState.h

        if fluidInput=="water": 
            initial_variables_dict.update({'h_process_in':h_process_in, 'h_process_out':h_process_out,
                                           's_process_in':s_process_in,
                                           'h_HX_out':h_HX_out,'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out})
        
        initial_variables_dict.update({'HX_eff':HX_eff,'T_in_C':T_in_C,'T_out_HX_C':T_out_HX_C, 'DELTA_HX':DELTA_HX,
                                       'T_out_C':T_out_C,'T_HX_out_K':T_HX_out_K,
                                       'heatFactor':heatFactor,'T_av_process_K':T_av_process_K})
        
        # ----------------------------------------
        # SL_L_P => Supply level with liquid heat transfer media parallel integration
        # PL_E_PM => Process level external HEX for heating of product or process medium
    
    elif type_integration == "SL_L_DRF":
        
        #Gets the temperatures
        
        if fluidInput=="water":    
            if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                T_out_C=IAPWS97(P=P_op_Mpa, x=0).T-273
        
        if fluidInput=="water": 
            output_ProcessState=IAPWS97(P=P_op_Mpa, T=T_in_C+273)

            input_ProcessState=IAPWS97(P=P_op_Mpa, T=T_out_C+273)
            
            s_process_in=input_ProcessState.s
            h_process_in=input_ProcessState.h

            #Other auxiliar calculations necessary  (for plotting)
            #These are from the view of the collectors
            h_in=output_ProcessState.h    
            in_s=output_ProcessState.s

            out_s=input_ProcessState.s
            h_out=input_ProcessState.h
            
            initial_variables_dict.update({'h_process_in':h_process_in,'s_process_in':s_process_in,
                                           'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out})
            
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C})
    
    elif type_integration=="SL_L_P" or type_integration=="PL_E_PM":   
        
        #Gets the temperatures
        
        T_process_out_K=T_in_C+273 #Outlet temperture from the process, the temperature that gets in the collector
        
        if fluidInput=="water":    
            if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                T_out_C=IAPWS97(P=P_op_Mpa, x=0).T-273
        T_process_in_K=T_out_C+273 #Inlet temperature towards the process. The outlet temperature from the collectors
        
        if fluidInput=="water": 
            output_ProcessState=IAPWS97(P=P_op_Mpa, T=T_process_out_K)

            input_ProcessState=IAPWS97(P=P_op_Mpa, T=T_process_in_K)
            
            s_process_in=input_ProcessState.s
            h_process_in=input_ProcessState.h

            #Other auxiliar calculations necessary  (for plotting)
            #These are from the view of the collectors
            h_in=output_ProcessState.h    
            in_s=output_ProcessState.s

            out_s=input_ProcessState.s
            h_out=input_ProcessState.h
            
            initial_variables_dict.update({'h_process_in':h_process_in,'s_process_in':s_process_in,
                                           'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out})
            
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C})
        
    # ---------------------------------------
    # SL_L_S => Supply level with liquid heat transfer media solar heating of storages
    # SL_L_S_PH => Supply level with liquid heat transfer media solar heating of storages (Preheating)
        
    elif type_integration=="SL_L_S" or type_integration=="SL_L_S_PH":
        
        ## SL_L_S
        DELTA_ST=30 # Temperature delta over the design process temp for the storage
        flowrate_design_kgs=2 # Design flow rate (fix value for SL_L_S)

        #---------------  STEP 1 -------------- 
        #The inlet temperature at the solar field 
        T_in_K=T_in_C+273#The inlet temperature at the solar field is the same than the return of the process
        #The outlet temperature at the solar field

        # --------------  STEP 2 -------------- 
        T_ini_storage=T_in_K #Initial temperature of the storage
        
        if fluidInput=="water": # Only applies to water
            if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                T_out_C=IAPWS97(P=P_op_Mpa, x=0).T-273-subcooling 
        
        T_out_K=T_out_C+273

        # --------------  STEP 3 --------------   
        T_min_storage=T_out_K #MIN temperature storage to supply to the process # Process temp [K]  
        if type_integration=="SL_L_S_PH":
            T_min_storage=T_in_K #MIN [K] When preheating the minimum temp is the process outlet    
        
        # --------------  STEP 4 -------------- 
        if type_integration=="SL_L_S":
            if fluidInput=="water": # Only applies to water
                if T_out_C+DELTA_ST>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                    T_max_storage=IAPWS97(P=P_op_Mpa, x=0).T -subcooling #Max temperature storage [K]
                else:
                    T_max_storage=T_out_C+DELTA_ST+273 #Max temperature storage [K]
            else:
                T_max_storage=T_out_C+DELTA_ST+273 #Max temperature storage [K]
        else:
            if fluidInput=="water": # Only applies to water
                if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                    T_max_storage=IAPWS97(P=P_op_Mpa, x=0).T -subcooling #Max temperature storage [K]
                else:
                    T_max_storage=T_out_C+273 #Max temperature storage [K]
            else:
                T_max_storage=T_out_C+273 #Max temperature storage [K]
        
        # --------------  STEP 5 -------------- 
        #energy_stored=0 # Initially the storage is empty The storage is always empty at the beginning. It is already taken into account in the next function
        
        if fluidInput=="water": # WATER STORAGE
            inputState=IAPWS97(P=P_op_Mpa, T=T_in_K)  #From the collectors point of view
            h_in=inputState.h
            in_s=inputState.s
            outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
            out_s=outputState.s
            h_out=outputState.h
            
            almacenamiento=IAPWS97(P=P_op_Mpa, T=T_max_storage) #Propiedades en el almacenamiento
            almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
            almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg          
            storage_max_energy=(almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_max_storage))/3600 #Storage capacity in kWh
            
            almacenamiento=IAPWS97(P=P_op_Mpa, T=T_in_K) #Propiedades en el almacenamiento
            almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
            almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg      
            
            storage_ini_energy=(almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_in_K))/3600 #Storage capacity in kWh
            
            almacenamiento=IAPWS97(P=P_op_Mpa, T=T_out_K) #Propiedades en el almacenamiento
            almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
            almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg      
            storage_min_energy=(almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_out_K))/3600 #Storage capacity in kWh
            
            if type_integration=="SL_L_S_PH":
                almacenamiento=IAPWS97(P=P_op_Mpa, T=T_in_K) #Propiedades en el almacenamiento
                almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
                almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg 
                storage_min_energy=(almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_in_K))/3600 #Storage capacity in kWh
            
            energStorageUseful=storage_max_energy-storage_min_energy # Maximum storage capacity in kWh
            energStorageMax=storage_max_energy-storage_ini_energy # Maximum storage capacity in kWh

        elif fluidInput=="oil": # THERMAL OIL STORAGE
            # Properties for MAX point
                 
            [storage_max_rho,storage_max_Cp,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_max_storage)
            storage_max_energy=(almVolumen*(1/1000)*(storage_max_rho)*storage_max_Cp*(T_max_storage))/3600 #Storage capacity in kWh
            
            [storage_ini_rho,storage_ini_Cp,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_in_K)
            storage_ini_energy=(almVolumen*(1/1000)*(storage_ini_rho)*storage_ini_Cp*(T_in_K))/3600 #Storage capacity in kWh
        
            [storage_min_rho,storage_min_Cp,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_out_K)
            storage_min_energy=(almVolumen*(1/1000)*(storage_min_rho)*storage_min_Cp*(T_out_K))/3600 #Storage capacity in kWh
            
            if type_integration=="SL_L_S_PH":
                [storage_min_rho,storage_min_Cp,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_in_K)
                storage_min_energy=(almVolumen*(1/1000)*(storage_min_rho)*storage_min_Cp*(T_in_K))/3600 #Storage capacity in kWh
            
            energStorageUseful=storage_max_energy-storage_min_energy # Maximum storage capacity in kWh
        
            energStorageMax=storage_max_energy-storage_ini_energy # Maximum storage capacity in kWh
    
        elif fluidInput=="moltenSalt": # MOLTEN SALTS STORAGE

            # Properties for MAX point
            [storage_max_rho,storage_max_Cp,k,Dv]=moltenSalt(T_max_storage)
            storage_max_energy=(almVolumen*(1/1000)*(storage_max_rho)*storage_max_Cp*(T_max_storage))/3600 #Storage capacity in kWh
            
            [storage_ini_rho,storage_ini_Cp,k,Dv]=moltenSalt(T_in_K)
            storage_ini_energy=(almVolumen*(1/1000)*(storage_ini_rho)*storage_ini_Cp*(T_in_K))/3600 #Storage capacity in kWh
        
            [storage_min_rho,storage_min_Cp,k,Dv]=moltenSalt(T_out_K)
            storage_min_energy=(almVolumen*(1/1000)*(storage_min_rho)*storage_min_Cp*(T_out_K))/3600 #Storage capacity in kWh
            
            if type_integration=="SL_L_S_PH":
                [storage_min_rho,storage_min_Cp,k,Dv]=moltenSalt(T_in_K)
                storage_min_energy=(almVolumen*(1/1000)*(storage_min_rho)*storage_min_Cp*(T_in_K))/3600 #Storage capacity in kWh
            
            energStorageUseful=storage_max_energy-storage_min_energy # Maximum storage capacity in kWh
        
            energStorageMax=storage_max_energy-storage_ini_energy # Maximum storage capacity in kWh
        
        if fluidInput=="water":
            initial_variables_dict.update({'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out})
        
        initial_variables_dict.update({'flowrate_design_kgs':flowrate_design_kgs,'T_in_C':T_in_C,'DELTA_ST':DELTA_ST,
                                       'T_out_C':T_out_C,'T_min_storage':T_min_storage,'T_max_storage':T_max_storage,
                                       'storage_max_energy':storage_max_energy,'storage_ini_energy':storage_ini_energy, 
                                       'storage_min_energy':storage_min_energy,'energStorageUseful':energStorageUseful,
                                       'energStorageMax':energStorageMax,'T_ini_storage':T_ini_storage})
            
    # ----------------------------------------
    # SL_L_PS => Supply level with liquid heat transfer media parallel integration with storage
            
    elif type_integration=="SL_L_PS":
    
        T_in_K=T_in_C+273
        
        if fluidInput=="water":
            if T_out_C>IAPWS97(P=P_op_Mpa, x=0).T-273: #Make sure you are in liquid phase
                T_out_C=IAPWS97(P=P_op_Mpa, x=0).T-273
            T_out_K=T_out_C+273
            #tempAlm=T_out_K-273
            inputState=IAPWS97(P=P_op_Mpa, T=T_in_K) #In the collector point of view
            h_in=inputState.h
            in_s=inputState.s
            outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
            out_s=outputState.s
            h_out=outputState.h
            
            #Storage calculations for water
            T_avg_K=(T_in_K+T_out_K)*0.5
            almacenamiento=IAPWS97(P=P_op_Mpa, T=T_avg_K) #Propiedades en el almacenamiento
            almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
            almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg
            energStorageMax=(almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_out_K-T_in_K))/3600 #Storage capacity in kWh
        
        elif fluidInput=="oil":
            T_out_K=T_out_C+273
            T_av_K=(T_in_K+T_out_K)*0.5
            [rho_av,Cp_av,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_av_K)
            energStorageMax=(almVolumen*(1/1000)*(rho_av)*Cp_av*(T_out_K-T_in_K))/3600 #Storage capacity in kWh
        
        elif fluidInput=="moltenSalt":
            T_out_K=T_out_C+273
            T_av_K=(T_in_K+T_out_K)*0.5
            [rho_av,Cp_av,k,Dv]=moltenSalt(T_av_K)
            energStorageMax=(almVolumen*(1/1000)*(rho_av)*Cp_av*(T_out_K-T_in_K))/3600 #Storage capacity in kWh
            
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,
                                       'energStorageMax':energStorageMax})
                    
    # ---------------------------------------- 
    # SL_S_FW => Supply level with steam solar heating of boiler feed water
        
    elif type_integration=="SL_S_FW":
        
        T_in_K=T_in_C+273

        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg
        in_s=initial.s
        
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)
        sat_vap=IAPWS97(P=P_op_Mpa, x=1)
        h_sat_liq=sat_liq.h
        h_sat_vap=sat_vap.h
        sensiblePart=h_sat_liq-h_in
        #latentPart=h_sat_vap-h_sat_liq #Not used
        total=h_sat_vap-h_in
        porctSensible=sensiblePart/total
        #porctLatent=latentPart/total #Not used
        Demand2=Demand*porctSensible
        
        T_out_K=IAPWS97(P=P_op_Mpa, x=0).T-subcooling #Heating point
        T_out_C=T_out_K-273 
          
        outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
        out_s=outputState.s
        h_out=outputState.h
        
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,
                                      'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out,'Demand2':Demand2})
            
    # ----------------------------------------
    # SL_S_FWS => Supply level with steam solar heating of boiler feed water including storage
        
    elif type_integration=="SL_S_FWS":

        T_in_K=T_in_C+273
        T_out_K=IAPWS97(P=P_op_Mpa, x=0).T #Heating point
        T_out_C=T_out_K-273 
        
        outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
        out_s=outputState.s
        h_out=outputState.h
            
        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg
        in_s=initial.s
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)
        sat_vap=IAPWS97(P=P_op_Mpa, x=1)
        h_sat_liq=sat_liq.h
        h_sat_vap=sat_vap.h
        sensiblePart=h_sat_liq-h_in
        #latentPart=h_sat_vap-h_sat_liq #Not used
        PreHeatedPart=h_out-h_in
        total=h_sat_vap-h_in
        porctSensible=sensiblePart/total
        #porctLatent=latentPart/total #Not used
        porctPreHeated=PreHeatedPart/total
        Demand2=Demand*porctPreHeated
        
        T_avg_K=(T_in_K+T_out_K)*0.5
        #tempAlm=T_out_K-273
        almacenamiento=IAPWS97(P=P_op_Mpa, T=T_avg_K) #Propiedades en el almacenamiento
        almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
        almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg
        energStorageMax=almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_out_K-T_in_K)/3600 #Storage capacity in kWh
            
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,
                                 'Demand2':Demand2,'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out,
                                 'energStorageMax':energStorageMax})
        
    # ---------------------------------------- 
    # SL_S_MW => Supply level with steam solar heating of boiler make-up water
    
    elif type_integration=="SL_S_MW":
     
        T_in_flag=0 #Flag 1 means closed loop (water flowing from a piping closed loop); Flag 0 means open loop (water flowing from the grid)
        
        T_in_K=T_in_C+273
        
        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg        
        in_s=initial.s
        
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)
        sat_vap=IAPWS97(P=P_op_Mpa, x=1)
        h_sat_liq=sat_liq.h
        h_sat_vap=sat_vap.h
        sensiblePart=h_sat_liq-h_in
        #latentPart=h_sat_vap-h_sat_liq #Not used
        total=h_sat_vap-h_in
        porctSensible=sensiblePart/total
        #porctLatent=latentPart/total #Not used
        Demand2=Demand*porctSensible
        
        T_out_K=IAPWS97(P=P_op_Mpa, x=0).T-subcooling #Heating point
        T_out_C=T_out_K-273 
          
        outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
        out_s=outputState.s
        h_out=outputState.h
        
        initial_variables_dict.update({'T_in_flag':T_in_flag,'T_in_C':T_in_C,'T_out_C':T_out_C,
                                       'Demand2':Demand2,'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out})
        
    # ----------------------------------------
    #SL_S_MWS => Supply level with steam solar heating of boiler make-up water including storage
        
    elif type_integration=="SL_S_MWS":
        
        T_in_flag=0 #Flag 1 means closed loop (water flowing from a piping closed loop); Flag 0 means open loop (water flowing from the grid)
        
        T_out_K=IAPWS97(P=P_op_Mpa, x=0).T #Heating point
        T_out_C=T_out_K-273 
        
        outputState=IAPWS97(P=P_op_Mpa, T=T_out_K)
        out_s=outputState.s
        h_out=outputState.h
        
        if T_in_flag==1:
            T_in_K=T_in_C+273
        else:
            T_in_K=np.average(T_in_C_AR)+273
            T_in_C=T_in_K-273
            
        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg
        in_s=initial.s
        
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)
        sat_vap=IAPWS97(P=P_op_Mpa, x=1)
        h_sat_liq=sat_liq.h
        h_sat_vap=sat_vap.h
        sensiblePart=h_sat_liq-h_in
        #latentPart=h_sat_vap-h_sat_liq #Not used
        PreHeatedPart=h_out-h_in
        total=h_sat_vap-h_in
        porctSensible=sensiblePart/total
        #porctLatent=latentPart/total #Not used
        porctPreHeated=PreHeatedPart/total
        Demand2=Demand*porctPreHeated
        
        T_avg_K=(T_in_K+T_out_K)*0.5
        #tempAlm=T_out_K-273
        almacenamiento=IAPWS97(P=P_op_Mpa, T=T_avg_K) #Propiedades en el almacenamiento
        almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
        almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg
        energStorageMax=almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_out_K-T_in_K)/3600 #Storage capacity in kWh
        
        initial_variables_dict.update({'T_in_flag':T_in_flag,'T_in_C':T_in_C,'T_out_C':T_out_C,
                                 'Demand2':Demand2,'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out,'energStorageMax':energStorageMax})
    
    # ----------------------------------------
    # SL_S_PD_OT => Supply level with steam direct solar steam generation once-through
        
    elif type_integration=="SL_S_PD_OT":  
        
        #Inlet towards the process
        input_ProcessState=IAPWS97(P=P_op_Mpa, x=1)
        s_process_in=input_ProcessState.s
        h_process_in=input_ProcessState.h
        
        #The outlet temperature at the solar field 
        T_out_K=input_ProcessState.T 
        T_out_C=input_ProcessState.T-273 #Temperature of saturation at that level

        # --------------  STEP 1 --------------
        
        #Outlet from the process
        T_in_K=T_in_C+273 #Temp return of condensates
        
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)

        if T_in_K>sat_liq.T: #Ensure the inlet is in liquid phase
            T_in_K=sat_liq.T  
        

        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg
        in_s=initial.s
        
        # --------------  STEP 2 --------------
        # Design point   
        x_design=0.8 #Design steam quality
        
        outputState=IAPWS97(P=P_op_Mpa, x=x_design)
        out_s=outputState.s
        h_out=outputState.h
        
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,
                                 'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out,'s_process_in':s_process_in,
                                 'h_process_in':h_process_in,'x_design':x_design})
        
    elif type_integration=="SL_S_PD": #Direct steam generation (Steam drum)
        
        # Outlet from the process
        #T_in_C = #T_process_out_C=T_process_out #The outlet from the process is the same as the inlet towards the solar field
        #T_in_K = T_in_C + 273# = T_process_out_K=T_process_out_C+273

        #Inlet towards the process
        input_ProcessState=IAPWS97(P=P_op_Mpa, x=1)
        #T_out_K=input_ProcessState.T # = T_process_in_K The inlet towards the process is the sames as the outlet from the solar field
        #T_out_C = T_out_K-273 # = T_process_in_C=T_process_in_K-273
        s_process_in=input_ProcessState.s
        h_process_in=input_ProcessState.h

        # --------------  STEP 1 --------------
        
        #The inlet temperature at the steam drum
        
        #T_in_C = #T_SD_in_C=T_process_out_C #The inlet temperature at the solar field is the same than the return of the process
        T_SD_in_K = T_in_C + 273 #= T_SD_in_C+273
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)

        if T_SD_in_K>sat_liq.T: #Ensure the inlet is in liquid phase
            T_SD_in_K=sat_liq.T  

        initial=IAPWS97(P=P_op_Mpa, T=T_SD_in_K)
        #h_SD_in=initial.h #kJ/kg #Not used
        #in_SD_s=initial.s #Not used

        #The outlet temperature at the steam drum
        #T_SD_out_K=sat_liq.T
        #T_SD_out_C=T_SD_out_K-273 #Temperature of saturation at that level

        # --------------- STEP 2 ---------------
        #Steam drum properties
        SD_mass= 200*int(desginDict['n_coll_loop']*desginDict['num_loops']*0.25) # mass in the steam drum [kg]
        
        #Limit conditions
        SD_limit_energy=SD_mass*IAPWS97(P=P_op_Mpa, T=283).h/3600 #Inf. Limit temperature for the steam drum in kWh

        #Minimum conditions
        SD_min_energy=SD_mass*IAPWS97(P=P_op_Mpa, x=0.2).h/3600 #Min temperature for the steam drum in kWh
        
        #Maximum conditions
        SD_max_energy=SD_mass*IAPWS97(P=P_op_Mpa, x=0.6).h/3600 #Max temperature for the steam drum in kWh

        PerdSD=(SD_min_energy-SD_limit_energy)/48 # SD ambient Loss Kwh - All energy is lost after 2 days

        # --------------- STEP 3 ---------------
        
        #Inlet of the Solar field
        T_in_K=sat_liq.T #Same temperature than steam drum
        T_in_C=T_in_K-273
        
        in_s=sat_liq.s #For plotting
        h_in=sat_liq.h #For plotting

        # Outlet of the solar field
        x_design=0.4 #Design steam quality
        outputState=IAPWS97(P=P_op_Mpa, x=x_design)
        T_out_K=outputState.T
        T_out_C=T_out_K-273
        out_s=outputState.s
        h_out=outputState.h
        
        
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,'T_SD_in_K':T_SD_in_K, 
                                       'SD_min_energy':SD_min_energy,'PerdSD':PerdSD, 'SD_mass':SD_mass, 
                                       'SD_limit_energy':SD_limit_energy, 'SD_max_energy':SD_max_energy,
                                       'x_design':x_design, 'h_process_in':h_process_in,
                                       's_process_in':s_process_in, 'out_s':out_s,
                                       'h_out':h_out,'in_s':in_s,'h_in':h_in})

    elif type_integration=="SL_S_PDS":
         
        x_design=0.4
        T_in_K=T_in_C+273 #Temp return of condensates
        
        initial=IAPWS97(P=P_op_Mpa, T=T_in_K)
        h_in=initial.h #kJ/kg
        in_s=initial.s
        sat_liq=IAPWS97(P=P_op_Mpa, x=0)
        outputState=IAPWS97(P=P_op_Mpa, x=x_design)
        T_out_K=outputState.T 
        T_out_C=outputState.T-273 #Temperature of saturation at that level
        
        out_s=outputState.s
        h_out=outputState.h
        
        input_ProcessState=IAPWS97(P=P_op_Mpa, x=1)
        s_process_in=input_ProcessState.s
        h_process_in=input_ProcessState.h
        
        T_avg_K=(T_in_K+T_out_K)/2
        #tempAlm=T_out_K-273
        almacenamiento=IAPWS97(P=P_op_Mpa, T=T_avg_K) #Propiedades en el almacenamiento
        almacenamiento_CP=almacenamiento.cp #Capacidad calorifica del proceso KJ/kg/K
        almacenamiento_rho=almacenamiento.v #volumen específico del agua consumida en m3/kg
        energStorageMax=almVolumen*(1/1000)*(1/almacenamiento_rho)*almacenamiento_CP*(T_out_K-T_in_K)/3600 #Storage capacity in kWh
        
        initial_variables_dict.update({'T_in_C':T_in_C,'T_out_C':T_out_C,
                                 'h_in':h_in,'in_s':in_s,'out_s':out_s,'h_out':h_out,'s_process_in':s_process_in,
                                 'h_process_in':h_process_in,'h_process_in':h_process_in,'x_design':x_design,
                                 'energStorageMax':energStorageMax})
        
    return initial_variables_dict
    
def SHIPcal_auto(origin,inputsDjango,plots,imageQlty,confReport,desginDict,initial_variables_dict,coll_par,modificators,pk): #At this point the energetic and and economical data is computed, the calculation of the equivalent parameters of the collectors in series is left here since the efficiency may depend on the temperature wich may change in recirculation
    
    version = "1.1.10"
    sender=confReport['sender']
    lang=confReport['lang'] #Language
    
    type_integration=desginDict['type_integration']
    n_coll_loop=desginDict['n_coll_loop']
    num_loops=desginDict['num_loops']
    almVolumen=desginDict['almVolumen']
        
    #Defined the variables from the initial_variables_dict
    
    steps_sim=initial_variables_dict['steps_sim']
    step_sim=initial_variables_dict['step_sim']
    
    array_zeros=np.zeros(steps_sim)
    
    theta_i_deg=array_zeros.copy()
    theta_i_rad=array_zeros.copy()
    theta_transv_deg=array_zeros.copy()
    IAM_long=array_zeros.copy()
    IAM_t=array_zeros.copy()
    IAM=array_zeros.copy()
    T_in_K=array_zeros.copy()
    T_out_K=array_zeros.copy()
    flowrate_kgs=array_zeros.copy()
    Perd_termicas=array_zeros.copy()
    flowrate_rec=array_zeros.copy()
    bypass=list()
    Q_prod=array_zeros.copy()
    Q_prod_lim=array_zeros.copy()
    T_SD_K=array_zeros.copy()
    SD_energy=array_zeros.copy()
    Q_prod_rec=array_zeros.copy()
    Q_defocus=array_zeros.copy()
    SOC=array_zeros.copy()
    Q_charg=array_zeros.copy()
    Q_discharg=array_zeros.copy()
    Q_useful=array_zeros.copy()
    flowToHx=array_zeros.copy()
    flowToMix=array_zeros.copy()
    flowDemand=array_zeros.copy()
    T_toProcess_K=array_zeros.copy()
    T_toProcess_C=array_zeros.copy()
    T_alm_K=array_zeros.copy()
    storage_energy=array_zeros.copy()
    x_out=array_zeros.copy()
    Q_prod_steam=array_zeros.copy()
    Q_drum=array_zeros.copy()
    
    #The arrays that won't change are just referenced, the ones that might change are copied.
    
    mofINV=modificators['mofINV']
    mofProd=modificators['mofProd']
    DNI=initial_variables_dict['DNI']
    localMeteo=initial_variables_dict['localMeteo']
    Lat=initial_variables_dict['Lat']
    Positional_longitude=initial_variables_dict['Positional_longitude']
    SUN_ELV=initial_variables_dict['SUN_ELV']
    SUN_AZ=initial_variables_dict['SUN_AZ']
    #time_angle=initial_variables_dict['time_angle']
    temp=initial_variables_dict['temp']
    T_in_C_AR=initial_variables_dict['T_in_C_AR']
    businessModel=initial_variables_dict['businessModel']
    Fuel_price=initial_variables_dict['Fuel_price']
    co2TonPrice=initial_variables_dict['co2TonPrice']
    co2factor=initial_variables_dict['co2factor']
    finance_study=initial_variables_dict['finance_study']
    costRaise=initial_variables_dict['costRaise']
    fuelCostRaise=initial_variables_dict['fuelCostRaise']
    CPI=initial_variables_dict['CPI']
    priceReduction=initial_variables_dict['priceReduction']
    n_years_sim=initial_variables_dict['n_years_sim']
    lim_inf_DNI=initial_variables_dict['lim_inf_DNI']
    m_dot_min_kgs=initial_variables_dict['m_dot_min_kgs']
    coef_flow_rec=initial_variables_dict['coef_flow_rec']
    Boiler_eff=initial_variables_dict['Boiler_eff']
    fluidInput=initial_variables_dict['fluidInput']
    plotPath=initial_variables_dict['plotPath']
    Energy_Before=initial_variables_dict['Energy_Before']
    Energy_Before_annual=initial_variables_dict['Energy_Before_annual']
    Demand=initial_variables_dict['Demand']
    
    #Integration
    x_design=initial_variables_dict['x_design']
    h_process_in=initial_variables_dict['h_process_in']
    energStorageMax=initial_variables_dict['energStorageMax']
    T_in_flag=initial_variables_dict['T_in_flag']
    s_process_in=initial_variables_dict['s_process_in']
    in_s=initial_variables_dict['in_s']
    out_s=initial_variables_dict['out_s']
    h_in=initial_variables_dict['h_in']
    h_out=initial_variables_dict['h_out']
    P_op_Mpa=initial_variables_dict['P_op_Mpa']
    T_in_C=initial_variables_dict['T_in_C']
    T_out_C=initial_variables_dict['T_out_C']
    DELTA_HX=initial_variables_dict['DELTA_HX']
    subcooling=initial_variables_dict['subcooling']
    
    #Integration dependent
    
    if type_integration=="SL_L_RF":
        if fluidInput=="water": 
            h_process_out=initial_variables_dict['h_process_out']
            h_HX_out=initial_variables_dict['h_HX_out']
        
        T_av_process_K=initial_variables_dict['T_av_process_K']
        heatFactor=initial_variables_dict['heatFactor']
        HX_eff=initial_variables_dict['HX_eff']
        T_HX_out_K=initial_variables_dict['T_HX_out_K']
    
    elif type_integration=='SL_L_DRF':
        design_flowrate_kgs = coll_par['mdot_test_permeter']*coll_par['Area_coll']*n_coll_loop
    
    elif type_integration=="SL_L_P" or type_integration=="PL_E_PM":
        pass #Nothing extra is imported
    
    elif type_integration=="SL_L_S" or type_integration=="SL_L_S_PH":
        DELTA_ST=initial_variables_dict['DELTA_ST']
        #flowrate_design_kgs=initial_variables_dict['flowrate_design_kgs']
        T_min_storage=initial_variables_dict['T_min_storage']
        T_max_storage=initial_variables_dict['T_max_storage']
        storage_max_energy=initial_variables_dict['storage_max_energy']
        storage_ini_energy=initial_variables_dict['storage_ini_energy']
        storage_min_energy=initial_variables_dict['storage_min_energy']
        energStorageUseful=initial_variables_dict['energStorageUseful']
        energStorageMax=initial_variables_dict['energStorageMax']
        T_ini_storage=initial_variables_dict['T_ini_storage']
        
    elif type_integration=="SL_L_PS":
        energStorageMax=initial_variables_dict['energStorageMax']
    
    elif type_integration=="SL_S_FW":
        Demand2=initial_variables_dict['Demand2']
        
    elif type_integration=="SL_S_FWS":
        Demand2=initial_variables_dict['Demand2']
        energStorageMax=initial_variables_dict['energStorageMax']
    
    elif type_integration=="SL_S_MW":
        T_in_flag=initial_variables_dict['T_in_flag']
        Demand2=initial_variables_dict['Demand2']
    
    elif type_integration=="SL_S_MWS":
        T_in_flag=initial_variables_dict['T_in_flag']
        Demand2=initial_variables_dict['Demand2']
        energStorageMax=initial_variables_dict['energStorageMax']
    
    elif type_integration=="SL_S_PD_OT":
        h_process_in=initial_variables_dict['h_process_in']
        x_design=initial_variables_dict['x_design']
    
    elif type_integration=="SL_S_PD":
        T_SD_in_K=initial_variables_dict['T_SD_in_K']
        SD_min_energy=initial_variables_dict['SD_min_energy']
        SD_limit_energy=initial_variables_dict['SD_limit_energy']
        PerdSD=initial_variables_dict['PerdSD']
        SD_mass=initial_variables_dict['SD_mass']
        SD_max_energy=initial_variables_dict['SD_max_energy']
    
    elif type_integration=="SL_S_PDS":
        h_process_in=initial_variables_dict['h_process_in']
        x_design=initial_variables_dict['x_design']
        energStorageMax=initial_variables_dict['energStorageMax']
    
    #Collectors
    type_coll=coll_par['type_coll']
    REC_type=coll_par['REC_type']
    Area_coll=coll_par['Area_coll']
    rho_optic_0=coll_par['rho_optic_0']
    Long=coll_par['Long']
    beta=coll_par['beta']
    orient_az_rad=coll_par['orient_az_rad']
    roll=coll_par['roll']
    
    Area=Area_coll*n_coll_loop #Area of aperture per loop [m²] Used later
    Area_total=Area*num_loops #Total area of aperture [m²] Used later
    num_modulos_tot=n_coll_loop*num_loops
    
    #Sender dependent
    
    if sender == 'CIMAV':
        #eta1=coll_par['eta1']
        #eta2=coll_par['eta2']
        #mdot_test=coll_par['mdot_test_permeter']#[kg/sm2]
        blong=coll_par['blong']
        nlong=coll_par['nlong']
        btrans=coll_par['btrans']
        ntrans=coll_par['ntrans']

    else:
        IAMfile_loc=coll_par['IAMfile_loc']
        
    
    meteoDict={'DNI':DNI.tolist(),'localMeteo':localMeteo}
    integrationDesign={'x_design':x_design,'porctSensible':initial_variables_dict['porctSensible'],'almVolumen':almVolumen,'energStorageMax':energStorageMax,
                       'T_out_process_C':T_out_C,'T_in_process_C':T_in_C,'T_out_HX_C':initial_variables_dict['T_out_HX_C']}
    
    # BLOCK 2.2 - SIMULATION ANNUAL LOOP <><><><><><><><><><><><><><><><><><><><><><><><><><><>        
    
    # --> Instant = 0 (Initial conditions)
    lim_inf_DNI_list=[float('inf')] #Records all the inf lim of DNI for CIMAVs collectors
    bypass.append("OFF")
    Q_prod[0]=0
    T_in_K[0]=temp[0] #Ambient temperature 
    T_out_K[0]=temp[0] #Ambient temperature
    energy_stored = 0 #Inititally the storage is always empty if there is one.
    if type_integration=="SL_S_PD":
        #Initial temperature of the steam drum
        T_SD_K[0]=T_SD_in_K #Initial temperature of the storage
        iniState=IAPWS97(P=P_op_Mpa, T=T_SD_in_K)
        SD_energy[0]=(SD_mass)*iniState.h/3600 #Storage capacity in kWh
        
    if type_integration=="SL_L_S" or type_integration=="SL_L_S_PH":
        T_alm_K[0]=T_ini_storage
        storage_energy[0]=storage_ini_energy
        #SOC[i]=100*(T_alm_K[i]-273)/(T_max_storage-273)
        SOC[0]=100*energy_stored/energStorageMax
    
    mismatchDNI=0
    nu_list = [0] #Records the hourly efficiency for CIMAV's collectors
    for i in range(1,steps_sim): #--> <><><><>< ANNUAL SIMULATION LOOP <><><><><><><><><><><><>
        
    # --> IAM calculation
        if sender=='solatom': #Using Solatom's IAMs
            if SUN_ELV[i]>0:
                theta_transv_deg[i],theta_i_deg[i]=theta_IAMs(SUN_AZ[i],SUN_ELV[i],beta,orient_az_rad)
                theta_i_deg[i]=abs(theta_i_deg[i])
                IAM[i]=optic_efficiency_N(theta_transv_deg[i],theta_i_deg[i],n_coll_loop) #(theta_transv_deg[i],theta_i_deg[i],n_coll_loop):
            else:
                IAM_long[i]=0
                IAM_t[i]=0
                IAM[i]=IAM_long[i]*IAM_t[i]
            
        elif sender=='CIMAV': #Using CIMAV's IAMs 
            if SUN_ELV[i]>0 and SUN_ELV[i]<180: #If the sun is above the horizon
                #Calculates the tranversal and longitudinal incidenc angle. This is to say the angle betwwn the proyection  longitudinal/transversal and the area vector from the collector
                theta_transv_deg[i],theta_i_deg[i] = theta_IAMs_v3(SUN_AZ[i],SUN_ELV[i],beta,orient_az_rad,roll)
                
                if coll_par['coll_optic'] == 'concentrator': #If it is a concentrator type collector it will have a default hourly tracking moving the area vector from east yo west, with 0 at midday, -90° at the sunrise.
                    theta_transv_deg[i] = 0
                
                #Dado el angulo de incidencia longitudina/transversal se calcula el IAM correspondiente con los parametros correspondientes
                IAM_long[i] = IAM_calc_weq(blong,nlong,theta_i_deg[i])
                IAM_t[i] = IAM_calc_weq(btrans,ntrans,theta_transv_deg[i])
            else:
                IAM_long[i],IAM_t[i]=0,0
            
            IAM[i]=IAM_long[i]*IAM_t[i]
            
            #In order to calculate the inferior limit of DNI...
            if DNI[i] > 0 and IAM[i] != 0: #If there is DNI and the sun is above the horizon
                
                #if type_integration == 'SL_L_S' or type_integration=="SL_L_S_PH":
                #    T_in_K[i]=T_alm_K[i-1] #In the case of only storage simulation ,the inlet tempereature will be the temperature that the storage had the previous step
                #elif T_in_flag==1:
                if T_in_flag==1: #FOt any other, if a closed circuit is being simulated
                   if bypass[i-1]=="REC" and T_out_K[i-1]>(T_in_C+273): #If the previous hour the collectors were recirculating and their fluid temperature is hotter than the design inlet temperature
                       T_in_K[i]=T_out_K[i-1] #Then their previous temperature is taken as the inlet temperature
                   else:
                       T_in_K[i]=T_in_C+273 #If it was not recirculating, then the inlet temperature is the design temperature
                else: #If  an open circuit is being simulated
                    if bypass[i-1]=="REC" and T_out_K[i-1]>(T_in_C_AR[i]+273): #And the field was reciculating and its fluid temperature is hotter than the crrersponding to the grid in that hour
                        T_in_K[i]=T_out_K[i-1] #THen the inlet temperature is the temperature for recirculation
                    else: #If it was not recirculating, or the grid temperature is hotter
                        T_in_K[i]=T_in_C_AR[i]+273 #Then it takes the temperature from the grid
                        
                T_av_K=(T_in_K[i]+T_out_C+273)/2 #[K] #Gets the expected average temperature of the collectors in order to get the expected Cp of the fluid
                if fluidInput == 'water':
                    Cp_av_KJkgK = IAPWS97(P=P_op_Mpa, T=T_av_K).cp
                    Cp_av_JkgK = Cp_av_KJkgK*1000 #[J/kg·K]
                elif fluidInput=="oil":
                    [rho_av,Cp_av_KJkgK,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_av_K)
                    Cp_av_JkgK = Cp_av_KJkgK*1000 #[J/kg·K]
                elif fluidInput=="moltenSalt":
                    [rho,Cp_av_KJkgK,k,Dv]=moltenSalt(T_av_K)
                    Cp_av_JkgK = Cp_av_KJkgK*1000 #[J/kg·K]
                    
                coll_par.update({'T_in_K':T_in_K[i]})
                F_Rta_eq,F_RU_L_eq,mdot_test_permeter = equiv_coll_series_o1(T_out_C+273,temp[i],DNI[i],IAM[i],Area,Cp_av_JkgK,**coll_par) #Gets the corresponding parameters for all the collectors in serie for its efficiency
                coll_par.update({'F_Rta_eq':F_Rta_eq,'F_RU_L_eq':F_RU_L_eq,'mdot_test_permeter':mdot_test_permeter}) #Update them in the coll_param dictionary
                lim_inf_DNI= F_RU_L_eq*(T_in_K[i]-temp[i])/(F_Rta_eq*IAM[i]) #(eta1*Tm_Ta + eta2*Tm_Ta**2)/rho_optic_0 #eta1 and eta2 are positives and the negative had to be put in the efficiency equation, from the clear of the equation rho_optic_0 is negative again and therefore everything is positive again. 
                nu_list += [F_Rta_eq*IAM[i] -F_RU_L_eq*(T_in_K[i]-temp[i])/DNI[i]] #Calculates the efficiency of the collector for that hour.
                
            else: #If there is no radiation or the sun is under the horizon
                lim_inf_DNI = float('inf')
                nu_list += [0]
                
            lim_inf_DNI_list+=[lim_inf_DNI]
            #In the case of CIMAV sender this calculations are also passed in the integratoins calculation in order to do not calculate them twice.
            
        else:               # Using default's IAMs 
            if SUN_ELV[i]>0:
                theta_transv_deg[i],theta_i_deg[i]=theta_IAMs(SUN_AZ[i],SUN_ELV[i],beta,orient_az_rad)
                theta_i_deg[i]=abs(theta_i_deg[i])
                [IAM_long[i]]=IAM_calc(theta_i_deg[i],0,IAMfile_loc) #Longitudinal
                [IAM_t[i]]=IAM_calc(theta_transv_deg[i],1,IAMfile_loc) #Transversal
                IAM[i]=IAM_long[i]*IAM_t[i]
            else:
                IAM_long[i]=0
                IAM_t[i]=0
                IAM[i]=IAM_long[i]*IAM_t[i]

        if DNI[i]>lim_inf_DNI and SUN_ELV[i]<0: #Error in the meteo file
            mismatchDNI+=DNI[i]
            if mismatchDNI/sum(DNI)>0.02: #If the error is very low we continue with the simulation
                raise ValueError('DNI>0 when SUN_ELV<0. Check meteo file')
        
        
        if DNI[i]>lim_inf_DNI and SUN_ELV[i]>0 and DNI[i]>0:# Status: ON -> There's is and it is anenough DNI to start the system
             
            if type_integration=="SL_L_PS":
                #SL_L_PS Supply level with liquid heat transfer media Parallel integration with storeage pg52 
                
                [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i-1],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1],sender,coll_par)
                [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand[i],energStorageMax)
           
            elif type_integration=="SL_L_DRF":
                [T_out_K[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_kgs[i]]=directopearationSimple(fluidInput,T_out_C,T_in_C,P_op_Mpa,temp[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,theta_i_rad[i],bypass,T_in_flag,T_in_C_AR[i],design_flowrate_kgs,mofProd,sender,coll_par)
                #[Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputdirectopearationSimple(Q_prod[i],Demand[i])
                [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand[i])
            
            elif type_integration=="SL_L_S" or type_integration=="SL_L_S_PH":
                #SL_L_PS Supply level with liquid heat transfer media Parallel integration with storeage pg52 
                
                #[T_out_K[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_kgs[i]]=operationOnlyStorageSimple(fluidInput,T_max_storage,T_alm_K[i-1],P_op_Mpa,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,flowrate_design_kgs,sender,coll_par)
                
                T_out_C_temp = T_out_C
                T_in_C_temp = T_in_C
                
                if (T_alm_K[i-1]+DELTA_ST)>=T_max_storage:
                    T_out_C_temp=T_max_storage-273
                else:
                    T_out_C_temp=(T_alm_K[i-1]+DELTA_ST-273)
                
                if type_integration=="SL_L_S_PH":
                    T_in_C_temp=T_alm_K[i-1]-273+DELTA_HX
                
                [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C_temp,P_op_Mpa,bypass[i-1],T_out_C_temp,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)

                #Storage control
                [T_alm_K[i],storage_energy[i],Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputOnlyStorageSimple(fluidInput,P_op_Mpa,T_min_storage,T_max_storage,almVolumen,T_out_K[i],T_alm_K[i-1],Q_prod[i],energy_stored,Demand[i],energStorageMax,storage_energy[i-1],storage_ini_energy,storage_min_energy,energStorageUseful,storage_max_energy)      
                
 
            elif type_integration=="SL_L_P" or type_integration=="PL_E_PM":     
                #SL_L_P Supply level with liquid heat transfer media Parallel integration pg52 
                
                """
                if fluidInput=="water":
                    flowDemand[i]=Demand[i]/(h_process_in-hProcess_in)#Not used, only for S_L_RF                  
                     
                elif fluidInput=="oil": 
                    T_av_process_K=(T_out_K+T_in_K)/2
                    [rho_av,Cp_av,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_av_process_K)    
                    flowDemand[i]=Demand[i]/(Cp_av*(T_out_K-T_in_K)) #Not used, only for S_L_RF         
                
                elif fluidInput=="moltenSalt": 
                    T_av_process_K=(T_out_K+T_in_K)/2
                    [rho_av,Cp_av,k,Dv]=moltenSalt(T_av_process_K)    
                    flowDemand[i]=Demand[i]/(Cp_av*(T_out_K-T_in_K)) #Not used, only for S_L_RF         
                """
            
                [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)
                [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand[i])
                                    
            elif type_integration=="SL_L_RF":
                #SL_L_RF Supply level with liquid heat transfer media return boost integration pg52
                
                if fluidInput=="water":
                    
                    flowDemand[i]=Demand[i]/(h_process_in-h_process_out)
                    [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)
                    #Corrections in Q_prod and DEemand
                    Q_prodProcessSide=Q_prod[i]*HX_eff #Evaluation of the Energy production after the HX
                    Q_prod[i]=Q_prodProcessSide #I rename the Qprod to QprodProcessSide since this is the energy the system is transfering the process side
                    Demand_HX=Demand[i]*heatFactor #Demand of Energy at the HX
                    [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand_HX)
                        
                    #HX simulation
                    if newBypass=="REC":
                        flowToHx[i]=0   #Valve closed no circulation through the HX. The solar field is recirculating
                        T_toProcess_K[i]=T_in_C+273
                        T_toProcess_C[i]=T_in_C
                    else:
                        [T_toProcess_C[i],flowToMix[i],T_toProcess_K[i],flowToMix[i],flowToHx[i]]=outputFlowsWater(Q_prod_lim[i],P_op_Mpa,h_HX_out,h_process_out,T_in_C+273,flowDemand[i])     
                else: 
                    
                    [rho_av,Cp_av,k_av,Dv_av,Kv_av,thermalDiff_av,Prant_av]=thermalOil(T_av_process_K)    
                    flowDemand[i]=Demand[i]/(Cp_av*(T_out_C-T_in_C))
                    [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)
                    #Corrections in Q_prod and Demand
                    Q_prodProcessSide=Q_prod[i]*HX_eff #Evaluation of the Energy production after the HX
                    Q_prod[i]=Q_prodProcessSide #I rename the Qprod to QprodProcessSide since this is the energy the system is transfering the process side
                    Demand_HX=Demand[i]*heatFactor #Temporary correction of demand for the output function. Afterwards it is corrected again
                    [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand_HX)
                        
                    
                    if newBypass=="REC":
                        flowToHx[i]=0   #Valve closed no circulation through the HX. The solar field is recirculating                         
                        T_toProcess_K[i]=T_in_C+273
                        T_toProcess_C[i]=T_in_C
                    else:
                        [T_toProcess_C[i],flowToMix[i],T_toProcess_K[i],flowToMix[i],flowToHx[i]]=outputFlowsHTF(Q_prod_lim[i],Cp_av,T_HX_out_K,T_in_C+273,flowDemand[i]) 
                          
            elif type_integration=="SL_S_FW" or type_integration=="SL_S_MW":
                #SL_S_FW Supply level with steam for solar heating of boiler feed water without storage              
                
                [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)
                [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand2[i])
            
            elif type_integration=="SL_S_FWS" or type_integration=="SL_S_MWS":
                #SL_S_FW Supply level with steam for solar heating of boiler feed water with storage  
                
                [T_out_K[i],flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationSimple(fluidInput,bypass,T_in_flag,T_in_K[i-1],T_in_C_AR[i],T_out_K[i-1],T_in_C,P_op_Mpa,bypass[i-1],T_out_C,temp[i],theta_i_rad[i],DNI[i],IAM[i],Area,n_coll_loop,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,Q_prod_rec[i-1], sender,coll_par)
                [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand2[i],energStorageMax)     
            
            elif type_integration=="SL_S_PD_OT":
                #SL_S_PD_OT Supply level with steam for direct steam generation
                
                [flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],x_out[i],T_out_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationDSG(bypass,bypass[i-1],T_out_K[i-1],T_in_C,P_op_Mpa,temp[i],REC_type,theta_i_rad[i],DNI[i],Long,IAM[i],Area,n_coll_loop,rho_optic_0,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,x_design,Q_prod_rec[i-1],subcooling)
                [Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand[i])
            
            elif type_integration=="SL_S_PD":
                #SL_S_PD Supply level with steam for direct steam generation
                [flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],T_out_K[i],T_SD_K[i],SD_energy[i],Q_prod_steam[i]]=operationDSG_Rec(m_dot_min_kgs,bypass,SD_min_energy,T_SD_K[i-1],SD_mass,SD_energy[i-1],T_in_C,P_op_Mpa,temp[i],REC_type,theta_i_rad[i],DNI[i],Long,IAM[i],Area,n_coll_loop,rho_optic_0,num_loops,mofProd,x_design,PerdSD)
                [Q_prod_lim[i],Q_defocus[i],Q_useful[i],SD_energy[i],Q_prod_steam[i],Q_drum[i]]=outputDSG_Rec(SD_max_energy,SD_min_energy,SD_energy[i],SD_energy[i-1],Q_prod[i],Q_prod_steam[i],Demand[i])
                
            elif type_integration=="SL_S_PDS":
                #SL_S_PDS Supply level with steam for direct steam generation with water storage
                
                [flowrate_kgs[i],Perd_termicas[i],Q_prod[i],T_in_K[i],x_out[i],T_out_K[i],flowrate_rec[i],Q_prod_rec[i],newBypass]=operationDSG(bypass,bypass[i-1],T_out_K[i-1],T_in_C,P_op_Mpa,temp[i],REC_type,theta_i_rad[i],DNI[i],Long,IAM[i],Area,n_coll_loop,rho_optic_0,num_loops,mofProd,coef_flow_rec,m_dot_min_kgs,x_design,Q_prod_rec[i-1],subcooling)
                #[Q_prod_lim[i],Q_defocus[i],Q_useful[i]]=outputWithoutStorageSimple(Q_prod[i],Demand[i])
                [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand[i],energStorageMax)     
            
        
        
        else: # Status: OFF -> There's not enough DNI to put the solar plant in production     
            
            if type_integration=="SL_L_S" or type_integration=="SL_L_S_PH":
                #SL_L_PS Supply level with liquid heat transfer media Parallel integration with storeage pg52 
                
                [T_out_K[i],Q_prod[i],T_in_K[i]]=offSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i])

                T_alm_K[i] = T_alm_K[i-1]
                SOC[i]=SOC[i-1]
                storage_energy[i]=storage_energy[i-1]
                
                #[T_out_K[i],Q_prod[i],T_in_K[i],SOC[i],T_alm_K[i],storage_energy[i]]=offOnlyStorageSimple(T_alm_K[i-1],energStorageMax,energy_stored,T_alm_K[i-1],storage_energy[i-1],SOC[i-1]) 
                if Demand[i]>0:
                    [T_alm_K[i],storage_energy[i],Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputOnlyStorageSimple(fluidInput,P_op_Mpa,T_min_storage,T_max_storage,almVolumen,T_out_K[i],T_alm_K[i-1],Q_prod[i],energy_stored,Demand[i],energStorageMax,storage_energy[i-1],storage_ini_energy,storage_min_energy,energStorageUseful,storage_max_energy)           
                        
            elif type_integration=="SL_L_PS":
                #SL_L_PS Supply level with liquid heat transfer media Parallel integration with storeage pg52 
                
                Perd_termicas[i] = DNI[i]*Area_total + Q_prod_rec[i-1]*num_loops*1000 #All the energy is lost since the collectors are not working
                [T_out_K[i],Q_prod[i],T_in_K[i],SOC[i]]=offStorageSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i],energStorageMax,energy_stored)
                if Demand[i]>0:
                    [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand[i],energStorageMax)
                        
            elif type_integration=="SL_L_DRF":
                
                Perd_termicas[i] = DNI[i]*Area_total #All the energy is lost since the collectors are not working
                [T_out_K[i],Q_prod[i],T_in_K[i]]=offSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i])
            
            elif type_integration=="SL_L_P" or type_integration=="PL_E_PM" or type_integration=="SL_L_RF":
                #SL_L_P Supply level with liquid heat transfer media Parallel integration pg52 
                
                Perd_termicas[i] = DNI[i]*Area_total + Q_prod_rec[i-1]*num_loops*1000 #All the energy is lost since the collectors are not working
                [T_out_K[i],Q_prod[i],T_in_K[i]]=offSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i])

            elif type_integration=="SL_S_FW" or type_integration=="SL_S_MW":
                #SL_S_FW Supply level with steam for solar heating of boiler feed water without storage 
                
                [T_out_K[i],Q_prod[i],T_in_K[i]]=offSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i])
                
            elif type_integration=="SL_S_FWS" or type_integration=="SL_S_MWS":
                #SL_S_FWS Supply level with steam for solar heating of boiler feed water with storage 
                
                [T_out_K[i],Q_prod[i],T_in_K[i],SOC[i]]=offStorageSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i],energStorageMax,energy_stored)
                if Demand2[i]>0:
                    [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand2[i],energStorageMax)                         
            
            elif type_integration=="SL_S_PD_OT":
                #SL_S_PD_OT Supply level with steam for direct steam generation
                [T_out_K[i],Q_prod[i],T_in_K[i]]=offSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i])
            
            elif type_integration=="SL_S_PD":
                #SL_S_PD Supply level with steam for direct steam generation
                 [T_out_K[i],Q_prod[i],T_in_K[i],T_SD_K[i],SD_energy[i]]=offDSG_Rec(PerdSD,SD_limit_energy,fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i],SD_energy[i-1],SD_mass,T_SD_K[i-1],P_op_Mpa)
                 
            elif type_integration=="SL_S_PDS":
                #SL_S_PDS Supply level with steam for direct steam generation with water storage
                [T_out_K[i],Q_prod[i],T_in_K[i],SOC[i]]=offStorageSimple(fluidInput,bypass,T_in_flag,T_in_C_AR[i],temp[i],energStorageMax,energy_stored)
                if Demand[i]>0:
                    [Q_prod_lim[i],Q_prod[i],Q_discharg[i],Q_charg[i],energy_stored,SOC[i],Q_defocus[i],Q_useful[i]]=outputStorageSimple(Q_prod[i],energy_stored,Demand[i],energStorageMax)
            
    processDict={'T_in_flag':T_in_flag,'T_in_C_AR':T_in_C_AR.tolist(),'T_toProcess_C':T_toProcess_C.tolist()}
    
    #DataFRame summary of the simulation (only for SL_L_P)
    #simulationDF=pd.DataFrame({'DNI':DNI,'T_in':T_in_K-273,'T_out':T_out_K-273,'bypass':bypass,
    #                          'Q_prod':Q_prod,'Q_prod_rec':Q_prod_rec,'flowrate_kgs':flowrate_kgs,
    #                          'flowrate_rec':flowrate_rec,'Q_prod_lim':Q_prod_lim,'Demand':Demand,
    #                          'Q_defocus':Q_defocus})

    #DataFRame summary of the simulation (only for SL_L_S)
    simulationDF=pd.DataFrame({'DNI':DNI,'Q_prod':Q_prod,'Q_charg':Q_charg,'Q_discharg':Q_discharg,'Q_defocus':Q_defocus,'Demand':Demand,'storage_energy':storage_energy,'SOC':SOC,'T_alm_K':T_alm_K-273})
    simulationDF=simulationDF
    
    #%%
    # BLOCK 2.2 - ANUAL INTEGRATION <><><><><><><><><><><><><><><><><><><><><><><><><><><>
    
    if coll_par['auto'] == 'on' and (sum(Q_prod) == 0 or np.isnan(sum(Q_prod))):
        LCOE = float('inf') #Added this possibility because sometimes the jump in temperature is too large for only a few collectors.
        print('It wasnt possible to produce any heaat!!!')
        print('Using (loops,coll per loop) = {} as configuration'.format((num_loops, n_coll_loop)))
        
    else:
        
        Production_max=sum(Q_prod) #Produccion total en kWh. Asumiendo que se consume todo lo producido
        Production_lim=sum(Q_prod_lim) #Produccion limitada total en kWh
        Demand_anual=sum(Demand) #Demanda energética anual
        solar_fraction_max=100*Production_max/Demand_anual #Fracción solar maxima
        
        tonCo2Saved=Production_lim*co2factor #Tons of Co2 saved
        totalDischarged=(sum(Q_discharg))
        totalCharged=(sum(Q_charg))
        totalDefocus = sum(Q_defocus)
        Utilitation_ratio=100*((Production_lim)/(Production_max))
        improvStorage=(100*Production_lim/(Production_lim-totalDischarged))-100 #Assuming discharged = Charged
        solar_fraction_lim=100*(Production_lim)/Demand_anual 
        Energy_module_max=Production_max/num_modulos_tot
        #operation_hours=np.nonzero(Q_prod)
        DNI_anual_irradiation=sum(DNI)/1000 #kWh/year/m2
        #Optic_rho_average=(sum(IAM)*rho_optic_0)/steps_sim
        Perd_term_anual=sum(Perd_termicas)/(1000) #kWh/year

        nonzeroflowrate_kgs = [flowrate_kgs[i] for i in np.nonzero(flowrate_kgs)[0]]

        annualProdDict={'Q_prod':Q_prod.tolist(),'Q_prod_lim':Q_prod_lim.tolist(),'Demand':Demand.tolist(),'Q_charg':Q_charg.tolist(),
                        'totalCharged':totalCharged,'totalDischarged':totalDischarged,'totalDefocus':totalDefocus,
                        'Q_discharg':Q_discharg.tolist(),'Q_defocus':Q_defocus.tolist(),'solar_fraction_max':solar_fraction_max,
                        'solar_fraction_lim':solar_fraction_lim,'improvStorage':improvStorage,'Utilitation_ratio':Utilitation_ratio,
                        'flow_rate_kgs':flowrate_kgs.tolist(), 'flowrate_kgs_average':np.mean(nonzeroflowrate_kgs), 'energStorageMax':energStorageMax,
                        'Energy_module_max':Energy_module_max,}
        
    
    #%%
    # ------------------------------------------------------------------------------------
    # BLOCK 3 - FINANCE SIMULATION -------------------------------------------------------
    # ------------------------------------------------------------------------------------
        
        Break_cost=0 # Init variable
        if finance_study==1 and steps_sim==8759:#This eneters only for yearly simulations with the flag finance_study = 1
    
        # BLOCK 3.1 - PLANT INVESTMENT <><><><><><><><><><><><><><><><><><><><><><><><><><><>
    
            if origin==-2: #If ReSSSPI front-end is calling, then it uses Solatom propietary cost functions
                [Selling_price,Break_cost,OM_cost_year]=SOL_plant_costFunctions(num_modulos_tot,type_integration,almVolumen,fluidInput)
    
            elif origin==-3: #Use the CIMAV's costs functions
                destination=[Lat,Positional_longitude]
                [Selling_price,Break_cost,OM_cost_year]=CIMAV_plant_costFunctions(num_modulos_tot,num_loops,type_integration,almVolumen,fluidInput,type_coll,destination,Area_total) #Returns all the prices in mxn
    
            else: #If othe collector is selected, it uses default cost functions
                #This function calls the standard cost functions, if necessary, please modify them within the function
                [Selling_price,Break_cost,OM_cost_year]=SP_plant_costFunctions(num_modulos_tot,type_integration,almVolumen,fluidInput)
                  
            Selling_price=Selling_price*mofINV
            
        #%%    
        # BLOCK 3.2 - FINANCE MODEL <><><><><><><><><><><><><><><><><><><><><><><><><><><>
            
            if co2TonPrice>0:
                CO2=1
                co2Savings=tonCo2Saved*co2TonPrice
            else:
                CO2=0
                co2Savings=0
            
            # Turnkey model   
            if businessModel=="Llave en mano" or businessModel=="Turnkey project" or businessModel=="turnkey":
                [LCOE,IRR,IRR10,AmortYear,Acum_FCF,FCF,Energy_savings,OM_cost,fuelPrizeArray,Net_anual_savings]=Turn_key(Production_lim,Fuel_price,Boiler_eff,n_years_sim,Selling_price,OM_cost_year,costRaise,co2Savings)
                if lang=="spa":        
                    TIRscript="TIR para el cliente"
                    Amortscript="<b>Amortización: </b> Año "+ str(AmortYear)
                    TIRscript10="TIR para el cliente en 10 años"
                if lang=="eng":
                    TIRscript="IRR for the client"
                    Amortscript="<b>Payback: </b> Year "+ str(AmortYear)
                    TIRscript10="IRR for the client 10 years"
        
            
            # ESCO Energy service company model    
            if businessModel=="Compra de energia" or businessModel=="ESCO" or businessModel=="Renting":
                 #From financing institution poit of view        
                [IRR,IRR10,AmortYear,Acum_FCF,FCF,BenefitESCO,OM_cost,fuelPrizeArray,Energy_savings,Net_anual_savings]=ESCO(priceReduction,Production_lim,Fuel_price,Boiler_eff,n_years_sim,Selling_price,OM_cost_year,costRaise,co2Savings)
                if lang=="spa":    
                    TIRscript="TIR para la ESE"
                    Amortscript="<b>Ahorro en precio actual combustible: </b>"+str(round(100*(1-priceReduction)))+"%" 
                if lang=="eng":   
                    TIRscript="IRR for the ESCO"
                    Amortscript="<b>Savings in fuel cost: </b>"+str(round(100*(1-priceReduction)))+"%" 
        
                #Form client point of view
                AmortYear=0
                Selling_price=0 #No existe inversión
                FCF[0]=0
                
            Energy_savingsList=Net_anual_savings.tolist()
            OMList=OM_cost.tolist()
            fuelPrizeArrayList=fuelPrizeArray.tolist()
            Acum_FCFList=[]
            for i in range(0,len(Acum_FCF)):
                if Acum_FCF[i]<0:
                    Acum_FCFList.append("("+str(int(abs(Acum_FCF[i])))+")")
                else:
                    Acum_FCFList.append(str(int(Acum_FCF[i])))
            
            anual_energy_cost = fuelPrizeArray*Energy_Before_annual
            Energy_savings_mean = np.mean(Net_anual_savings)
            fraction_savings = np.mean(Net_anual_savings/anual_energy_cost)*100
            
            finance={'AmortYear':AmortYear,'finance_study':finance_study,'CO2':CO2,'co2Savings':co2Savings,
                     'fuelPrizeArrayList':fuelPrizeArrayList,'Acum_FCFList':Acum_FCFList,'Energy_savingsList':Energy_savingsList,
                     'TIRscript':TIRscript,'TIRscript10':TIRscript10,'Amortscript':Amortscript,
                     'co2TonPrice':co2TonPrice,'fuelIncremento':fuelCostRaise,'IPC':CPI,'Selling_price':Selling_price,
                     'IRR':IRR,'IRR10':IRR10,'tonCo2Saved':tonCo2Saved,'OM_cost_year':OMList, 'LCOE':LCOE,
                     'anual_energy_cost':anual_energy_cost.tolist(),
                     'Energy_savings_mean':Energy_savings_mean}
        
        else:
            n_years_sim=0 #No finance simulation
            Acum_FCF=np.array([]) #No finance simulation
            FCF=np.array([]) #No finance simulation
            AmortYear=0 #No finance simulation
            Selling_price=0 #No finance simulation
            
#%%
# ------------------------------------------------------------------------------------
# BLOCK 4 - PLOT GENERATION ----------------------------------------------------------
# ------------------------------------------------------------------------------------
    if coll_par['auto'] == 'off':
        plotVars={'lang':lang,'Production_max':Production_max,'Production_lim':Production_lim,
                  'Perd_term_anual':Perd_term_anual,'DNI_anual_irradiation':DNI_anual_irradiation,
                  'Area':Area,'num_loops':num_loops,'imageQlty':imageQlty,'plotPath':plotPath,'Energy_Before_annual':Energy_Before_annual,
                  'Demand':Demand.tolist(),'Q_prod':Q_prod.tolist(),'Q_prod_lim':Q_prod_lim.tolist(),'type_integration':type_integration,
                  'Q_charg':Q_charg.tolist(),'Q_discharg':Q_discharg.tolist(),'DNI':DNI.tolist(),'SOC':SOC.tolist(),
                  'Q_useful':Q_useful.tolist(),'Q_defocus':Q_defocus.tolist(),'T_alm_K':T_alm_K.tolist(),
                  'n_years_sim':n_years_sim,'Acum_FCF':Acum_FCF.tolist(),'FCF':FCF.tolist(),'m_dot_min_kgs':m_dot_min_kgs,
                  'steps_sim':steps_sim,'AmortYear':AmortYear,'Selling_price':Selling_price,
                  'in_s':in_s,'out_s':out_s,'T_in_flag':T_in_flag,'Fuel_price':Fuel_price,'Boiler_eff':Boiler_eff,
                  'T_in_C':T_in_C,'T_in_C_AR':T_in_C_AR.tolist(),'T_out_C':T_out_C,
                  'outProcess_s':s_process_in,'T_out_process_C':T_out_C,'P_op_bar':P_op_Mpa*10,
                  'x_design':x_design,'h_in':h_in,'h_out':h_out,'hProcess_out':h_process_in,'outProcess_h':h_process_in,
                  'Break_cost':Break_cost,'sender':sender,'origin':origin}
        
        # Plot functions
        
        # Plots for annual simulations
        if steps_sim==8759:
            if plots[0]==1: #(0) Sankey plot
                image_base64,sankeyDict=SankeyPlot(sender,origin,lang,Production_max,Production_lim,Perd_term_anual,DNI_anual_irradiation,Area,num_loops,imageQlty,plotPath)
            if plots[0]==0: #(0) Sankey plot -> no plotting
                sankeyDict={'Production':0,'raw_potential':0,'Thermal_loss':0,'Utilization':0}
            if plots[1]==1: #(1) Production week Winter & Summer
                prodWinterPlot(sender,origin,lang,Demand,Q_prod,Q_prod_lim,type_integration,Q_charg,Q_discharg,DNI,plotPath,imageQlty)   
                prodSummerPlot(sender,origin,lang,Demand,Q_prod,Q_prod_lim,type_integration,Q_charg,Q_discharg,DNI,plotPath,imageQlty)  
            if plots[2]==1 and finance_study==1: #(2) Plot Finance
                financePlot(sender,origin,lang,n_years_sim,Acum_FCF,FCF,m_dot_min_kgs,steps_sim,AmortYear,Selling_price,plotPath,imageQlty)
            if plots[3]==1: #(3)Plot of Storage first week winter & summer 
                storageWinter(sender,origin,lang,Q_prod,Q_charg,Q_prod_lim,Q_useful,Demand,Q_defocus,Q_discharg,type_integration,T_alm_K,SOC,plotPath,imageQlty)    
                storageSummer(sender,origin,lang,Q_prod,Q_charg,Q_prod_lim,Q_useful,Demand,Q_defocus,Q_discharg,type_integration,T_alm_K,SOC,plotPath,imageQlty)    
            if plots[4]==1: #(4) Plot Prod months
                output_excel=prodMonths(sender,origin,Q_prod,Q_prod_lim,DNI,Demand,lang,plotPath,imageQlty)
                output_excel=output_excel
            if plots[15]==1: #(14) Plot Month savings
                output_excel2=savingsMonths(sender,origin,Q_prod_lim,Energy_Before,Fuel_price,Boiler_eff,lang,plotPath,imageQlty)
                output_excel2=output_excel2
    
        
        # Plots for non-annual simulatios (With annual simuations you cannot see anything)
        if steps_sim!=8759:
            if plots[5]==1: #(5) Theta angle Plot
                thetaAnglesPlot(sender,origin,step_sim,steps_sim,theta_i_deg,theta_transv_deg,plotPath,imageQlty)
            if plots[6]==1: #(6) IAM angles Plot
                IAMAnglesPlot(sender,origin,step_sim,IAM_long,IAM_t,IAM,plotPath,imageQlty) 
            if plots[7]==1: #(7) Plot Overview (Demand vs Solar Radiation) 
                demandVsRadiation(sender,origin,lang,step_sim,Demand,Q_prod,Q_prod_lim,Q_prod_rec,steps_sim,DNI,plotPath,imageQlty)
            if plots[8]==1: #(8) Plot flowrates  & Temp & Prod
                flowRatesPlot(sender,origin,step_sim,steps_sim,flowrate_kgs,flowrate_rec,num_loops,flowDemand,flowToHx,flowToMix,m_dot_min_kgs,T_in_K,T_toProcess_C,T_out_K,T_alm_K,plotPath,imageQlty)
            if plots[9]==1: #(9)Plot Storage non-annual simulation  
                storageNonAnnual(sender,origin,SOC,Q_useful,Q_prod,Q_charg,Q_prod_lim,step_sim,Demand,Q_defocus,Q_discharg,steps_sim,plotPath,imageQlty)
                 
            if plots[16]==1 and type_integration=='SL_S_PD': #(16)Plot for SL_S_PD
                SL_S_PDR_Plot(sender,origin,step_sim,steps_sim,SD_min_energy,SD_max_energy,Q_prod,Q_prod_steam,SD_energy,T_in_K,T_out_K,T_SD_K,plotPath,imageQlty)
            if plots[17]==1 and type_integration=='SL_S_PD': #(17)Plot for SL_S_PD 
                storageNonAnnualSL_S_PDR(sender,origin,SOC,Q_useful,Q_prod_steam,Q_prod,Q_drum,Q_charg,Q_prod_lim,step_sim,Demand,Q_defocus,Q_discharg,steps_sim,plotPath,imageQlty)
                
        # Property plots
        if fluidInput=="water" or fluidInput=="steam": #WATER or STEAM
            if plots[10]==1: #(10) Mollier Plot for s-t for Water
                mollierPlotST(sender,origin,lang,type_integration,in_s,out_s,T_in_flag,T_in_C,T_in_C_AR,T_out_C,s_process_in,T_out_C,P_op_Mpa*10,x_design,plotPath,imageQlty)              
            if plots[11]==1: #(11) Mollier Plot for s-h for Water 
                mollierPlotSH(sender,origin,lang,type_integration,h_in,h_out,h_process_in,h_process_in,in_s,out_s,T_in_flag,T_in_C,T_in_C_AR,T_out_C,s_process_in,T_out_C,P_op_Mpa*10,x_design,plotPath,imageQlty)  
        if fluidInput=="oil": 
            if plots[12]==1:
                rhoTempPlotOil(sender,origin,lang,T_out_C,plotPath,imageQlty) #(12) Plot thermal oil properties Rho & Cp vs Temp
            if plots[13]==1:
                viscTempPlotOil(sender,origin,lang,T_out_C,plotPath,imageQlty) #(13) Plot thermal oil properties Viscosities vs Temp        
        if fluidInput=="moltenSalt": 
            if plots[12]==1:
                rhoTempPlotSalt(sender,origin,lang,T_out_C,plotPath,imageQlty) #(12) Plot thermal oil properties Rho & Cp vs Temp
            if plots[13]==1:
                viscTempPlotSalt(sender,origin,lang,T_out_C,plotPath,imageQlty) #(13) Plot thermal oil properties Viscosities vs Temp        
    
    
        
        # Other plots
        if plots[14]==1: #(14) Plot Production
            productionSolar(sender,origin,lang,step_sim,DNI,m_dot_min_kgs,steps_sim,Demand,Q_prod,Q_prod_lim,Q_charg,Q_discharg,type_integration,plotPath,imageQlty)
           
        
    #%%
    # ------------------------------------------------------------------------------------
    # BLOCK 5 - REPORT GENERATION ----------------------------------------------------------
    # ------------------------------------------------------------------------------------
        
        # Create Report with results (www.ressspi.com uses a customized TEMPLATE called in the function "reportOutput"
        if steps_sim==8759: #The report is only available when annual simulation is performed
            if origin==-2:
                fileName="results"+str(pk)
                reportsVar={'logo_output':'no_logo','date':inputsDjango['date'],'type_integration':type_integration,
                            'fileName':fileName,'reg':pk,
                            'Area_total':Area_total,'n_coll_loop':n_coll_loop,
                            'num_loops':num_loops,'m_dot_min_kgs':m_dot_min_kgs}
    
    
    
                
                reportsVar.update(inputsDjango)
                reportsVar.update(initial_variables_dict.get('inputs',{}))
                reportsVar.update(finance)
                reportsVar.update(confReport)
                reportsVar.update(annualProdDict)
                reportsVar.update(sankeyDict)
                reportsVar.update(meteoDict)
                reportsVar.update(processDict)
                reportsVar.update(integrationDesign)   
                template_vars=reportOutput(origin,reportsVar,-1,"",pk,version,os.path.dirname(os.path.dirname(__file__))+'/ressspi',os.path.dirname(os.path.dirname(__file__)),Energy_Before_annual,sankeyDict)
            elif origin==-3:
                template_vars={}
                reportsVar={'type_integration':type_integration,'coll_weight':coll_par['coll_weight'],
                            'energyStored':energy_stored,'m_dot_min_kgs':m_dot_min_kgs,
                            'Area_total':Area_total,'energStorageMax':energStorageMax,
                            'Demand_anual':Demand_anual,'solar_fraction_max':solar_fraction_max,
                            'solar_fraction_lim':solar_fraction_lim,'DNI_anual_irradiation':DNI_anual_irradiation}
                reportsVar.update({'AmortYear':AmortYear,'CO2':CO2,'co2Savings':co2Savings,'fuelPrizeArray':fuelPrizeArray,
                                   'Energy_savingsList':Energy_savingsList,'co2TonPrice':co2TonPrice,'fraction_savings':fraction_savings,
                                   'Selling_price':Selling_price,'IRR':IRR,'tonCo2Saved':tonCo2Saved,'IRR10':IRR10,
                                   'OM_cost_year':OMList, 'LCOE':LCOE,'anual_energy_cost':anual_energy_cost.tolist(),
                                   'Energy_savings_mean':Energy_savings_mean}) #Finance fields
                reportsVar.update(annualProdDict)
                
                template_vars={'version':version,'logo_output':'no_logo','type_integration':type_integration,
                            'energyStored':energy_stored,"location":localMeteo,
                            'Area_total':Area_total,'n_coll_loop':n_coll_loop,'energStorageMax':energStorageMax,
                            'num_loops':num_loops,'m_dot_min_kgs':m_dot_min_kgs,
                            'Production_max':Production_max,'Production_lim':Production_lim,
                            'Demand_anual':Demand_anual,'solar_fraction_max':solar_fraction_max,
                            'solar_fraction_lim':solar_fraction_lim,'DNI_anual_irradiation':DNI_anual_irradiation}
                reportsVar.update(initial_variables_dict.get('inputs',{}))
                template_vars.update(finance)
                template_vars.update(confReport)
                template_vars.update(annualProdDict)
                template_vars.update(modificators)
                reportOutputOffline(template_vars)
            elif origin == 1:
                template_vars={} 
                reportsVar={'version':version,'logo_output':'no_logo','type_integration':type_integration,
                            'energyStored':energy_stored,"location":localMeteo,'fraction_savings':fraction_savings,
                            'Area_total':Area_total,'n_coll_loop':n_coll_loop,'energStorageMax':energStorageMax,
                            'num_loops':num_loops,'m_dot_min_kgs':m_dot_min_kgs,
                            'Production_max':Production_max,'Production_lim':Production_lim,
                            'Demand_anual':Demand_anual,'solar_fraction_max':solar_fraction_max,
                            'solar_fraction_lim':solar_fraction_lim,'DNI_anual_irradiation':DNI_anual_irradiation}
                reportsVar.update(finance)
                reportsVar.update(confReport)
                reportsVar.update(annualProdDict)
                reportsVar.update(modificators)
                if origin==0 or origin == 1:
                    reportOutputOffline(reportsVar)            
            else:
                template_vars={} 
                reportsVar={'version':version,'logo_output':'no_logo','type_integration':type_integration,
                            'energyStored':energy_stored,"location":localMeteo,
                            'Area_total':Area_total,'n_coll_loop':n_coll_loop,'energStorageMax':energStorageMax,
                            'num_loops':num_loops,'m_dot_min_kgs':m_dot_min_kgs,
                            'Production_max':Production_max,'Production_lim':Production_lim,
                            'Demand_anual':Demand_anual,'solar_fraction_max':solar_fraction_max,
                            'solar_fraction_lim':solar_fraction_lim,'DNI_anual_irradiation':DNI_anual_irradiation}
                reportsVar.update(finance)
                reportsVar.update(confReport)
                reportsVar.update(annualProdDict)
                reportsVar.update(modificators)
                if origin==0:
                    reportOutputOffline(reportsVar)
        else:
            template_vars={}
            reportsVar={}
            
        return(template_vars,plotVars,reportsVar,version)
    
    return(LCOE)


# ----------------------------------- END SHIPcal -------------------------
# -------------------------------------------------------------------------
#%% 
"""
# Variables needed for calling SHIPcal from terminal
    
#Plot Control ---------------------------------------
imageQlty=200

plots=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # Put 1 in the elements you want to plot. Example [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0] will plot only plots #0, #8 and #9
#(0) A- Sankey plot
#(1) A- Production week Winter & Summer
#(2) A- Plot Finance
#(3) A- Plot of Storage first week winter & summer
#(4) A- Plot Prod months
#(5) NA- Theta angle Plot
#(6) NA- IAM angles Plot
#(7) NA- Plot Overview (Demand vs Solar Radiation)
#(8) NA- Plot flowrates  & Temp & Prod
#(9) NA- Plot Storage non-annual simulation 
#(10) P- Mollier Plot for s-t for Water
#(11) P- Mollier Plot for s-h for Water
#(12) P- Plot thermal oil/molten salt properties Rho & Cp vs Temp
#(13) P- Plot thermal oil/molten salt properties Viscosities vs Temp 
#(14) Plot Production 
#(15) A- Plot Month savings 
#(16) NA- Plot for SL_S_PD



finance_study=1

month_ini_sim=1
day_ini_sim=1
hour_ini_sim=1

month_fin_sim=12
day_fin_sim=31
hour_fin_sim=24



# -------------------- FINE TUNNING CONTROL ---------
mofINV=1 #Sobre el coste de inversion
mofDNI=1  #Corrección a fichero Meteonorm
mofProd=1 #Factor de seguridad a la producción de los módulos

# -------------------- SIZE OF THE PLANT ---------
num_loops=290
n_coll_loop=10

#SL_L_P -> Supply level liquid parallel integration without storage
#SL_L_PS -> Supply level liquid parallel integration with storage
#SL_L_RF -> Supply level liquid return flow boost
#SL_L_DRF -> Supply level liquid return flow boost with no heat exchanger (The simplest)
#SL_L_S -> Storage
#SL_L_S_PH -> Storage preheat
#SL_S_FW -> Supply level solar steam for heating of boiler feed water without storage
#SL_S_FWS -> Supply level solar steam for heating of boiler feed water with storage
#SL_S_PD_OT -> Supply level solar steam for direct solar steam generation #For CIMAV only works for a large number of plane collectors +30
#PL_E_PM ->
#SL_S_MW ->
#SL_S_MWS ->
#SL_S_PD ->
#SL_S_PDS -> #For CIMAV only works for a large number of plane collectors +20

type_integration="SL_L_P" 
almVolumen=4300000 #litros

# --------------------------------------------------
confReport={'lang':'spa','sender':'CIMAV','cabecera':'Resultados de la <br> simulación','mapama':0}
modificators={'mofINV':mofINV,'mofDNI':mofDNI,'mofProd':mofProd}
desginDict={'num_loops':num_loops,'n_coll_loop':n_coll_loop,'type_integration':type_integration,'almVolumen':almVolumen}
simControl={'finance_study':finance_study,'mes_ini_sim':month_ini_sim,'dia_ini_sim':day_ini_sim,'hora_ini_sim':hour_ini_sim,'mes_fin_sim':month_fin_sim,'dia_fin_sim':day_fin_sim,'hora_fin_sim':hour_fin_sim}    
# ---------------------------------------------------

origin=-3 #0 if new record; -2 if it comes from www.ressspi.com

if origin==0:
    #To perform simulations from command line using hardcoded inputs
    inputsDjango={}
    last_reg=666
elif origin==-3:
    inputsDjango = {'T_in_flag': 1,
                    'almVolumen': 4300000,
                    'businessModel': 'turnkey',
                    'co2TonPrice': 0.0,
                    'co2factor': 0.0,
                    'collector_type': 'POWER THROUGH 250 INVENTIVE POWER.txt',
                    'date': '2020-05-08',
                    'demand': 94171.0,
                    'demandUnit': '666',
                    'email': 'ja.arpa97@gmail.com',
                    'every_day': True,
                    'every_month': True,
                    'fluid': 'water',
                    'fuel': 'gas_licuado_petroleo',
                    'fuelPrice': 1.3791643373493976,
                    'fuelUnit': 1.0,
                    'hourEND': 24,
                    'hourINI': 0,
                    'industry': 'MineraGaby',
                    'location': 'Rosario.dat',
                    'n_coll_loop': 10,
                    'name': '',
                    'num_loops': 290.0,
                    'pais': 'Argentina',
                    'pressure': 1.0,
                    'pressureUnit': '1',
                    'rable_coll_type': 'POWER THROUGH 250 INVENTIVE POWER',
                    'semana': ['0', '1', '2', '3', '4', '5', '6'],
                    'surface': 40000.0,
                    'tempIN': 52.86,
                    'tempOUT': 82.6,
                    'type_integration': 'SL_L_S',
                    'year': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']}
    last_reg=666
    
else:
    #To perform simulations from command line using inputs like if they were from django
    inputsDjango={'pressureUnit':'bar',
                  'pressure':30,
                  'demand':1875*8760,
                  'demandUnit':'kWh',
                  'hourEND':24,
                  'hourINI':1,
                  'Jan':1/12,
                  'Feb':1/12,
                  'Mar':1/12,
                  'Apr':1/12,
                  'May':1/12,
                  'Jun':1/12,
                  'Jul':1/12,
                  'Aug':1/12,
                  'Sep':1/12,
                  'Oct':1/12,
                  'Nov':1/12,
                  'Dec':1/12,
                  'Mond':0.143,
                  'Tues':0.143,
                  'Wend':0.143,
                  'Thur':0.143,
                  'Fri':0.143,
                  'Sat':0.143,
                  'Sun':0.143,
                  'date':'2020-05-08',
                  'name':'jaarpa',
                  'industry':'comparison_test',
                  'email':'jaarpa97@gmail.com',
                  'sectorIndustry':'developing',
                  'fuel':'Gasoil-B',
                  'fuelPrice':0.05,
                  'co2TonPrice':0,
                  'co2factor':1,
                  'fuelUnit':'kWh',
                  'businessModel':'turnkey',
                  'location':'Bakersfield',
                  'location_aux':'',
                  'surface':None,
                  'terrain':'',
                  'orientation':'NS',
                  'inclination':'flat',
                  'shadows':'free',
                  'distance':None,
                  'process':'',
                  'fluid':'steam',
                  'connection':'',
                  'tempOUT':235,
                  'tempIN':20,
                 }
    
    last_reg=666

    #inputsDjango= {'date': '2018-11-04', 'name': 'miguel', 'email': 'mfrasquetherraiz@gmail.com', 'industry': 'Example', 'sectorIndustry': 'Food_beverages', 'fuel': 'Gasoil-B', 'fuelPrice': 0.063, 'co2TonPrice': 0.0, 'co2factor': 0.00027, 'fuelUnit': 'eur_kWh', 'businessModel': 'turnkey', 'location': 'Sevilla', 'location_aux': '', 'surface': 1200, 'terrain': 'clean_ground', 'distance': 35, 'orientation': 'NS', 'inclination': 'flat', 'shadows': 'free', 'fluid': 'water', 'pressure': 6.0, 'pressureUnit': 'bar', 'tempIN': 80.0, 'tempOUT': 150.0, 'connection': 'storage', 'process': '', 'demand': 1500.0, 'demandUnit': 'MWh', 'hourINI': 8, 'hourEND': 18, 'Mond': 0.167, 'Tues': 0.167, 'Wend': 0.167, 'Thur': 0.167, 'Fri': 0.167, 'Sat': 0.167, 'Sun': 0.0, 'Jan': 0.083, 'Feb': 0.083, 'Mar': 0.083, 'Apr': 0.083, 'May': 0.083, 'Jun': 0.083, 'Jul': 0.083, 'Aug': 0.083, 'Sep': 0.083, 'Oct': 0.083, 'Nov': 0.083, 'Dec': 0.083, 'last_reg': 273}
    #last_reg=inputsDjango['last_reg']
    

version, initial_variables_dict, coll_par, integration_Dict = SHIPcal_prep(origin,inputsDjango,confReport,modificators,simControl)
    
initial_variables_dict = SHIPcal_integration(desginDict,initial_variables_dict, integration_Dict) #This second section of SHIPcal updates the integration variables depending on the type of integrations. This will be used mainly to iterate over the storage capacity.
#coll_par.update({'auto':'on'})
#LCOE = SHIPcal_auto(origin,inputsDjango,plots,imageQlty,confReport,desginDict,initial_variables_dict,coll_par,modificators,last_reg)
#print(LCOE)
coll_par.update({'auto':'off'})
[jSonResults,plotVars,reportsVar,version] = SHIPcal_auto(origin,inputsDjango,plots,imageQlty,confReport,desginDict,initial_variables_dict,coll_par,modificators,last_reg)
"""
