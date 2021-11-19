import sys, os, os.path
from scipy.io import wavfile
import pandas as pd
import csv

input_filename = "Heartbeat-SoundBible.com-1259675634.wav"
if input_filename[-3:] != 'wav':
    print('WARNING!! Input File format should be *.wav')
    sys.exit()

samrate, data = wavfile.read(str(input_filename))
print('Load is Done! \n')

wavData = pd.DataFrame(data)

if len(wavData.columns) == 2:
    print('Stereo .wav file\n')
    wavData.columns = ['R', 'L']
    stereo_R = pd.DataFrame(wavData['R'])
    stereo_L = pd.DataFrame(wavData['L'])
    print('Saving...\n')
    stereo_R.to_csv(str(input_filename[:-4] + "_Output_stereo_R.csv"), mode='w')
    stereo_L.to_csv(str(input_filename[:-4] + "_Output_stereo_L.csv"), mode='w')
    # wavData.to_csv("Output_stereo_RL.csv", mode='w')
    print('Save is done ' + str(input_filename[:-4]) + '_Output_stereo_R.csv , '
                          + str(input_filename[:-4]) + '_Output_stereo_L.csv')

elif len(wavData.columns) == 1:
    print('Mono .wav file\n')
    wavData.columns = ['M']

    wavData.to_csv(str(input_filename[:-4] + "_Output_mono.csv"), mode='w')

    print('Save is done ' + str(input_filename[:-4]) + '_Output_mono.csv')

else:
    print('Multi channel .wav file\n')
    print('number of channel : ' + len(wavData.columns) + '\n')
    wavData.to_csv(str(input_filename[:-4] + "Output_multi_channel.csv"), mode='w')

    print('Save is done ' + str(input_filename[:-4]) + 'Output_multi_channel.csv')

'''Only keep the data of the column of L'''
import pandas as pd
f=pd.read_csv("Heartbeat-SoundBible.com-1259675634_Output_stereo_L.csv")
keep_col = ['L']
new_f = f[keep_col]
new_f.to_csv("FinalCsvFileForheartbeat.csv", index=False)
print('Finished delete the first column')

# reading the CSV file
text = open("FinalCsvFileForheartbeat.csv", "r")

# join() method combines all contents of
# csvfile.csv and formed as a string
text = ''.join([i for i in text])

# search and replace the contents
text = text.replace("L", "0")
#text = text.replace("EmployeeNumber", "EmpNumber")
#text = text.replace("EmployeeDepartment", "EmpDepartment")
#text = text.replace("lined", "linked")

# output.csv is the output file opened in write mode
x = open("output.csv", "w")

# all the replaced text is written in the output.csv file
x.writelines(text)
x.close()
print('done')