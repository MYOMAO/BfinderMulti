### HiForest Configuration
# Collisions: pp
# Type: Data
# Input: AOD

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet()

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest 94X",)
import subprocess, os
version = subprocess.check_output(['git',
    '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      # 'file:/afs/cern.ch/work/r/rbi/public/forest/HighEGJet_Run2017G_17Nov2017-v2_AOD_large.root'
       'file:B08D12ED-302F-E811-BE78-C4346BC0F3E0.root'
      )
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(8))

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_ReReco_EOY17_v6', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
             tag = cms.string("JPcalib_Data94X_2017pp_v2"),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")

         )
      ])

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestAOD.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

#############################
# Jets
#############################
process.load('HeavyIonsAnalysis.JetAnalysis.fullJetSequence_pp_data_cff')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_DATA_pp5020_2017
process = overrideJEC_DATA_pp5020_2017(process)

#####################################################################################

############################
# Event Analysis
############################
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
process.pfcandAnalyzer.skipCharged = False
process.pfcandAnalyzer.pfPtMin = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_ = cms.untracked.bool(False)
process.pfcandAnalyzer.genLabel = cms.InputTag("genParticles")
process.load("HeavyIonsAnalysis.JetAnalysis.hcalNoise_cff")

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')

####################################################################################

#####################
# Photons
#####################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = False
process.ggHiNtuplizerGED.doGenParticles = False

####################################################################################

#####################
# Electron ID
#####################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format to be processed
# DataFormat.AOD or DataFormat.MiniAOD
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce. Check here https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_7_4
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff']

# add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#####################################################################################

#########################
# Main analysis list
#########################

process.ana_step = cms.Path(
    process.hltanalysis *
    process.hltobject *
    # process.l1object +
    process.hiEvtAnalyzer *
    process.jetSequence +
    # Should be added in the path for VID module
    # process.egmGsfElectronIDSequence +
    process.ggHiNtuplizer +
    process.ggHiNtuplizerGED +
    process.pfcandAnalyzer +
    process.HiForest +
    process.trackSequencesPP
)

#####################################################################################

#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pHBHENoiseFilterResultProducer = cms.Path(process.HBHENoiseFilterResultProducer)
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)

process.pPAprimaryVertexFilter = cms.Path(process.PAprimaryVertexFilter)
process.pBeamScrapingFilter=cms.Path(process.NoScraping)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization

process.ana_step = cms.Path( 
    process.hltanalysis * 
    process.hiEvtAnalyzer  
    # process.hltobject + 
#   process.HiForest 
    ) 

#################### D/B finder #################
AddCaloMuon = False
runOnMC = False ## !!
HIFormat = False
UseGenPlusSim = False
VtxLabel = "offlinePrimaryVerticesRecovery"
TrkLabel = "generalTracks"
useL1Stage2 = True
HLTProName = "HLT"
from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X
finderMaker_75X(process, AddCaloMuon, runOnMC, HIFormat, UseGenPlusSim, VtxLabel, TrkLabel, useL1Stage2, HLTProName)

process.Bfinder.MVAMapLabel = cms.InputTag(TrkLabel,"MVAValues")
process.Bfinder.makeBntuple = cms.bool(True)
process.Bfinder.tkPtCut = cms.double(0.2) # before fit
process.Bfinder.jpsiPtCut = cms.double(0.0) # before fit
process.Bfinder.bPtCut = cms.vdouble(2.0, 5.0, 5.0, 2.0, 2.0, 2.0, 5.0) # before fit
process.Bfinder.Bchannel = cms.vint32(1, 0, 1, 1, 1, 0, 0)
process.Bfinder.VtxChiProbCut = cms.vdouble(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.10)
process.Bfinder.svpvDistanceCut = cms.vdouble(2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0)
process.Bfinder.doTkPreCut = cms.bool(True)
process.Bfinder.doMuPreCut = cms.bool(True)
process.Bfinder.MuonTriggerMatchingPath = cms.vstring(
    "HLT_HIL1DoubleMu0_v1")
process.Bfinder.MuonTriggerMatchingFilter = cms.vstring(
    "hltL1fL1sDoubleMu0L1Filtered0")
process.p = cms.Path(process.BfinderSequence)



###############################
import FWCore.ParameterSet.VarParsing as VarParsing
ivars = VarParsing.VarParsing('analysis')

ivars.maxEvents = -1
ivars.outputFile='HiForestAOD.root'
#ivars.inputFiles='file:/afs/cern.ch/work/w/wangj/public/HIZeroBias2/Run2017G-17Nov2017-v1/141428A3-8F24-E811-B2A0-1CC1DE056008.root'
ivars.inputFiles='file:B08D12ED-302F-E811-BE78-C4346BC0F3E0.root'
ivars.parseArguments() # get and parse the command line arguments

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(ivars.inputFiles)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(ivars.maxEvents)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(ivars.outputFile))

