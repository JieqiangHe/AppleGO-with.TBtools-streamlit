import os
from pickle import TRUE
from posixpath import split
from select import select
import sys
from turtle import color
import streamlit as st
import altair as alt
import pandas as pd

#install java
import jdk
HOME = os.path.expanduser('~')
if os.path.exists(HOME + "/.jdk/jdk-11.0.15+10/Contents/Home/bin/java") == False:
    jdk.install('11')
    print(jdk.OS)
    javatb = HOME + "/.jdk/jdk-11.0.15+10/Contents/Home/bin/java"
    print (javatb)
else:
    javatb = HOME + "/.jdk/jdk-11.0.15+10/Contents/Home/bin/java"
    print("java is already installed")

header = st.container()

with header:
    st.write("""
    # 🍎 APPLE GO (TBtools.) 
    ###### *Description: Using TBtools cmd to do Gene Ontology analysis with Apple id or TAIR ID.*
    """)
    species = st.multiselect("Select One Specie:", ["Arabidopsis", "Apple"],default=["Arabidopsis"])
    if species == []:
        st.error("Please select one specie. You didn't select any specie.")
    elif species == ["Arabidopsis"]:
        path = 'data/TAIR_out.emapper.annotations.GO.txt'
        st.info("You selected Arabidopsis. We will use TAIR as default.")
    elif species == ["Apple"]:
        path = 'data/GDDH13v1.1_out.emapper.annotations.GO.txt'
        st.info("You selected Apple. We will use Apple as default.")
    else:
        path = 'data/TAIR_out.emapper.annotations.GO.txt'
        st.warning("You selected two specie. We will use Arabidopsis as default.")
    ID = st.text_area("Put Your ID Matrix", help="Enter your apple ID here, one ID per line.", height=200, placeholder="Enter your apple ID here, one ID per line.")
    ID_list = ID.split('\n')
    IDfile = open("tempID.txt", "w")
    for i in ID_list:
        IDfile.write(i + '\n')
    IDfile.close()
    gobasic = 'data/go-basic.obo'
    cmd = javatb + ' -cp ' + ' TBtools_JRE1.6.jar ' + ' biocjava.bioIO.GeneOntology.EnrichMent.GOTermEnrichment ' + ' --oboFile ' + gobasic + ' --gene2GoFile ' + path + ' --selectionSetFiles ' + 'tempID.txt'
    if st.button("Run"):
        st.warning("Please wait for a while. This analysis may take a while.")
        os.system(cmd)
        if cmd == 0:
            st.success("Successfully run TBtools GO enrichment!")
        else:
            st.error("Failed to run TBtools GO enrichment! Check your ID")
    st.subheader("Result")
    gocategory = st.multiselect("Select GO BP/CC/MF:", ["BP","CC","MF"], default=["BP"])
    gosortfile = "wait"
    if gocategory == []:
        st.error("Please select one category. You didn't select any go category.")
    elif gocategory == ["BP"]:
        st.info("You selected BP. We will use BP as default.")
        gosortfile = str("tempID.txt.BP_EnrichResult.xls.sorted.padjust.xls")
    elif gocategory == ['CC']:
        st.info("You selected CC. We will use CC as default.")
        gosortfile = str("tempID.txt.CC_EnrichResult.xls.sorted.padjust.xls")
    elif gocategory == ['MF']:
        st.info("You selected MF. We will use MF as default.")   
        gosortfile = str("tempID.txt.MF_EnrichResult.xls.sorted.padjust.xls")
    else:
        st.warning("You selected > two category. We will use BP as default.")
    resultfile = open(gosortfile, "r")
    topnum = st.slider("Select Top Number of GO Terms:", min_value=1, max_value=100, value=10)
    resultlist = []
    while True:
        line = resultfile.readline()
        if not line:
            break
        if line[0] == '':
            print ("Reach the end of file")
        line = line.strip()
        linelist = line.split('\t')
        print (linelist)
        per = [linelist[0],linelist[1],linelist[2],linelist[3],linelist[4],linelist[5],linelist[6],linelist[7],linelist[8],linelist[9],linelist[10]]
        resultlist.append(per)
    resultfile.close()
    topnum_goterms = resultlist[:topnum]
    selectfile = open("selected_result.txt", "w")
    for i in topnum_goterms:
        selectfile.write(i[0] + '\t' + i[1] + '\t' + i[2] + '\t' + i[3] + '\t' + i[4] + '\t' + i[5] + '\t' + i[6] + '\t' + i[7] + '\t' + i[8] + '\t' + i[9] + '\t' + i[10] + '\n')
    selectfile.close()
    print(topnum_goterms)
    selectfilepandas = pd.read_table("selected_result.txt", sep='\t', header=0)
    st.dataframe(selectfilepandas)
    savename = st.text_input("Save as:", key="savename")
    if savename == "":
        st.error("Please enter a name for your file.")
    st.download_button("Download Result (.txt) 📂",data = open(gosortfile, "rb"),file_name=savename,mime="text/plain")
    dotelement = alt.Chart(selectfilepandas).mark_circle().encode(
        x='HitsGenesCountsInSelectedSet', y='GO_Name',color='corrected p-value(BH method)',tooltip=['corrected p-value(BH method)', 'HitsGenesCountsInSelectedSet', 'GO_Name']).interactive()
    st.altair_chart(dotelement,use_container_width=True)
    barelement = alt.Chart(selectfilepandas).mark_bar().encode(
        x=alt.X('HitsGenesCountsInSelectedSet'),
        y=alt.Y('GO_Name'),
        color=alt.Color('corrected p-value(BH method)',scale=alt.Scale(scheme='redblue'))).interactive()
    st.altair_chart(barelement,use_container_width=True)











        



    
    

        
    
    
    
    
    