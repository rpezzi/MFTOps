# WARNING: suffix hx-dy is automatic added to the end of the command
configMap = {
# Physics with beam and Cosmics 202.425 kHz (severe mask)
"COSMICS": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
"PHYSICS": "./daq_init_gap12.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 1:
#"PHYSICS_GAP8_202": "./daq_init_gap8.py --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 2:
#"PHYSICS_GAP4_134": "./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 3:
#"PHYSICS_GAP8_134": "./daq_init_gap8.py --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 4:
#"PHYSICS_GAP103_134": "./daq_init_gap103.py --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 5:
#"PHYSICS_GAP20_202": "./daq_init_gap20.py --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 5:
#"PHYSICS_GAP4_101": "./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 6:
#"PHYSICS_GAP12_101": "./daq_init_gap12.py --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 7:
#"PHYSICS_GAP12_67": "./daq_init_gap12.py --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 8:
#"PHYSICS_GAP8_67": "./daq_init_gap8.py --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 9:
#"PHYSICS_GAP8_101": "./daq_init_gap8.py --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 10:
#"PHYSICS_DCS": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 11:
"PHYSICS_GAP8_202": "./daq_init_gap8.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 12:
"PHYSICS_GAP4_134": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 13:
"PHYSICS_GAP8_134": "./daq_init_gap8.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 14:
"PHYSICS_GAP103_134": "./daq_init_gap103.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 134.950 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 15:
"PHYSICS_GAP20_202": "./daq_init_gap20.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 15:
"PHYSICS_GAP4_101": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 16:
"PHYSICS_GAP12_101": "./daq_init_gap12.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 17:
"PHYSICS_GAP12_67": "./daq_init_gap12.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 18:
"PHYSICS_GAP8_67": "./daq_init_gap8.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --mask 2 --name cru-",
# Test 19:
"PHYSICS_GAP8_101": "./daq_init_gap8.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-",
# Technical in Beam Tuning (RU ON, chips OFF) (Cosmics 202.425 kHz) TODO: ENSURE -tech can be in any position in the command line
#"TECHNICAL": "./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 -tech --name cru-",
# Technical in Beam Tuning (RU ON, chips OFF) (Cosmics 202.425 kHz) TODO: ENSURE -tech can be in any position in the command line
"TECHNICAL": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 202.425 --auto_rof --scan 2 --mask 2 -tech --name cru-",
# Noise scan 67.475 kHz
#"NOISE": "./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --name cru-",
# Noise scan 67.475 kHz
"NOISE": "./daq_init.py --dcs --gbtxload 3 --log --trig_source 4 --continuous -f 67.475 --auto_rof --scan 2 --name cru-",
# pp 202.425 kHz monte carlo emulated pattern
"PPMC": "./daq_init.py --gbtxload 3 --dcs --log --trig_source 4 --continuous -f 202.425 --auto_rof --mc_hit --mc_id 1 --name cru-",
# PbPb 44.983 kHz monte carlo emulated pattern
"PBPBMC": "./daq_init.py --gbtxload 3 --dcs --log --trig_source 4 --continuous -f 44.983 --auto_rof --mc_hit --mc_id 0 --name cru-"
}
