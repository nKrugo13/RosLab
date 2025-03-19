# -*- coding: utf-8 -*-
"""
 Personal Projects
 Graphing functions
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
import re
#import math

#TODO: Make a function that creates a folder in this 
#Setup Environment
#BeadInputPath = os.getenv("Bead_Input_path", "C:\\Users\\krugo\\ASU Research/Data/Total_Image_Bead2")
initial_point = ()
final_point = None
rectangle = None

BeadInputPath = os.getenv("Bead_Input_path", "\ASU_Research\Total_Image_Bead_Alexandra")
#BeadInputPath = os.getenv("Bead_Input_path", "\ASU_Research\Total_Image_Bead2")
    
#IMPORTANT NOTE: This file saves based on the location of your files here so make sure that your file has the graphs file as well as the other two folders inside it
def Plotter(df, name,value,save): 
    """
    Takes in the dataframe, name of the file, the type of plot, and whether you want to save the file
    Value: 1) Intensity, 2) Comparison Intensity, 3) Plot Profile, 4) Comparison of Plot Profile
    Save: 'y' or 'n'
    Important that the name array is in the format of [Potential, Potential Value]
    """
    name_withPotential = str(name[0]+ ' ' + name[1])

    if value == 1 or value == 2:
        xlabel = 'X'
        ylabel = 'Y'
        if value == 1:
            title = str('Intesity for '+ name_withPotential)
            new_name = str('Intensity_Profile_for_'+name_withPotential)
            file_new_name = str('Intensity_Profile/Plot/'+new_name)
        elif value == 2:
            title = str('Differnce in Intensities for ' + name[0])
            new_name = str('Intensity_Comparison_Profile_for_'+name[0])
            file_new_name = str('Intensity_Profile/Comparison/'+new_name)
        column_name = [new_name, 'Intensity']
        
        #TODO: FIX THe Scaling for low end Change the scaled_size back to 2000
        # Only necessary for very zoomed in ROI cuts can be fixed by changing to a heat map instead
        fig, ax = plt.subplots()
        
        number_of_points = int(len(df['X'])) * int(len(df['Y']))
        width_inches, height_inches = fig.get_size_inches()
        dpi = fig.dpi

        Plotting_Area = (width_inches * height_inches) * int(dpi)

        scaled_size = Plotting_Area / np.log(number_of_points)
        
        new_points_df = df
        print('This is your Scaling factor: ' + str(scaled_size) + ', number of points: '+  str(number_of_points)+' and plotting area: ' + str(Plotting_Area) + ' DPI: '+ str(dpi))
        
        
        
        # Show the plot

    elif value == 3 or value == 4:    
        xlabel = 'Distance'
        ylabel = 'Grey Value'
        if value == 3:
            title = str('Grey Value for '+ name_withPotential)
            new_name = str('Plot_Profile_for_'+name_withPotential)
            file_new_name = str('Plot_Profile/Plot/'+new_name)
        elif value == 4:
            title = str('Differnce in Grey Values for ' + name[0])
            new_name = str('Plot_Profile_Comparison_for_'+name[0])
            file_new_name = str('Plot_Profile/Comparison/'+new_name)
        column_name = [new_name, 'Value']
        df[column_name[1]].plot()
        
    
        
    
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    if save == 'y':
        file_path = str(os.getcwd()+BeadInputPath+'\\Graphs\\'+file_new_name+'.png')
        plt.savefig(file_path)
        print('File Saved at '+file_path)
    else:
        plt.show()
    plt.clf()

#Type o plot is the column name of plot type
def multi_plotter(multi_array,desired_save, type_o_plot,tracker):
    """
    Multi Plotter is a function that takes in an array of dataframes and plots them all on the same graph
    ISSUES: Electrode probabilty can be quite difficult to work 
    This is a recursive function or at least attempted in order to make this more efficient
    Also a Smoother has been added but is not needed and can be commented out its only purpose is to help with the electrode finder
    Tracker is the recursive part of this function and is used to store the amplitudes of the peaks
    """
    value = 0
    if type_o_plot[1] == 'Intensity':
        new_name = Plot_Title_finder(type_o_plot[0],'Multi')
        xlabel = 'X'
        ylabel = 'Y'
    elif type_o_plot[1] == 'Value':
        new_name = type_o_plot[0]
        xlabel = 'Distance'
        ylabel = 'Grey Value'
    if tracker == 'all':
        plt.figure(figsize=(20, 10))
        print(len(multi_array))
        for i in range(len(multi_array)):
            plt.plot(multi_array[i][0][type_o_plot[1]],density=True, bins=300, label= multi_array[i][1])
            print(f'Iteration {i}, Name: {multi_array[i][1]}')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title('Plot profile comparison for all')
        plt.grid()
        plt.legend()
        plt.show()
        #plt.clf()
    elif tracker == 'First':
        tracker = []
        print(tracker)
        multi_plotter(multi_array,desired_save, type_o_plot,tracker)
    else:
        #TODO: Fix this spart of function so that we can split graphs across several plots
        #NOTE: Tracker is repurposed as a list for storing amplitudes        
        orginal_length_o_multi_array = int(len(multi_array))
        if orginal_length_o_multi_array != 0 and len(multi_array) != 0:
            plt.figure(figsize=(10, 5))
            list_index = len(multi_array)
            i = 0
            value = orginal_length_o_multi_array
            while len(multi_array) != 0:
                if i <= value:
                    #multi_array[0][0][type_o_plot[1]]
                    window_size = 5
                    type_o_plot[1] = 'Value'
                    #multi_array[0][0][type_o_plot[1]+' smooth'] = (multi_array[0][0][type_o_plot[1]]).rolling(window_size, min_periods=1).mean()
                    #(multi_array[0][0][type_o_plot[1]]).plot.hist(density=True, bins=int(7), label= multi_array[0][1])
                    #print(f'Iteration {i}, Name: {multi_array[0][1]}')
                    print(len(multi_array))
                    df_value_savgol_filter = savgol_filter ((multi_array[0][0]['Value']), window_length=11, polyorder=3)
                    peaks, _ = find_peaks((multi_array[0][0]['Value']), prominence=1)
                    max_value = (multi_array[0][0]['Value']).max()
                    min_value = (multi_array[0][0]['Value']).min()
                    new_peaks = []
                    new_min_peaks = []
                    value_cut_for = 'max'
                    (multi_array[0][0]['Value']) *= -1
                    min_peaks, _= find_peaks((multi_array[0][0]['Value']), prominence=1)
                    #print((multi_array[0][0]).loc[peaks, 'Value'])
                    (multi_array[0][0]['Value']) *= -1
                    if min_value < 0 and abs(min_value) > max_value:
                        (multi_array[0][0]['Value']) *= -1
                        peaks, _= find_peaks((multi_array[0][0]['Value']), prominence=0.6)
                        #print((multi_array[0][0]).loc[peaks, 'Value'])
                        (multi_array[0][0]['Value']) *= -1
                        min_peaks, _= find_peaks((multi_array[0][0]['Value']), prominence=0.6)
                        #print((multi_array[0][0]).loc[peaks, 'Value'])
                        print('Negative DEP')
                        value_cut_for = 'min'
                    for t in range(len(peaks)):
                        #print(multi_array[0][0]['Value'][peaks[t]])
                        if float(multi_array[0][0]['Value'][peaks[t]]) >= float(0.6 * max_value) and value_cut_for == 'max':
                            new_peaks.append(peaks[t])
                        elif float(multi_array[0][0]['Value'][peaks[t]]) <= float(0.6 * min_value) and value_cut_for == 'min':
                            new_peaks.append(peaks[t])
                    for t2 in range(len(min_peaks)):
                        if float(multi_array[0][0]['Value'][min_peaks[t2]]) <= float(0.3 * max_value) and value_cut_for == 'max':
                            new_min_peaks.append(min_peaks[t2])
                        elif float(multi_array[0][0]['Value'][min_peaks[t2]]) >= float(0.3 * min_value) and value_cut_for == 'min':
                            new_min_peaks.append(min_peaks[t2])

                    tracker.append([(multi_array[0][0]).loc[new_peaks, 'Value'], multi_array[0][1]])
                    plt.plot(multi_array[0][0]['Distance'], multi_array[0][0][type_o_plot[1]], label=multi_array[0][1])
                    #plt.plot(multi_array[0][0]['Distance'], df_value_savgol_filter, label='Smoothed'+multi_array[0][1])
                    plt.plot(multi_array[0][0]['Distance'][new_peaks], multi_array[0][0][type_o_plot[1]][new_peaks], "o", color = 'green')
                    plt.plot(multi_array[0][0]['Distance'][new_min_peaks], multi_array[0][0][type_o_plot[1]][new_min_peaks], "o", color = 'red')
                    #plt.plot(multi_array[0][0]['Distance'], df_value_savgol_filter, label='Smoothed '+type_o_plot[0])
                    
                    electrode_index_bounds = electrode_probabillity_scanner(tracker[i][0])
                    print(electrode_index_bounds)
                    v = 1
                    starting_Point = multi_array[0][0]['Distance'].iloc[0]
                    ending_Point = multi_array[0][0]['Distance'].iloc[-1]
                    '''plt.axvspan(starting_Point, (new_peaks[0]+starting_Point-1), color='gray', alpha=0.3)
                    plt.axvspan((electrode_index_bounds[0]+starting_Point+1), (electrode_index_bounds[1]+starting_Point-1), color='gray', alpha=0.3)
                    plt.axvspan((electrode_index_bounds[2]+starting_Point+1), (electrode_index_bounds[3]+starting_Point-1), color='gray', alpha=0.3)
                    plt.axvspan((new_peaks[-1]+starting_Point+1), ending_Point, color='gray', alpha=0.3)'''
                    
                    '''for index in range(int(len(electrode_index_bounds)/2)):
                        ax.axvspan(index, electrode_index_bounds[v], color='gray', alpha=0.3)
                        v = v + 2'''
                    
                    #stored_maximum_intensities
                    #print(type(df_value_savgol_filter))
                    print('Plotted '+ multi_array[0][1])
                    #print(multi_array[0][0][type_o_plot[1]+' smooth'])
                    multi_array.pop(0)
                    i = i + 1
                    # NOTE: reason for this section is if more than 6 plots are graphed it can be difficult to view
                    '''if len(multi_array) == 0:
                        multi_array = 6'''
                #Five in this number of plots on one figure
                if i >= value or len(multi_array) == 0:
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.title(new_name)
                    plt.grid()
                    plt.legend()
                    plt.show()
                    if len(multi_array) == 0:
                        print('Break the Function')
                        i = -10
                        #multi_array.append('Fail')
                        plt.clf()
                        #print(tracker)
                        break
                    else:
                        i = 0
                        multi_plotter(multi_array,desired_save, type_o_plot,tracker)               

        plt.clf()
    if len(multi_array) == 0:
        print(tracker)
        print('Time####################################################################')
        return tracker 
    else:
        print('What Happend: '+ len(multi_array))
        return 'Fail'
        
#INPUT: data file location name
#OUTPUT: The number of potential used
#NOTE: Can be made much better but it works well with the naming convention I used
# Naming convention is the month_day_year_hour_minute_second_PotentialOnorOff_PotentialValue 
def Plot_Title_finder(name_1,value):
    file_name_parts = name_1.split('_')
    trigger = False

    number_name = []
    
    #potential = str(file_name_parts[5])
    potential = str([item for item in file_name_parts if item.startswith('V(') or item.startswith('NoV(')])
    
    pot_number = potential.split('(')
    #TODO: Clean this up
    if str(pot_number[0]) == '[\'V':
        Potential_or_NO = 'Potential'
    elif pot_number[0] == '[\'NoV':
        Potential_or_NO = 'No Potential'
    else:
        print('SOMETHING IS WRONG IN FINDING IF IT IS POTENTIAL OR NOT IN THE TITLE FINDER PLOT')
    standalone_potential_number_integer_value = int(file_name_frequency_finder(pot_number[1]))            
    if value == 3 or value == 4 or value == 1 or value == 2:
        pot_num2 = pot_number[1].split(')')
        potential_number_only = str(pot_num2[0])
        #print('This is the potential number only for value 3: ' + potential_number_only)
        both_number_and_potential_OnOff_list = [potential_number_only, Potential_or_NO]
        print(both_number_and_potential_OnOff_list[0]+both_number_and_potential_OnOff_list[1])

        return both_number_and_potential_OnOff_list
    #TODO: Make sure that the multi works with changes made above specifically the
    elif value == 'Multi':
        temp = []
        for i in range(len(file_name_parts)):
            if file_name_parts[i] == 'for':
                return temp
            else:
                temp.append(file_name_parts[i])
    print('Something has borken this is your last potential: '+ potential + 'This is your usage value: '+ pot_number[0]+pot_number[1])
    
#Looks into the Data/Total image folder and finds all data then pairs each data set with its potential on and off 
#Outputs: an array of arrays with location names 
#TODO: Make it output a sorted array by value of potential
#NOTE: This was orginally made to automate all analysis pairings using the naming convention
def organized_data_output_multiArray(x):
    global numerical_frequency_integer_index
    folder_path = os.getcwd() + x
    print("Current Working Directory:", folder_path)
    file_names = os.listdir(folder_path)
    #file_names = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    combo_array_of_names = []
    extra_file_names = file_names
    numerical_frequency_integer_index = []
    
    for i in range(int(len(file_names)/2)):
        file_name = file_names[i]
        
        #TODO: WIP TO MAKE THIS ABSTRACT AND FIND Potential Number Sort and Organize by this
        #freq_value = re.search(r'\((\d+Hz)\)', file_name).group(1)
        file_name_parts = (((file_name.split('_'))[5]).split('('))[1]
        potential = str(file_name_parts[5])
        seperate_no = ((file_name_parts[5]).split(')'))[0]
        freq_value_string = file_name.split('(')[1].split('Hz')[0]
        seperate_no = freq_value_string
        #freq_value_string = (seperate_no[0])
        #freq_value_string = str(freq_value)

        numerical_frequency_integer_index.append(int(file_name_frequency_finder(freq_value_string)))
        '''
        numerical_frequency_array.append(freq_values[0])
        numerical_frequency_array.append(freq_values[2])'''
        temp = []
        #TODO: Investigate this for loop and why it is pertinent
        for j in range(len(file_names)):

            file_name2 = file_names[j]
            
            # Safely split to extract the number in parentheses
            try:
                new_seperated = file_name2.split('(')[1].split('Hz')[0]
            except IndexError:
                new_seperated = None  # If the split fails, set to None (or handle appropriately)

            # Check if the file has "NoV" or "V"
            if 'NoV' in file_name2:
                status = False
            elif 'V' in file_name2:
                status = True
            else:
                status = None  # Handle case if neither is found (you could skip or set as False/None)

            # Compare if the number matches and the status is True
            if new_seperated == seperate_no and status is True:
                temp = [r"\{}".format(file_names[j]), r"\{}".format(file_names[i])]
                combo_array_of_names.append(temp)
    '''print(freq_values)        
    print(numerical_frequency_array)  '''

    # This is the most important array in the script which organizes our data pairing sets
    return combo_array_of_names        

#TODO: Figure out what this is for and how to implement in
#NOTE: This is not necessary for this script and can be removed. Although it could be useful for future  
def sorter(file_names):
    numerical_frequency_array = []
    for i in range(int(len(file_names)/2)):
        file_name = file_names[i]
        file_name_parts = file_name[i][0].split('_')
        potential = str(file_name_parts[5])
        seperate_no = potential.split('(')
        value = (seperate_no[1])
        value = file_name_frequency_finder(value)
        numerical_frequency_array.append(value[0])
        numerical_frequency_array.append(value[2])
    sorted_numerical_frequency_array = sort_numbers_with_indices(numerical_frequency_array)
    print('This is your sorted numberical frequency array from sorter: ' + sorted_numerical_frequency_array)
    
def sort_numbers_with_indices(nums):
    # Enumerate the list to keep track of original indices
    indexed_nums = list(enumerate(nums))
    
    # Sort the list based on the values
    sorted_nums = sorted(indexed_nums, key=lambda x: x[1])
    
    # Extract the sorted indices
    sorted_indices = [index for index, _ in sorted_nums]
    
    # Extract the sorted values
    sorted_values = [value for _, value in sorted_nums]

    return sorted_values, sorted_indices

#File Name Parser to Numerical value for experiement
def file_name_frequency_finder(value): 
    Frequency_value = str((value.split('H'))[0])
    temp = []
    number_Frequency_Value = 1 
    for character in Frequency_value:
        if character.isnumeric() == True:
            temp.append(character)
        elif character == 'M' or character == 'k' or character == 'm' or character == 'K':
            if character == 'M' or character == 'm':
                number_Frequency_Value = 1000000
            elif character == 'K' or character == 'k':
                number_Frequency_Value = 1000
            else:
                print('Something is broken in file_name_frequency_finder having too many indices that match m or k')
        else:
            break
    #TODO: failing here after selecting potential, temp not set to value [CCK]   
    int_potential_number_standalone = int(number_Frequency_Value * int(''.join(temp)))
    number_Frequency_Value = [number_Frequency_Value * int(''.join(temp)), 'V'] + [int(number_Frequency_Value * int(''.join(temp))),'No V']
    return int_potential_number_standalone
    #print(number_Frequency_Value)
    return number_Frequency_Value
    
def Combiner(df1,df2,Value):
    """
    Makes a new dataframe that is the difference between two dataframes
    """
    
    df1.rename(columns={ Value : Value+'1'}, inplace=True)
    df2.rename(columns={ Value : Value+'2'}, inplace=True)
    
    combined_final  = pd.merge(df1, df2)
    combined_final[Value] = combined_final[Value+'1'] - combined_final[Value+'2']
    
    del combined_final[Value+'1']
    del combined_final[Value+'2']
    
    return combined_final

#Input: Dataframe over all space and the cordinate of the column you wish to sum over
#Output: Dataframe which is now distance and the Grey Value
#TODO: Look into this for which axis it sums
def dimensional_Reducer(df,cordinate):
    final_df = []
    for coordinate_value in df[cordinate].unique():
        Distance = df[df[cordinate] == coordinate_value]
        Value = Distance['Value'].sum()/(len(df[cordinate].unique()))
        result_df = pd.DataFrame({'Distance': [coordinate_value], 'Value': [Value]})
        final_df.append(result_df)
        
    final_product = pd.concat(final_df, ignore_index=True)

    return final_product

#Pulled from MatPlotLib Documentation
def ROI_Click_Tracker(event):
    """
    ROI Functions are very finicky and can be difficult to work with. 
    Highly recommend Not touching these. They work perfectly and I have not run into issues since creation
    """
    global initial_point, final_point, rectangle
    if event.button == 1:
        if event.name == 'button_press_event':
            if initial_point:
#            if initial_point is not None:
                plt.close()
            else:
                initial_point = (event.xdata, event.ydata)
            rectangle = None
            print(initial_point)
            
        elif event.name == 'motion_notify_event' and initial_point is not None:
            current_pos = (event.xdata, event.ydata)
            if rectangle:
                rectangle.remove()
            rectangle = plt.gca().add_patch(plt.Rectangle((initial_point[0], initial_point[1]),
                                                             current_pos[0] - initial_point[0],
                                                             current_pos[1] - initial_point[1],
                                                             edgecolor='black', fill=False))
            plt.show()
            plt.draw()
        elif event.name == 'button_release_event':
            final_point = (event.xdata, event.ydata)
            print(final_point)
            #plt.close()

#TODO: Potential Selector for starting file
def ROI_Plotter():
    #NOTE: manually setting ROI bounds for x and y are commented out but can be set manually
    global initial_point, final_point, rectangle
    initial_point = ()
    combinedDatasetNameArray = organized_data_output_multiArray(BeadInputPath)
    df = pd.read_csv(str(os.getcwd()+BeadInputPath+combinedDatasetNameArray[0][0]))
    Potential_file_name_list = combinedDatasetNameArray[0]
    df = pd.read_csv(str(os.getcwd()+BeadInputPath+Potential_file_name_list[0]))
    df.rename(columns ={'Value':'Intensity'}, inplace=True)
    df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('ROI Selector')
    scatter = plt.scatter(df['X'], df['Y'], c=df['Intensity'])
    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', ROI_Click_Tracker)
    fig.canvas.mpl_connect('motion_notify_event', ROI_Click_Tracker)
    fig.canvas.mpl_connect('button_release_event', ROI_Click_Tracker)
    
    plt.show()
    print(initial_point, final_point)
    x_bounds = [int(initial_point[0]), int(final_point[0])]
    x_bounds = sorted(x_bounds)
    y_bounds = [int(initial_point[1]), int(final_point[1])]
    print(x_bounds, y_bounds)
    y_bounds = sorted(y_bounds)
    #x_bounds = [19,110]
    #y_bounds = [0,131]
    df_list = ROI_all_dataCutter(x_bounds, y_bounds,combinedDatasetNameArray)
    print(df_list)
    return df_list

#Input: asks for a number from input commmand
#OutPut: list of two the file names of the two files with that frequency
#Uses Frequency_Finder and global numerical_value_potential list and Organized_data_output_multiArray
#Error Correcting: if number is not found in files will run again asking same question
def Potential_number_to_file_name():
    #NOTE: Not necessary for this script but can be useful for future
    global numerical_frequency_integer_index
    all_file_names_array = organized_data_output_multiArray(BeadInputPath)


    print('These are all the potentials avaible: ',numerical_frequency_integer_index)

    number = input('What Potential would you like to look at, may use k or m:')
    number = file_name_frequency_finder(str(str(number)+'H'))
    for i in range(len(numerical_frequency_integer_index)):  
        if int(numerical_frequency_integer_index[i]) == number:
            index_equivalent = int(i)
            break
        else:
            index_equivalent = 'Could not find the Potential requested please try again.'
    if type(index_equivalent) != int:
        Potential_number_to_file_name()
    else:           
        return all_file_names_array[index_equivalent]


def ROI_all_dataCutter(x_bounds, y_bounds,Potential_file_name_list):
    data_file_name = Potential_file_name_list
    df_cut_list =[]
    #TODO: Take this extra loop out once fixed and all t's
    for t in range(len(data_file_name)):
        for i in range(len(data_file_name[t])):
            df = pd.read_csv(str(os.getcwd()+BeadInputPath+data_file_name[t][i]))
            df['X'] = pd.to_numeric(df['X'], errors='coerce')
            df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
            xbounded_df = df.loc[(df['X'] > int(x_bounds[0])) & (df['X'] < int(x_bounds[1]))]
            full_cut_df = xbounded_df.loc[(xbounded_df['Y'] > int(y_bounds[0])) & (xbounded_df['Y'] < int(y_bounds[1]))]
            final_df_with_name = [full_cut_df, data_file_name[i]]
            df_cut_list.append(final_df_with_name)

    return df_cut_list

#TASK: Collect Dataset and customize for automatice generation of analysized data sets
def main():
    """
    
    """
    print("Graphing - Start")
    print("Testing for Bead File " + BeadInputPath)

    #Collect the Data that is avaible 
    combinedDatasetNameArray = organized_data_output_multiArray(BeadInputPath)
    #print(combinedDatasetNameArray)
    multi_plotter_array = []

    #NOTE: These commented vlaue and save ask for inputs which allow for any of these four kinds of graphs
    #Input for what is desired
    value = int(input('What would you like; single Intensities(1), Compared Intesities(2), Plot Profile(3), Comparison Plot Profile(4)'))
    #save = input('Would you like them saved? (y), (n)?')
    #value =3
    save = 'n'
    #ROI_asker = 'n'
    ROI_asker = input('Would you like to make a cut at a ROI for this plot? (y), (n)?')   
    if ROI_asker == 'y':
        list_of_cut_df = ROI_Plotter()   
        combinedDatasetNameArray =[list_of_cut_df]
    else:
        print('No List of Cuts since no ROI Requested')
    if value == 1 or value== 2:
        for i in range(len(combinedDatasetNameArray)):
            j=0
            while j < len(combinedDatasetNameArray[i]):
                if ROI_asker == 'n':
                    file_path_name = str(os.getcwd()+BeadInputPath+combinedDatasetNameArray[i][j])
                    df = pd.read_csv(file_path_name)
                elif ROI_asker == 'y':
                    df = list_of_cut_df[j][0]
                    file_path_name = list_of_cut_df[j][1]
                df.rename(columns ={'Value':'Intensity'}, inplace=True)
                df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
                #List first being Potenial value the second value being whether it has potential or not
                title_name = Plot_Title_finder(file_path_name,value)
                print(df['Intensity'])

                print('This is the title name for df 1 '+title_name[0]+' '+title_name[1])

                if value == 2:
                    j = j + 1 
                    if ROI_asker == 'n':
                        file_path_name = str(os.getcwd()+BeadInputPath+combinedDatasetNameArray[i][j])
                        df2 = pd.read_csv(file_path_name)
                    elif ROI_asker == 'y':
                        df2 = list_of_cut_df[j][0]
                    df2.rename(columns ={'Value':'Intensity'}, inplace=True)
                    df2['Intensity'] = pd.to_numeric(df2['Intensity'], errors='coerce')
                    combined_difference_df = Combiner(df,df2,'Intensity') 
                    #TODO: Make it so the lowest relative values are blocked out

                    Plotter(combined_difference_df, title_name, value, save)
                else:
                    #print(df)
                    Plotter(df, title_name, value, save)
                j = j + 1 
            if ROI_asker == 'y':
                if int(len(list_of_cut_df)) == i/2:
                    break
    elif value == 3 or value == 4:
        
        #temp = (combinedDatasetNameArray[-1])
        #print(temp)
        for i in range(len(combinedDatasetNameArray)):
            j=0
            #TODO: Find a way to have it get everything for the file path
            while j < len(combinedDatasetNameArray[i]):
                if ROI_asker == 'n':
                    file_path_name = str(os.getcwd()+BeadInputPath+combinedDatasetNameArray[i][j])
                    df = pd.read_csv(file_path_name)
                elif ROI_asker == 'y':
                    df = list_of_cut_df[j][0]
                    file_path_name = list_of_cut_df[j][1]
                    
                    
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                reduced_df = dimensional_Reducer(df, 'X')

                title_name = Plot_Title_finder(file_path_name,value)
                
                if value == 4:
                    j = j + 1
                    if ROI_asker == 'n':
                        file_path_name = str(os.getcwd()+BeadInputPath+combinedDatasetNameArray[i][j])
                        df2 = pd.read_csv(file_path_name)
                    elif ROI_asker == 'y':
                        df2 = list_of_cut_df[j][0]
                    df2['Value'] = pd.to_numeric(df2['Value'], errors='coerce')
                    reduced_df2 = dimensional_Reducer(df2, 'X')

                    reduced_df = Combiner(reduced_df,reduced_df2,'Value')
                    #print('Main Function Printing the appended multi_plotter_array list for ' + str(i)+str(j)+'\n')
                    
                    multi_plotter_array.append([reduced_df,title_name[0]])
                    
                #print(multi_plotter_array)
                if len(combinedDatasetNameArray[i]) == 5:
                    print('Graphing- Trigger for Multiplot: \n')
                    
                    
                    print('Desired Multitracker activated')
                    #TODO: Put input in for seperation of plots
                    tracker = 'all'
                    column_name = ['Multi_Plot_for_Comparison_of_Plot_Profile', 'Value']
                    amplitude_list = multi_plotter(multi_plotter_array,save,column_name, tracker)
                    #print(amplitude_list)
                    print('Graphing - MultiPlot - Finish')
                    return amplitude_list
                else:
                    print('Would have printed df not Multi')
                    Plotter(reduced_df,title_name,value,save)
                j=j+1 
      
    if str(input('Would you like to run this again? (y) or (n) ')) == 'y':                 
        main()
    else:
        print("Graphing - Finish")
#Function.py main loop
main()

#Pulled from MatPlotLib Documentation
#NOTE: Fixed this so that it is not only highest but broken into parts
def calculate_metric(series):
    max_value = series.max()
    min_value = series.min()
    lengths = int((len(series))/2)
    if abs(min_value) > max_value:
        values = series.nsmallest(lengths)
    else:
        values = series.nlargest(lengths)

    print(max_value, min_value)
    print(values)
    average_amp = values.mean()
    print(average_amp)
    return average_amp

#NOTE: This can be tricky with low resolution and high electrode amounts
def electrode_probabillity_scanner(df):
    previous_index = df.index[0]
    last_index = df.index[-1]
    electrode_index = []
    for current_index in df.index[1:]:
        if current_index - previous_index > 10:
            electrode_index.append(previous_index)
            electrode_index.append(current_index)
        previous_index = current_index
    return electrode_index

"""
This next part of the code is responsible for the analysis of the data and acquiring the Real part of the CM for out system 
This is done by taking the average of the intensity values of the data and then plotting the average intensity values against the frequency values
This is done by first finding the frequency values of the data and then sorting the data by the frequency values
After this the data is scanned for the electrode values and then the average intensity values are calculated for the data
The average intensity values are then plotted against the frequency values
I am not happy with the current state of the code but it works and is a good starting point for future work
This also only works when main is outputting from the multi_plotter_array function so you must have main value being 3 or 4 to get an output
"""
Amplitude_RAW_values = main()
numerical_frequency_array = []
stored_sorted_values = []
stored_sorted_values2 = []
for t in range(len(Amplitude_RAW_values)):
    print(Amplitude_RAW_values[t][1])
    value = file_name_frequency_finder((Amplitude_RAW_values[t][1]))
    numerical_frequency_array.append(value)
sorted_Frequency_values_Used_FOR_X_AXIS , sorted_index_of_HZ = sort_numbers_with_indices(numerical_frequency_array)

for item in sorted_index_of_HZ:
    value = Amplitude_RAW_values[int(item)][0]
    print("DataFrame: ", value)
    bounds = electrode_probabillity_scanner(value)
    print(bounds)
    temp_storage_of_intensity_average_channel_values = []
    number_one_multiply = 1
    for boundary in range(len(bounds)):
        selected_rows = 0
        if boundary == 0:
            selected_rows = value[value.index <= bounds[boundary]]
        elif bounds[boundary] == bounds[-1]:
            selected_rows = value[value.index >= bounds[-1]]
        elif bounds[boundary+1] - bounds[boundary] > 10:
            print('Too Far Away')
        else:
            selected_rows = value[(value.index >= bounds[boundary]) & (value.index <= bounds[boundary + number_one_multiply])]
        if len(selected_rows) > 1:
            print(selected_rows, bounds[boundary])
            temp_storage_of_intensity_average_channel_values.append(calculate_metric(selected_rows))
            number_one_multiply = 1
        else:
            number_one_multiply = number_one_multiply + 1
    average_value = sum(temp_storage_of_intensity_average_channel_values) / len(temp_storage_of_intensity_average_channel_values)
    result = calculate_metric(value)
    stored_sorted_values.append(result)
    stored_sorted_values2.append(average_value)
    print("Result:", result, "\n Selected Resultant: ", average_value)



print('########################################################################################## \n ##################################################33')
#print(type(stored_sorted_values), stored_sorted_values)
#print(type(sorted_Frequency_values_Used_FOR_X_AXIS), sorted_Frequency_values_Used_FOR_X_AXIS)
#result_list = [x * math.log(x) for x in sorted_Frequency_values_Used_FOR_X_AXIS]
#print(result_list)
plt.plot(sorted_Frequency_values_Used_FOR_X_AXIS, stored_sorted_values, marker='o', linestyle='-')
plt.plot(sorted_Frequency_values_Used_FOR_X_AXIS, stored_sorted_values2, marker='x', linestyle='-')
#plt.plot(stored_sorted_values, marker='o', linestyle='-')
plt.xscale('log')
plt.xlabel('Frequency Hz')
plt.ylabel('Amplitudes')
plt.grid()
plt.title('Amplitude of difference between plot profiles vs Frequency values')
plt.show()
        

