from CRABClient.UserUtilities import config
config = config()

config.General.requestName = '2017ppBsBPB0New3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
#config.JobType.psetName = '/BuToJpsiKp_pThat-5_TuneCP5_5p02TeV_Pythia8/RunIIpp5Spring18DR-94X_mc2017_realistic_forppRef5TeV_v1-v1/AODSIM'
#config.JobType.psetName = 'runForestAOD_pp_MC_94X_onlyBfinder.py'

config.JobType.psetName = 'runForestAOD_pp_DATA_94X_onlyBfinder.py'
config.JobType.numCores = 1
#config.JobType.maxMemoryMB = 20000
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True
config.Site.ignoreGlobalBlacklist = True
#config.Data.inputDataset = '/HIMinimumBias0/HIRun2018A-04Apr2019-v1/AOD'

#config.Data.inputDataset = 'runForestAOD_pp_MC_94X_onlyBfinder.py'

#config.Data.inputDataset = '/BuToJpsiKp_pThat-5_TuneCP5_5p02TeV_Pythia8/RunIIpp5Spring18DR-94X_mc2017_realistic_forppRef5TeV_v1-v1/AODSIM'

config.Data.inputDataset = '/DoubleMuon/Run2017G-17Nov2017-v1/AOD'

#config.Data.lumiMask = "v1_JSON.txt"
config.Data.splitting = 'FileBased'
config.Data.inputDBS = "global"                                                                                                                                                   
#config.Data.splitting = "LumiBased"                                                                                                                                               
config.Data.unitsPerJob = 2

config.Data.lumiMask = 'Cert_306546-306826_5TeV_EOY2017ReReco_Collisions17_JSON_MuonPhys.txt'

#NJOBS = 500  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = -1
#config.Data.outLFNDirBase = '/store/user/zzshi/' 
config.Data.outLFNDirBase = '/store/group/phys_heavyions/zshi/2017ppDataBmesonMulti'
config.Data.publication = False
config.Data.outputDatasetTag = '2017ppBMesonData'


config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ["T2_TR_METU","T3_US_Kansas","T2_US_MIT","T2_US_Purdue","T2_US_Nebraska","T2_US_Vanderbilt","T2_CH_CERN"]

config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
#config.section_("Debug")
#config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
#:wconfig.Site.whitelist = ['T2_US_MIT']
