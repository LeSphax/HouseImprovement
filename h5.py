import tables
import h5py
filename = "./data/AMPds2.h5"
filename = "PGE2.h5"

with h5py.File(filename, "r") as f:
    # List all groups
    print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]

    # Get the data
    data = f[a_group_key]
    print(f[a_group_key])
    f.require_group('building1').keys()

    print(f.require_group('building1')['elec'])
    print("Keys: %s" % f.require_group('building1')['elec']['meter1']['_i_table']['index'].keys())
    print(f.require_group('building1')['elec']['meter1'])
    print(f.require_group('building1')['elec']['meter1']['_i_table']['index'])
    print(f.require_group('building1')['elec']['meter1']['table'])

    print(list(f.require_group('building1')['elec']['meter1']['table'])[0:100])
    # for kkey in f.require_group('building1')['elec']['meter1']['_i_table']['index'].keys():
    #     print(f.require_group('building1')['elec']['meter1']['_i_table']['index'][kkey])
    #     if (len(list(f.require_group('building1')['elec']['meter1']['_i_table']['index'][kkey])) < 1000):
    #         print(list(f.require_group('building1')['elec']['meter1']['_i_table']['index'][kkey]))
    #     else:
    #         print(len(list(f.require_group('building1')['elec']['meter1']['_i_table']['index'][kkey])))
    
 