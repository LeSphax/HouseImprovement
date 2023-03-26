import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "nilmtk2"))
sys.path.append(os.path.dirname(__file__))

import numpy as np
import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt

rcParams['figure.figsize'] = (13, 6)


from nilmtk2 import DataSet, TimeFrame, MeterGroup, HDFDataStore
from nilmtk2.legacy.disaggregate import CombinatorialOptimisation
from nilmtk2.utils import print_dict
from nilmtk2.metrics import f1_score

# ## Import Data from HDF file

# data = DataSet('./data/AMPds2.h5')
data = DataSet('./PGE.h5')
print('Loaded', len(data.buildings), 'buildings')

# ## Loading data for Building 1

elec = data.buildings[1].elec


elec.get_timeframe()


data.buildings[1].elec

# ## Set a window

data.set_window(start='2021-01-01',end='2021-08-24')
elec_1 = data.buildings[1].elec

# ## Mains and Submeters Data

mains=elec_1.mains()
submeters=elec_1.submeters()

# ## Running HART_85

df = next(mains.load())

from nilmtk2.disaggregate.hart_85 import Hart85
h = Hart85({})
if (os.path.isfile('model.pickle')):
    h.import_model('model.pickle')
else:
    h.partial_fit([df], [], columns=[('power','active')], noise_level = 0.009, state_threshold=0.009, min_tolerance=0.1, large_transition=1)

# #### Please set columns accordingly 
# #### For REDD, since mains is 'Apparent Power'
# #### For IAWE, you may set columns to columns= [('power','active')] or to columns= [('power','active'),('power','reactive')]
# 
# ## Train the model



# ## Save Model using export_model

h.export_model('model.pickle')

# # ## Import model after saving


result=h.disaggregate_chunk([df])
print(result)
exit


# # Uncomment it for closing the Output HDFDataStore

# # ## Returned Disaggregated Dataframe

# df.tail()

# # ## Since Hart is unsupervised, Find best matched appliances to disaggregated output.

# h.best_matched_appliance(submeters,df)

# # ## So it shows column 0's appliance best matches with Fridge, 1-> dish washer, 2-> washer dryer

# elec  

# # ## Comparing for Fridge

# # First we need to take intersection of indices of dataframes of fridge and predicted (Inner Join)
# df_fridge = next(elec_1['heat pump', 1].load())
# merged_df = pd.merge(df[1], df_fridge, left_index=True, right_index=True)


# merged_df.head()


# (merged_df[1][0:5000].sum() - merged_df['power', 'active'][0:5000].sum()) / merged_df[1][0:5000].sum()


# merged_df[1][0:6000].plot(c='r')
# merged_df['power', 'active'][0:6000].plot()
# plt.legend(["Predicted", "Ground truth"])
# plt.ylabel("Power (W)")
# plt.xlabel("Time")

# # ## Comparing for  Washer Dryer

# df_dish_washer = next(elec_1['washer dryer', 1].load())
# merged_df = pd.merge(df[2], df_fridge, left_index=True, right_index=True)


# merged_df.head()


# ax1 = merged_df[2].plot(c='r')
# ax2 = merged_df['power', 'active'].plot(c='grey')
# ax1.legend(["Predicted", "Ground truth"])
# plt.ylabel("Power (W)")
# plt.xlabel("Time")


