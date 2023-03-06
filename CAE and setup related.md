# CAE and setup related

## Import

```python
mdb.ModelFromInputFile(name='Model Name', inputFileName='INP file location.inp')

# remove original model 1
del mdb.models['Model-1']
```

## Job Setup

```python

mdb.Job(name=job_name, model='LTKN6046_host', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=20, 
    numDomains=20, numGPUs=1)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

```