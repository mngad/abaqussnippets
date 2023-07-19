from odbAccess import *
from abaqusConstants import *
import odbAccess
import time 
#**********************************************
# Main Variables
#**********************************************
first_step_name = 'Load_stat'
load_step_name = 'Load_stat'
#tib_instance_name = 'ASSEMBLY'
tib_instance_name = 'TIB-1'
node_set_name = 'TIB_SET'
#node_set_name = 'CONTACTNODESET'
tib_rp_name = 'TIBRP'
explicit = True
filename = 'F:/TKR_Exp_test1/Static_v3_0p01-2mm.odb'
inc_amount = 0.01
#**********************************************************************
preferred_extension = '.xlsx'  # Insert the extension for the output file
#**********************************************************************

odb = openOdb(path=filename)
my_assembly = odb.rootAssembly

name_of_file1 = filename[:-4] + '_CPRESS' + preferred_extension
name_of_file2 = filename[:-4] + '_CSLIP1' + preferred_extension
name_of_file3 = filename[:-4] + '_CSLIP2' + preferred_extension

name_of_file6 = filename[:-4] + '_nodelabels' + preferred_extension
name_of_file7 = filename[:-4] + '_tibpos' + preferred_extension
name_of_file8 = filename[:-4] + '_tibrot' + preferred_extension
name_of_file9 = filename[:-4] + '_tibRF' + preferred_extension
start_time = time.time()
old_looptime = 0
with open(name_of_file1, 'w') as SD_results_x, open(name_of_file2, 'w') as SD_results_y, \
        open(name_of_file3, 'w') as SD_results_z, open(name_of_file6, 'w') as SD_results_n, \
        open(name_of_file7, 'w') as tibpos_res, open(name_of_file8, 'w') as tibrot_res, \
        open(name_of_file9, 'w') as tib_rf_res:
    #***********************************************************************
   last_frame = odb.steps[first_step_name].frames[-1]
   # print(last_frame)
   displacement = last_frame.fieldOutputs['CPRESS']
   # print(displacement)
   field_values = displacement.values
   # print(field_values)
   center = odb.rootAssembly.instances[tib_instance_name].nodeSets[node_set_name]
   # print(center)
   center_displacement = displacement.getSubset(region=center)
   # print(center_displacement)
   center_values = center_displacement.values
   
   # nodenumbers
   SD_results_n.write('\t'.join(str(v.nodeLabel) for v in center_values) + '\n')

   SD_results_x.write('0\t' + '\t'.join(str(v.nodeLabel) for v in center_values) + '\n')
   SD_results_y.write('0\t' + '\t'.join(str(v.nodeLabel) for v in center_values) + '\n')
   SD_results_z.write('0\t' + '\t'.join(str(v.nodeLabel) for v in center_values) + '\n')

   step_num = 0
   

   if explicit:
      for stepName in odb.steps.keys():

         print(str(stepName))
         if (stepName == load_step_name):
            init = time.time()
            init_time = init - start_time
            for i, frame in enumerate(odb.steps[stepName].frames):
               print(str(i) +"/" + str(len(odb.steps[stepName].frames)-1)+"\r")
               center = odb.rootAssembly.instances[tib_instance_name].nodeSets[node_set_name]
               for field, res in [('CPRESS', SD_results_x),
                  ('CSLIP1', SD_results_y),
                  ('CSLIP2', SD_results_z)]:
                  subset = frame.fieldOutputs[field].getSubset(region=center)
                  values = subset.values
                  if i < 1:
                     res.write('0\t')
                  else:
                     res.write(str(inc_amount * i) + '\t')
                  for v in values:
                     res.write(str(v.data) + '\t')
                  res.write('\n')
               tibRP = odb.rootAssembly.nodeSets['TIBRP']
               for field, res in [('U', tibpos_res), ('UR', tibrot_res), ('RF', tib_rf_res)]:
                  if i < 1:
                        res.write('0\t')
                  else:
                     res.write(str(inc_amount * i) + '\t')
                  dat = frame.fieldOutputs[field].getSubset(region=tibRP).values[0]
                  if field == 'U':
                     res.write(str(dat.data[1]) + '\n')
                  else:
                     res.write(str(dat.data[0]) + '\t' + str(dat.data[1]) + '\t' + str(dat.data[2]) + '\n')
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

#         else:
#            lastFrame = odb.steps[stepName].frames[-1]
#            for field, file in zip(
#               [lastFrame.fieldOutputs['CPRESS   General_Contact_Domain'], lastFrame.fieldOutputs['CSLIP1   General_Contact_Domain'], lastFrame.fieldOutputs['CSLIP2   General_Contact_Domain']],
#               [SD_results_x, SD_results_y, SD_results_z]
#               ):
#               if step_num < 1:
#                    file.write('0\t')
#               else:
#                    file.write(str(inc_amount * step_num) + '\t')
#               for v in field.getSubset(region=odb.rootAssembly.instances['TIB-1'].nodeSets['TIB_SET']).values:
#                    file.write(str(v.data) + '\t')
#               file.write('\n')
#            step_num += 1

   else:
      for i, step_name in enumerate(odb.steps.keys()):
         step = odb.steps[step_name]
         last_frame = step.frames[-1]

         contact_x = last_frame.fieldOutputs['CPRESS'].getSubset(region=odb.rootAssembly.instances[tib_instance_name].nodeSets[node_set_name]).values
         slip_x = last_frame.fieldOutputs['CSLIP1'].getSubset(region=odb.rootAssembly.instances[tib_instance_name].nodeSets[node_set_name]).values
         slip_y = last_frame.fieldOutputs['CSLIP2'].getSubset(region=odb.rootAssembly.instances[tib_instance_name].nodeSets[node_set_name]).values

         SD_results_x.write('{}\t{}\n'.format(inc_amount * i, '\t'.join(map(str, contact_x))))
         SD_results_y.write('{}\t{}\n'.format(inc_amount * i, '\t'.join(map(str, slip_x))))
         SD_results_z.write('{}\t{}\n'.format(inc_amount * i, '\t'.join(map(str, slip_y))))

         tib_rp = odb.rootAssembly.nodeSets[tib_rp_name]
         tib_pos = last_frame.fieldOutputs['U'].getSubset(region=tib_rp).values[0].data[1]
         tib_rot = last_frame.fieldOutputs['UR'].getSubset(region=tib_rp).values[0].data
         tib_rf = last_frame.fieldOutputs['RF'].getSubset(region=tib_rp).values[0].data

         tibpos_res.write('{}\t{}\n'.format(inc_amount * i, tib_pos))
         tibrot_res.write('{}\t{}\n'.format(inc_amount * i, '\t'.join(map(str, tib_rot))))
         tib_rf_res.write('{}\t{}\n'.format(inc_amount * i, '\t'.join(map(str, tib_rf))))