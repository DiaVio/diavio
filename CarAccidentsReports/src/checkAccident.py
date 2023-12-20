import pickle

file_path = '/home/ubuntu/Desktop/2T_HDD/CarAccidentsReports/src/sim-record/accident-2023-11-17-08-55-00-gen185'
f_f = open(file_path, 'rb')
chromosome = pickle.load(f_f)
f_f.close()
chromosome.func()