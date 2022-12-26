from serial import *
from time import sleep
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wgt
import os

def SaveStop(val):
    plt.savefig("saved")
    
def Stop(val):
    os._exit(1)

def AcquireTrigger(val): # Function to run the whole program and return data for the asked
    global acquire    
    acquire = 1

def FindHeader(s):
    for i in range(1000):
        try_head = s.read(1)
        if try_head[0] == 47:
            print("Header found, ready to proceed.")
            sleep(1)
            return True
    print("Header not found. Exiting.")
    return False

def GetCounts(s, exp_rate = 40000):
    data = s.read(10)
    counts = np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    for i in range(exp_rate-1):
        data = s.read(10)
        counts = counts + np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    return counts

def ContinuousCheck(): # Function to monitor counts for past 3 min
    
    s = Serial("COM5", 4000000)
    s.set_buffer_size(1000000)
    
    acquisition_time = 120
    ack_reset = acquisition_time # This value needs to be changed once more 
    global acquire
    acquire = 0    
    
    # plt.style.use('dark_background')
    # plt.style.use('seaborn-dark')
    
    plt.rcParams.update({
    "lines.color": "0.5",
    "patch.edgecolor": "0.5",
    "text.color": "0.95",
    "axes.facecolor": "0.5",
    "axes.edgecolor": "0.5",
    "axes.labelcolor": "0.5",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "0.1",
    "figure.edgecolor": "0.1",
    "savefig.facecolor": "0.1",
    "savefig.edgecolor": "0.1"})
    
    fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize = (10,6), sharex = True)
    
    b1ax = plt.axes([0.02, 0.93, 0.12, 0.045])
    save_stop_button = wgt.Button(b1ax, "Capture Screen", color="grey", hovercolor="#05b5fa")
    save_stop_button.on_clicked(SaveStop)
    
    b2ax = plt.axes([0.15, 0.93, 0.06, 0.045])
    stop_button = wgt.Button(b2ax, "Stop", color="grey", hovercolor="#05b5fa")
    stop_button.on_clicked(Stop)
    
    b3ax = plt.axes([0.22, 0.93, 0.14, 0.045])
    acquire_button = wgt.Button(b3ax, "Acquire data: "+str(ack_reset)+"s", color="grey", hovercolor="#05b5fa")
    acquire_button.on_clicked(AcquireTrigger)
    
    time_axis = np.array([1])
    tic = 1
    
    temp_data = []
    acquisition = 0
    
    found = False
    
    while (found == False):    
        pos_head = s.read(1)
        if pos_head[0] == 47:
            print('Head found')
            found = True
            counts = [GetCounts(s, 40000)]
            start_time = time.time()
            for i in range(180):
                
                # print(s.in_waiting)
                      
                tic += 1
            
                time_axis= np.append(time_axis, tic)
            
                counts = np.append(counts, [GetCounts(s, 40000)], axis = 0)
            
                A = counts[:, 0]
                B = counts[:, 1]
                BP = counts[:, 2]
                AP = counts[:, 3]
                AB = counts[:, 4]
                ABP = counts[:, 5]
                APB = counts[:, 6]
                APBP = counts[:, 7]
                ABBP = counts[:, 8]
                
                
                if acquire == 1:
                    
                    print(".", end = " ")
                    
                    if ack_reset < 1:
                        
                        acquire = 0
                        b4ax = plt.axes([0.37, 0.93, 0.16, 0.045])
                        display = wgt.Button(b4ax, "  "+str(ack_reset)+"s | Acq "+str(acquisition)+" complete", color="0.2", hovercolor="0.2")
                        print("Acquisition no.", acquisition, "completed.")
                        np.savetxt("data"+str(acquisition)+".txt", temp_data)
                        acquisition += 1
                        ack_reset = acquisition_time # Restored to the original value, 120 in this case
                        temp_data = []
                    
                    else:
                        
                        b4ax = plt.axes([0.37, 0.93, 0.04, 0.045])
                        display = wgt.Button(b4ax, str(ack_reset)+"s", color="0.2", hovercolor="0.2")
                        
                        temp_data.append([A[-1], B[-1], BP[-1], AP[-1], AB[-1], ABP[-1], APB[-1], APBP[-1], ABBP[-1]])
                        ack_reset -= 1
                    
                ax1.cla()
                ax2.cla()
                ax3.cla()
                ax4.cla()
                
                ax1.plot(time_axis, A, color = "#45fc03", label = "A")
                ax1.plot(time_axis, AP, color = "#05b5fa", label = "A'")
                ax1.text(time_axis[-1], A[-1], A[-1])
                ax1.text(time_axis[-1], AP[-1], AP[-1])
            
                ax2.plot(time_axis, B, color = "#45fc03", label = "B")
                ax2.plot(time_axis, BP, color = "#05b5fa", label = "B'")
                ax2.text(time_axis[-1], B[-1], B[-1])
                ax2.text(time_axis[-1], BP[-1], BP[-1])
            
                ax3.plot(time_axis, AB, color = "#701c8c", label = "AB")
                ax3.plot(time_axis, ABP, color = "#FFD700", label = "AB'")
                ax3.text(time_axis[-1], AB[-1], AB[-1])
                ax3.text(time_axis[-1], ABP[-1], ABP[-1])
            
                ax4.plot(time_axis, APB, color = "#701c8c", label = "A'B")
                ax4.plot(time_axis, APBP, color = "#FFD700", label = "A'B'")
                ax4.plot(time_axis, ABBP, color = "#FD0E35", label = "ABB'")        
                ax4.text(time_axis[-1], APB[-1], APB[-1])
                ax4.text(time_axis[-1], APBP[-1], APBP[-1])
                
                ax1.legend(loc = 'upper left')
                ax1.set_title("Counts against time")
                ax1.set_ylabel("Counts")
            
                ax2.legend(loc = 'upper left')
                ax2.set_title("Counts against time")
            
                ax3.legend(loc = 'upper left')
                ax3.set_xlabel("Time(s)")
                ax3.set_ylabel("Counts")
            
                ax4.legend(loc = 'upper left')
                ax4.set_xlabel("Time(s)")
                
                plt.pause(0.001)
        
            while True:
                
                tic += 1
                
                time_axis= np.delete(time_axis, 0)
                time_axis= np.append(time_axis, tic)
                
                counts = np.delete(counts, 0, axis = 0)
                counts = np.append(counts, [GetCounts(s, 40000)], axis = 0)
            
                A = counts[:, 0]
                B = counts[:, 1]
                BP = counts[:, 2]
                AP = counts[:, 3]
                AB = counts[:, 4]
                ABP = counts[:, 5]
                APB = counts[:, 6]
                APBP = counts[:, 7]
                ABBP = counts[:, 8]
                
                ax1.cla()
                ax2.cla()
                ax3.cla()
                ax4.cla()
                
                if acquire == 1:
                    
                    print(".", end = " ")
                    
                    if ack_reset < 1:
                        acquire = 0
                        print("Acquisition no.", acquisition, "completed.")
                        np.savetxt("data"+str(acquisition)+".txt", temp_data)
                        acquisition += 1
                        ack_reset = acquisition_time # Restored to the original value, 120 in this case
                        temp_data = []
                        
                    temp_data.append([A[-1], B[-1], BP[-1], AP[-1], AB[-1], ABP[-1], APB[-1], APBP[-1], ABBP[-1]])
                    ack_reset -= 1
                
                ax1.plot(time_axis, A, color = "#45fc03", label = "A")
                ax1.plot(time_axis, AP, color = "#05b5fa", label = "A'")
                ax1.text(time_axis[-1], A[-1], A[-1])
                ax1.text(time_axis[-1], AP[-1], AP[-1])
            
                ax2.plot(time_axis, B, color = "#45fc03", label = "B")
                ax2.plot(time_axis, BP, color = "#05b5fa", label = "B'")
                ax2.text(time_axis[-1], B[-1], B[-1])
                ax2.text(time_axis[-1], BP[-1], BP[-1])
            
                ax3.plot(time_axis, AB, color = "#701c8c", label = "AB")
                ax3.plot(time_axis, ABP, color = "#FFD700", label = "AB'")
                ax3.text(time_axis[-1], AB[-1], AB[-1])
                ax3.text(time_axis[-1], ABP[-1], ABP[-1])
            
                ax4.plot(time_axis, APB, color = "#701c8c", label = "A'B")
                ax4.plot(time_axis, APBP, color = "#FFD700", label = "A'B'")
                ax4.plot(time_axis, ABBP, color = "#FD0E35", label = "ABB'")        
                ax4.text(time_axis[-1], APB[-1], APB[-1])
                ax4.text(time_axis[-1], APBP[-1], APBP[-1])   
                
                ax1.legend(loc = 'upper left')
                ax1.set_title("Counts against time")
                ax1.set_ylabel("Counts")
            
                ax2.legend(loc = 'upper left')
                ax2.set_title("Counts against time")
            
                ax3.legend(loc = 'upper left')
                ax3.set_xlabel("Time(s)")
                ax3.set_ylabel("Counts")
            
                ax4.legend(loc = 'upper left')
                ax4.set_xlabel("Time(s)")
                
                plt.pause(0.001)
            
            plt.show()
    
    # s.close()
    
ContinuousCheck()