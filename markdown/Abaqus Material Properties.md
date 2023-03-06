# Abaqus Material Properties

## Cycling through properties

```
for mat in mdb.models['ModelName'].materials.keys():
    myMat = mdb.models['ModelName'].materials[mat]
    if mat.endswith('SUFFIX'):
        rho = int(myMat.density.table[0][0])
        alpha = 0.8
        if rho<(10):rho=10
        E =rho*alpha
        nu = 0.3
        del myMat.elastic
        myMat.Elastic(table=((E, nu), ))

```