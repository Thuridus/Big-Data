import requests
import json
import pywebhdfs.webhdfs
import time
import quandl
import pandas
import datetime
import os
import socket
import kafka


def import_fse(quandl_companies_list, quandl_start_date, quandl_end_date, hdfs_export_path, hdfs_connection, kafka_producer):
    hdfs_export_filename = hdfs_export_path + "/quandl_fse.csv"
    resultdf = pandas.DataFrame()

    for company in quandl_companies_list:
        data = quandl.get("FSE/" + company, start_date = quandl_start_date, end_date = quandl_end_date)
        data['Share'] = company
        resultdf = pandas.concat([resultdf, data])
    
    resultdf = resultdf[['Share','Open','High','Low', 'Close', 'Change', 'Traded Volume', 'Turnover', 'Last Price of the Day', 'Daily Traded Units','Daily Turnover']]
    resultdf.groupby('Share')
    
    if hdfs_connection.exists_file_dir(hdfs_export_filename):
        hdfs_connection.delete_file_dir(hdfs_export_filename)

    hdfs_connection.create_file(hdfs_export_filename, resultdf.to_csv(sep=";",index=True, line_terminator='\n'), permission=777)
    kafka_producer.send("new_data_available", hdfs_export_filename)


def import_infections(import_url, hdfs_connection, hdfs_path_infection, kafka_producer):
    response = requests.get(import_url)
    jsonresponse = response.json()["records"]
    hdfs_export_filename = hdfs_path_infection + "/infections.cvs"

    responsedf = pandas.json_normalize(jsonresponse)

    if hdfs_connection.exists_file_dir(hdfs_export_filename):
        hdfs_connection.delete_file_dir(hdfs_export_filename)
    
    hdfs_connection.create_file(hdfs_export_filename, responsedf.to_csv(sep=";",index=False, line_terminator='\n'), permission=777)
    kafka_producer.send("new_data_available", hdfs_export_filename)


hdfspath = "http://" + str(socket.gethostbyname("knox-apache-knox-helm-svc")) + ":8080"
enddate = datetime.date.today().strftime("%Y-%m-%d")
startdate = "2020-01-01"
quandl_companies = json.loads("{\"1COV_X\": [\"1COV_X\", \"Covestro AG (1COV_X)\"], \"2HR_X\": [\"2HR_X\", \"H&R (2HR_X)\"], \"AAD_X\": [\"AAD_X\", \"Amadeus FiRe AG (AAD_X)\"], \"AB1_X\": [\"AB1_X\", \"Air Berlin Plc (AB1_X)\"], \"ADS_X\": [\"ADS_X\", \"Adidas (ADS_X)\"], \"ADV_X\": [\"ADV_X\", \"Adva Se (ADV_X)\"], \"AFX_X\": [\"AFX_X\", \"Carl Zeiss Meditec (AFX_X)\"], \"AIR_X\": [\"AIR_X\", \"Airbus Group (eads N.v.) (AIR_X)\"], \"AIXA_X\": [\"AIXA_X\", \"Aixtron Se (AIXA_X)\"], \"ALV_X\": [\"ALV_X\", \"Allianz Se (ALV_X)\"], \"ANN_X\": [\"ANN_X\", \"Deutsche Annington Immobilien Se (ANN_X)\"], \"AOX_X\": [\"AOX_X\", \"alstria office REIT-AG (AOX_X)\"], \"ARL_X\": [\"ARL_X\", \"Aareal Bank (ARL_X)\"], \"B5A_X\": [\"B5A_X\", \"Bauer Aktiengesellschaft (B5A_X)\"], \"BAF_X\": [\"BAF_X\", \"Balda (BAF_X)\"], \"BAS_X\": [\"BAS_X\", \"Basf Se (BAS_X)\"], \"BAYN_X\": [\"BAYN_X\", \"Bayer (BAYN_X)\"], \"BBZA_X\": [\"BBZA_X\", \"Bb Biotech (BBZA_X)\"], \"BC8_X\": [\"BC8_X\", \"Bechtle (BC8_X)\"], \"BDT_X\": [\"BDT_X\", \"Bertrandt (BDT_X)\"], \"BEI_X\": [\"BEI_X\", \"Beiersdorf Aktiengesellschaft (BEI_X)\"], \"BIO3_X\": [\"BIO3_X\", \"Biotest  Vz (BIO3_X)\"], \"BMW_X\": [\"BMW_X\", \"Bmw St (BMW_X)\"], \"BNR_X\": [\"BNR_X\", \"Brenntag (BNR_X)\"], \"BOSS_X\": [\"BOSS_X\", \"Hugo Boss (BOSS_X)\"], \"BYW6_X\": [\"BYW6_X\", \"Baywa Vna (BYW6_X)\"], \"CBK_X\": [\"CBK_X\", \"Commerzbank (CBK_X)\"], \"CEV_X\": [\"CEV_X\", \"Centrotec Sustainable (CEV_X)\"], \"CLS1_X\": [\"CLS1_X\", \"Celesio (CLS1_X)\"], \"COK_X\": [\"COK_X\", \"Cancom Se (COK_X)\"], \"COM_X\": [\"COM_X\", \"comdirect bank AG (COM_X)\"], \"CON_X\": [\"CON_X\", \"Continental (CON_X)\"], \"COP_X\": [\"COP_X\", \"Compugroup Medical (COP_X)\"], \"CWC_X\": [\"CWC_X\", \"Cewe Stiftung & Co. Kgaa (CWC_X)\"], \"DAI_X\": [\"DAI_X\", \"Daimler (DAI_X)\"], \"DB1_X\": [\"DB1_X\", \"Deutsche B\u00c3\u00b6rse (DB1_X)\"], \"DBAN_X\": [\"DBAN_X\", \"Deutsche Beteiligungs AG (DBAN_X)\"], \"DBK_X\": [\"DBK_X\", \"Deutsche Bank (DBK_X)\"], \"DEQ_X\": [\"DEQ_X\", \"Deutsche Euroshop (DEQ_X)\"], \"DEX_X\": [\"DEX_X\", \"Delticom (DEX_X)\"], \"DEZ_X\": [\"DEZ_X\", \"Deutz (DEZ_X)\"], \"DIC_X\": [\"DIC_X\", \"DIC Asset AG (DIC_X)\"], \"DLG_X\": [\"DLG_X\", \"Dialog Semiconductor Plc (DLG_X)\"], \"DPW_X\": [\"DPW_X\", \"Deutsche Post (DPW_X)\"], \"DRI_X\": [\"DRI_X\", \"Drillisch (DRI_X)\"], \"DRW3_X\": [\"DRW3_X\", \"Dr\u00c3\u00a4gerwerk  & Co. Kgaa Vz (DRW3_X)\"], \"DTE_X\": [\"DTE_X\", \"Deutsche Telekom (DTE_X)\"], \"DUE_X\": [\"DUE_X\", \"D\u00c3\u00bcrr (DUE_X)\"], \"DWNI_X\": [\"DWNI_X\", \"Deutsche Wohnen (DWNI_X)\"], \"EOAN_X\": [\"EOAN_X\", \"E.on Se (EOAN_X)\"], \"EON_X\": [\"EON_X\", \"E.on Se (EON_X)\"], \"EVD_X\": [\"EVD_X\", \"CTS Eventim (EVD_X)\"], \"EVK_X\": [\"EVK_X\", \"Evonik Industries (EVK_X)\"], \"EVT_X\": [\"EVT_X\", \"Evotec (EVT_X)\"], \"FIE_X\": [\"FIE_X\", \"Fielmann (FIE_X)\"], \"FME_X\": [\"FME_X\", \"Fresenius Medical Care  & Co. Kgaa St (FME_X)\"], \"FNTN_X\": [\"FNTN_X\", \"Freenet (FNTN_X)\"], \"FPE3_X\": [\"FPE3_X\", \"Fuchs Petrolub  Vz (FPE3_X)\"], \"FRA_X\": [\"FRA_X\", \"Fraport (FRA_X)\"], \"FRE_X\": [\"FRE_X\", \"Fresenius Se & Co. Kgaa (FRE_X)\"], \"G1A_X\": [\"G1A_X\", \"GEA AG (G1A_X)\"], \"GBF_X\": [\"GBF_X\", \"Bilfinger Se (GBF_X)\"], \"GFJ_X\": [\"GFJ_X\", \"Gagfah S.a. (GFJ_X)\"], \"GFK_X\": [\"GFK_X\", \"Gfk Se (GFK_X)\"], \"GIL_X\": [\"GIL_X\", \"Dmg Mori Seiki (GIL_X)\"], \"GLJ_X\": [\"GLJ_X\", \"Grenkeleasing (GLJ_X)\"], \"GMM_X\": [\"GMM_X\", \"Grammer (GMM_X)\"], \"GSC1_X\": [\"GSC1_X\", \"Gesco (GSC1_X)\"], \"GWI1_X\": [\"GWI1_X\", \"Gerry Weber International (GWI1_X)\"], \"GXI_X\": [\"GXI_X\", \"Gerresheimer (GXI_X)\"], \"HAB_X\": [\"HAB_X\", \"Hamborner Reit AG (HAB_X)\"], \"HAW_X\": [\"HAW_X\", \"Hawesko Holding (HAW_X)\"], \"HBH3_X\": [\"HBH3_X\", \"Hornbach Holding Ag (HBH3_X)\"], \"HDD_X\": [\"HDD_X\", \"Heidelberger Druckmaschinen (HDD_X)\"], \"HEI_X\": [\"HEI_X\", \"Heidelbergcement (HEI_X)\"], \"HEN3_X\": [\"HEN3_X\", \"Henkel  & Co. Kgaa Vz (HEN3_X)\"], \"HHFA_X\": [\"HHFA_X\", \"HHLA AG (Hamburger Hafen und Logistik) (HHFA_X)\"], \"HNR1_X\": [\"HNR1_X\", \"Hannover R\u00c3\u00bcck Se (HNR1_X)\"], \"HOT_X\": [\"HOT_X\", \"Hochtief (HOT_X)\"], \"IFX_X\": [\"IFX_X\", \"Infineon Technologies (IFX_X)\"], \"INH_X\": [\"INH_X\", \"Indus Holding (INH_X)\"], \"JEN_X\": [\"JEN_X\", \"Jenoptik (JEN_X)\"], \"JUN3_X\": [\"JUN3_X\", \"Jungheinrich (JUN3_X)\"], \"KBC_X\": [\"KBC_X\", \"Kontron (KBC_X)\"], \"KCO_X\": [\"KCO_X\", \"Kl\u00c3\u00b6ckner & Co (Kl\u00c3\u00b6Co) (KCO_X)\"], \"KD8_X\": [\"KD8_X\", \"Kabel Deutschland Holding (KD8_X)\"], \"KGX_X\": [\"KGX_X\", \"Kion Group (KGX_X)\"], \"KRN_X\": [\"KRN_X\", \"Krones (KRN_X)\"], \"KU2_X\": [\"KU2_X\", \"Kuka Aktiengesellschaft (KU2_X)\"], \"KWS_X\": [\"KWS_X\", \"Kws Saat (KWS_X)\"], \"LEG_X\": [\"LEG_X\", \"Leg Immobilien (LEG_X)\"], \"LEO_X\": [\"LEO_X\", \"Leoni (LEO_X)\"], \"LHA_X\": [\"LHA_X\", \"Deutsche Lufthansa (LHA_X)\"], \"LIN_X\": [\"LIN_X\", \"Linde (LIN_X)\"], \"LPK_X\": [\"LPK_X\", \"LPKF Laser & Electronics AG (LPK_X)\"], \"LXS_X\": [\"LXS_X\", \"Lanxess (LXS_X)\"], \"MAN_X\": [\"MAN_X\", \"Man Se St (MAN_X)\"], \"MEO_X\": [\"MEO_X\", \"Metro  St (MEO_X)\"], \"MLP_X\": [\"MLP_X\", \"Mlp (MLP_X)\"], \"MOR_X\": [\"MOR_X\", \"Morphosys (MOR_X)\"], \"MRK_X\": [\"MRK_X\", \"Merck Kgaa (MRK_X)\"], \"MTX_X\": [\"MTX_X\", \"MTU Aero Engines AG (MTX_X)\"], \"MUV2_X\": [\"MUV2_X\", \"M\u00c3\u00bcnchener R\u00c3\u00bcckversicherungs-Gesellschaft AG (Munich Re) (MUV2_X)\"], \"NDA_X\": [\"NDA_X\", \"Aurubis (NDA_X)\"], \"NDX1_X\": [\"NDX1_X\", \"Nordex Se (NDX1_X)\"], \"NEM_X\": [\"NEM_X\", \"Nemetschek (NEM_X)\"], \"NOEJ_X\": [\"NOEJ_X\", \"NORMA Group SE (NOEJ_X)\"], \"O1BC_X\": [\"O1BC_X\", \"Xing (O1BC_X)\"], \"O2C_X\": [\"O2C_X\", \"Petro Welt AG (ex cat oil) (O2C_X)\"], \"O2D_X\": [\"O2D_X\", \"Telefonica Deutschland AG (O2) (O2D_X)\"], \"OSR_X\": [\"OSR_X\", \"Osram Licht (OSR_X)\"], \"P1Z_X\": [\"P1Z_X\", \"Patrizia Immobilien (P1Z_X)\"], \"PFV_X\": [\"PFV_X\", \"Pfeiffer Vacuum Technology (PFV_X)\"], \"PMOX_X\": [\"PMOX_X\", \"Prime Office (PMOX_X)\"], \"PSAN_X\": [\"PSAN_X\", \"PSI Software AG (PSAN_X)\"], \"PSM_X\": [\"PSM_X\", \"Prosiebensat.1 Media (PSM_X)\"], \"PUM_X\": [\"PUM_X\", \"Puma Se (PUM_X)\"], \"QIA_X\": [\"QIA_X\", \"Qiagen N.v. (QIA_X)\"], \"QSC_X\": [\"QSC_X\", \"Qsc (QSC_X)\"], \"RAA_X\": [\"RAA_X\", \"Rational (RAA_X)\"], \"RHK_X\": [\"RHK_X\", \"Rh\u00c3\u2013n-klinikum (RHK_X)\"], \"RHM_X\": [\"RHM_X\", \"Rheinmetall (RHM_X)\"], \"RRTL_X\": [\"RRTL_X\", \"RTL S.A. (RRTL_X)\"], \"RWE_X\": [\"RWE_X\", \"Rwe  St (RWE_X)\"], \"S92_X\": [\"S92_X\", \"SMA Solar AG (S92_X)\"], \"SAP_X\": [\"SAP_X\", \"Sap (SAP_X)\"], \"SAX_X\": [\"SAX_X\", \"Str\u00c3\u00b6er SE & Co. KGaA (SAX_X)\"], \"SAZ_X\": [\"SAZ_X\", \"Stada Arzneimittel Ag (SAZ_X)\"], \"SBS_X\": [\"SBS_X\", \"Stratec Biomedical (SBS_X)\"], \"SDF_X\": [\"SDF_X\", \"K+s Aktiengesellschaft (SDF_X)\"], \"SFQ_X\": [\"SFQ_X\", \"SAF-Holland SA (SFQ_X)\"], \"SGL_X\": [\"SGL_X\", \"Sgl Carbon Se (SGL_X)\"], \"SIE_X\": [\"SIE_X\", \"Siemens (SIE_X)\"], \"SIX2_X\": [\"SIX2_X\", \"Sixt Se St (SIX2_X)\"], \"SKB_X\": [\"SKB_X\", \"Koenig & Bauer (SKB_X)\"], \"SKYD_X\": [\"SKYD_X\", \"Sky Deutschland (SKYD_X)\"], \"SLT_X\": [\"SLT_X\", \"Schaltbau Holding (SLT_X)\"], \"SOW_X\": [\"SOW_X\", \"Software (SOW_X)\"], \"SPR_X\": [\"SPR_X\", \"Axel Springer Se (SPR_X)\"], \"SRT3_X\": [\"SRT3_X\", \"Sartorius  Vz (SRT3_X)\"], \"SW1_X\": [\"SW1_X\", \"Shw (SW1_X)\"], \"SY1_X\": [\"SY1_X\", \"Symrise (SY1_X)\"], \"SZG_X\": [\"SZG_X\", \"Salzgitter (SZG_X)\"], \"SZU_X\": [\"SZU_X\", \"S\u00c3\u00bcdzucker (SZU_X)\"], \"TEG_X\": [\"TEG_X\", \"Tag Immobilien (TEG_X)\"], \"TIM_X\": [\"TIM_X\", \"ZEAL Network SE (TIM_X)\"], \"TKA_X\": [\"TKA_X\", \"Thyssenkrupp (TKA_X)\"], \"TLX_X\": [\"TLX_X\", \"Talanx Aktiengesellschaft (TLX_X)\"], \"TTI_X\": [\"TTI_X\", \"Tom Tailor Holding (TTI_X)\"], \"TTK_X\": [\"TTK_X\", \"Takkt (TTK_X)\"], \"TUI1_X\": [\"TUI1_X\", \"Tui (TUI1_X)\"], \"UTDI_X\": [\"UTDI_X\", \"United Internet (UTDI_X)\"], \"VIB3_X\": [\"VIB3_X\", \"Villeroy & Boch AG (VIB3_X)\"], \"VNA_X\": [\"VNA_X\", \"Vonovia SE (ex Deutsche Annington) (VNA_X)\"], \"VOS_X\": [\"VOS_X\", \"Vossloh (VOS_X)\"], \"VOW3_X\": [\"VOW3_X\", \"Volkswagen  Vz (VOW3_X)\"], \"VT9_X\": [\"VT9_X\", \"Vtg Aktiengesellschaft (VT9_X)\"], \"WAC_X\": [\"WAC_X\", \"Wacker Neuson Se (WAC_X)\"], \"WCH_X\": [\"WCH_X\", \"Wacker Chemie (WCH_X)\"], \"WDI_X\": [\"WDI_X\", \"Wirecard (WDI_X)\"], \"WIN_X\": [\"WIN_X\", \"Diebold Nixdorf AG (WIN_X)\"], \"ZIL2_X\": [\"ZIL2_X\", \"Elringklinger (ZIL2_X)\"], \"ZO1_X\": [\"ZO1_X\", \"Zooplus (ZO1_X)\"]}")
quandl.ApiConfig.api_key = 'tBctXCfFqZzRwSny_Znm'
infection_import_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

hdfsconn = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"{hdfspath}/webhdfs/v1/",
                                         request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})
infection_file_path = "/user/root/input/infections"
fse_file_path = "/user/root/input/fse"

hdfsconn.make_dir("/user/root/input", permission=777)
hdfsconn.make_dir("/user/root/input/infections", permission=777)
hdfsconn.make_dir("/user/root/input/fse", permission=777)
 
foundInfections = False
foundFSE = False
root_dir = hdfsconn.list_dir("/user/root/input")
if len(root_dir) > 0:
    for dir in root_dir.values():
        for dir2 in dir.values():
            for dir3 in dir2:
                if dir3["pathSuffix"] == "infections":
                    foundInfections = True
                if dir3["pathSuffix"] == "fse":
                    foundFSE = True

producer = kafka.KafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap:9092')

if foundInfections and foundFSE:
    while True:
        import_fse(quandl_companies, startdate, enddate, fse_file_path, hdfsconn, producer)
        import_infections(infection_import_url, hdfsconn, infection_file_path, producer)
        print("import process finished successfully! Next import will be in 1 hour")
        time.sleep(3600)
