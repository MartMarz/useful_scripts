import sys
import ROOT
import stat
import os
import Utilities.General.cmssw_das_client as das_client
file_prefix="root://xrootd-cms.infn.it//"

veto_list = ["/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
            "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM",
            "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM",
            "/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM"
            ]

def get_files(dataset_name):
    print dataset_name
    data = das_client.get_data("dataset="+dataset_name+" instance=prod/global").get('data',None)
    datasets =[ data[i].get('dataset',None)[0].get('name',None) for i in range(len(data)) ]
    print datasets
    files = []
    for dataset in datasets:
        if dataset in veto_list:
            continue
        print dataset
        data=das_client.get_data("file dataset="+dataset+" instance=prod/global")
        for d in data.get('data',None):
            #print d
            for f in d.get('file',None):
                #print f
                #if not 'nevents' in f:
                    #continue
                files.append([file_prefix+f.get('name',None),f.get('nevents',None)])
    return files

def split_files_into_jobs(files,events_per_job):
    events=0
    file_splitting = []
    files_in_job = []
    for i,file in enumerate(files):
        #print "file ",i
        files_in_job.append(file[0])
        if file[1]==None:
            file_ = ROOT.TFile.Open(file)
            tree = None
            try:
                tree = file_.Get("Events")
            except ReferenceError:
                file_.Close()
                continue
            events+=tree.GetEntries()
            file_.Close()
        else:
            events+=file[1]
        if events>=events_per_job or i==(len(files)-1):
            file_splitting.append(files_in_job)
            events=0
            files_in_job = []
    return file_splitting

def print_shell_script(boson,postfix,files):
    script=""
    script+="#!/bin/bash\n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh\n"
    script+="cd /nfs/dust/cms/user/mwassmer/MonoTop/CMSSW_10_2_13/src\n"
    script+="eval `scram runtime -sh`\n"
    if not os.path.isdir("root_files"):
        os.mkdir("root_files")
    script+="cd /nfs/dust/cms/user/mwassmer/MonoTop/useful_scripts/Vboson_Pt_Reweighting/root_files\n"
    script+="python /nfs/dust/cms/user/mwassmer/MonoTop/useful_scripts/Vboson_Pt_Reweighting/V_boson_pt_reweighting.py "+boson+" "+postfix
    for file in files:
        script+=" "+file
    script+="\n"
    script+="exitcode=$?\n"
    script+="#"+boson+'_boson_pt_'+postfix+'.sh\n'
    script+="if [ $exitcode -eq 0 ]\n"
    script+="then\n"
    script+="  exit 0\n"
    script+="else\n"
    script+="  exit 1\n"
    script+="fi\n"
    
    if not os.path.isdir("scripts"):
        os.mkdir("scripts")
    filename = 'scripts/'+boson+'_boson_pt_'+postfix+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

boson = str(sys.argv[1])
if not (boson=="Zvv" or boson=="Zll" or boson=="W"):
    print "first argument has to be Z or W"
    exit()
files = get_files(str(sys.argv[2]).replace('"',''))
print("number of files: ",len(files))
file_splitting = split_files_into_jobs(files,100000)
#print file_splitting
for i,files in enumerate(file_splitting):
    print_shell_script(boson,str(i),files)