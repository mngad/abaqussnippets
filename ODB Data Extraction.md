# ODB File Data Extraction

## Open ODB & Define Assembly

```python
odb = openOdb(path=filename)
my_assembly = odb.rootAssembly
```

## Cycling through frames for Multiple Fields Simultaneously

```python
for i, frame in enumerate(odb.steps[stepName].frames):
    center = odb.rootAssembly.instances['TIB-1'].nodeSets['TIB_SET']
    for field, res in [('CPRESS   General_Contact_Domain', SD_results_x),
        ('CSLIP1   General_Contact_Domain', SD_results_y),
        ('CSLIP2   General_Contact_Domain', SD_results_z)]:
        subset = frame.fieldOutputs[field].getSubset(region=center)
        values = subset.values

```

## Cycle through U, UR and RF about a single RF

Writes the output to separate results files: tibpos_res, tibrot_res and tib_rf_res. Can split the output and add tabs for the x, y and z components.

```python
for field, res in [('U', tibpos_res), ('UR', tibrot_res), ('RF', tib_rf_res)]:
    dat = frame.fieldOutputs[field].getSubset(region=tibRP).values[0]
    if field == 'U':
        res.write(str(dat.data[1]) + '\n')
    else:
        res.write(str(dat.data[0]) + '\t' + str(dat.data[1]) + '\t' + str(dat.data[2]) + '\n')
```


## Tangentially Related
Time the loop and estimate remaining time.

```python
import time
start_time = time.time()

init = time.time()
init_time = init - start_time

# Do the looping

end_time = time.time()
loop_time = end_time - start_time

if(old_looptime != 0): 
    loopdif = loop_time - old_looptime
    totpred = ((loopdif) * len(odb.steps[stepName].frames))+ init_time
    remainingtime = totpred - (i*loopdif) - init_time
    if remainingtime > 120:
        rem = str(remainingtime/60) + "mins"
    else:
        rem = str(remainingtime) + "s"
    if totpred > 120:
        tot = str(totpred/60) + "mins"
    else:
        tot = str(totpred) + "s"
    print("current time: " + str(loop_time) + ", remaining time: " + rem+ ", total time: " + tot +"\r")

old_looptime = loop_time
```

## [Full Example Script](ExampleCode/Scriptfor_DataExtract.py)