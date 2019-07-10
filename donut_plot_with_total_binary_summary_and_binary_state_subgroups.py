#!/usr/bin/env python
# donut_plot_with_total_binary_summary_and_binary_state_subgroups.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# donut_plot_with_total_binary_summary_and_binary_state_subgroups.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.7; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a dataframe, and some information about columns in the 
# dataframe and makes two donut plots. One plot is the total
# of the specified binary data (such as present or not present, +/-, True or 
# False), and the other plot is a further breakdown of the binary state by 
# categorical classification or grouping.
#
# The dataframe can be pickled, tab-separated form, or comma-separated form. The 
# script will use the extension to decide how to read it in, and so use `.pkl`
# for saving pickled dataframes or `.tsv` or `.csv` for the tab- or comma-
# separated text versions, respectively. If using inside Jupyter or IPython, you 
# can use the main function of the script, 
# `donut_plot_with_total_binary_summary_and_binary_state_subgroups()` and when 
# calling it supply the dataframe in memory to avoid needing a file 
# intermediate.
#
#
#
#
# For impetus, see 
# `developing donut plot to plot omega intron distribution among mitos from XXXXXX cerevisiae set.md`
# 
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# 
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version

#
# To do:
# -  add `--hilolist` based on `donut_plot_with_subgroups_from_dataframe.py`
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python donut_plot_with_total_binary_summary_and_binary_state_subgroups.py data.tsv binary_col grp_col
#-----------------------------------
# Issue `donut_plot_with_total_binary_summary_and_binary_state_subgroups.py -h` for 
# details.
# 
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the dataframe (or dataframe file) and columns:
# from donut_plot_with_total_binary_summary_and_binary_state_subgroups import donut_plot_with_total_binary_summary_and_binary_state_subgroups
# donut_plot_with_total_binary_summary_and_binary_state_subgroups(df_file="data.tsv",binary_state_col="status",grouping_col="subtype");
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from donut_plot_with_total_binary_summary_and_binary_state_subgroups import donut_plot_with_total_binary_summary_and_binary_state_subgroups
donut_plot_with_total_binary_summary_and_binary_state_subgroups(df_file="data.tsv",binary_state_col="In_Stock",grouping_col="Manufacturer");
'''
#
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

plot_figure_size = (16.09,4.75) # width by height written as `(width,height)`; 
# increase the width of overall figure if the labels of the two subplots are
# overlapping. If you change this to substantial degree, you may also want to 
# adjust text size settings below and possibly turn off plot titles using 
# `include_subplot_titles=False`in favor of adding your own in post-processing.
# Originally `(14,4)` seemed best but adjusted it further after adjusting the 
# plot title offset and font sizes.
include_subplot_titles = True
total_plot_title = "OVERALL"
group_plot_title = "BY GROUP"
title_text_size = 20     # font size for titles above each subplot
main_plot_text_size = 14 # font size for text in each plot
large_img_size = (27,6.1) # size to be used with `--large_image` `flag. Width 
# by height written as `(width,height)`
light_color_for_last_in_state_set = True # Set this to False to reverse the 
# order of the subgroup colors if wrong binary state being colored as light for 
# the groups in the plot on the right. (This predates addition of `--hilolist`, 
# which is a better way to control. However, because binary there is only two 
# options and so leaving this so one doesn't have to necessarily use 
# `--hilolist` if too cumbersome.)
save_plot_name_prefix = "donut_plot"

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************






















#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


###---------------------------HELPER FUNCTIONS--------------------------------###

def generate_output_file_name(save_plot_name_prefix):
    '''
    Takes a file name prefix as an argument and returns string for the name of 
    the output file.  

    save_plot_name_prefix = "donut_plot"


    Specific example
    =================
    Calling function with
        ("donut_plot")
    returns
        "donut_plot.png"
    '''
    return save_plot_name_prefix + ".png"


def extract_dataframe(file_name):
    '''
    Takes a file name and using the extension determines how to extract the
    dataframe recorded in it. 
    Returns a pandas dataframe object.

    Works with pickled, tab-separated text, and comma-seperated text.
    (haven't added json yet).
    Specify, which with file ending in `.pkl`,`.tsv`, or `.csv`.
    Case doesn't matter for the extension.
    '''
    extension = Path(file_name).suffix
    if extension.lower() == ".pkl":
        return pd.read_pickle(file_name)
    elif extension.lower() == ".tsv":
        return pd.read_csv(file_name, sep='\t')
    elif extension.lower() == ".csv":
        return pd.read_csv(file_name)
    else:
        sys.stderr.write("\n**ERROR** Cannot determine how dataframe is stored "
            "in '{}'.\nChange the file name extension in the input file to be "
            "`.pkl`, `.tsv`, or `.csv` to indicate\nif dataframe stored "
            "pickled, stored as tab-separated text, or stored as\n"
            "comma-separated text."
            ".\n**EXITING !!**.\n".format(file_name))
        sys.exit(1)

    
def sequential_color_maps_generator():
    '''
    generator to yield a never-ending supply of sequential color palettes/ 
    color maps.
    However it will start with several of the ones like color brwwer defined 
    sequential ones. See 'sequential'
    at https://ggplot2.tidyverse.org/reference/scale_brewer.html (Turns out
    same ones already in matplotlib, see 
    https://matplotlib.org/tutorials/colors/colormaps.html so can even use 
    without having to convert from seaborn `sns.color_palette` to colormaps,
    which I didn't know if it was even possible without moving to the custom
    ones)
    Only after those are exhausted will it move on to some other ones that 
    I judged as possibly good options and diverse and then after those are 
    exhausted it will try to generate random ones. 
    '''
    color_brewer_seq_names = ["Blues", "Reds","Greens","Oranges",
                            "Purples"] #"Greys" looks bad because white is least
    list_of_other_good_sequences = ["teal", "fuchsia", "darkslateblue", "sage", 
                                    "darkviolet",  "crimson", "darkgoldenrod", 
                                    "dodgerblue", "maroon", "darkolivegreen",  
                                    "darkturquoise", "royalblue", "chocolate"]
    np.random.seed(42)
    for col_name in color_brewer_seq_names:
        yield plt.get_cmap(col_name) #`plt.get_cmap` use based on
        # https://matplotlib.org/tutorials/colors/colormaps.html
    for col_name in list_of_other_good_sequences:
        try:
            yield sns.light_palette(col_name, as_cmap=True)
        except ValueError:
            yield sns.light_palette(col_name, as_cmap=True,input="xkcd")
    while True:
        rgb = tuple((np.random.random(size=3) * 1)) # based on 
        # https://stackoverflow.com/a/48793922/8508004
        yield sns.light_palette(rgb, input="rgb", as_cmap=True)

def is_number(s):
    '''
    check if a string can be cast to a float or numeric (integer).

    Takes a string.

    Returns True or False
    fixed from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    later noted similar code is at https://code-maven.com/slides/python-programming/is-number
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def cast_to_number(s):
    '''
    Cast a string to a float or integer. 
    Tries casting to float first and if that works then it tries casting the 
    string to an integer. (I thought I saw suggestion of that order somewhere 
    when searching for what I used as `is_number()` check but cannot find source
    right now.)

    Returns a float, int, or if fails, False. (Where using, it shouldn't ever
    trigger returning `False` because checked all could be converted first.)

    based on fixed code from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    '''
    try:
        number = float(s)
        try:
            number = int(s)
            return number
        except ValueError:
            pass
        return number
    except ValueError:
        pass
    try:
        import unicodedata
        num = unicodedata.numeric(s)
        return num
    except (TypeError, ValueError):
        pass
    return False


def f7(seq):
    '''
    remove duplicates from a list whilst preserving order.
    For when just using `set` to get to unique because order importance.

    from https://stackoverflow.com/a/480227/8508004
    '''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


###--------------------------END OF HELPER FUNCTIONS--------------------------###
###--------------------------END OF HELPER FUNCTIONS--------------------------###

#*******************************************************************************
###------------------------'main' function of script--------------------------##

def donut_plot_with_total_binary_summary_and_binary_state_subgroups(
    df_file=None, df=None, binary_state_col=None, grouping_col=None,
    save_image=False, save_vg=False, include_percent_in_grp_label=True,
    include_total_in_grp_label=True, hilolist = None, swap_left_colors = False,
    advance_color_increments=0, advance_right_color_increments=0,
    include_subplot_titles=include_subplot_titles,
    total_plot_title = total_plot_title, 
    group_plot_title = group_plot_title):
    '''
    Takes the following:
    - name of a dataframe file (string) or a dataframe
    - text of name of column to use as binary data
    - text of name of column to use in grouping
    - Whether you want an image saved or not. If no image file saved, it tries
    to return a plot figure object.
    - optionally, for when `save_image=True`, whether you want to save the plot 
    image as vector graphics 
    - Optionally including the percent of total for each group in the plot 
    label.
    - Optionally including the total amount for each group in the plot label.
    - Optionally, a list to use as the high to low intensity degree for coloring
    the subgroups can be specified.
    - Optionally, swap the colors used in the left subplot.
    - optionally, how many cycles you want the sequential color palette 
    generator to advance through its first colors.
    - optionally, how many cycles you want the sequential color palette 
    generator to advance through its colors for the subplot on the right. Use 
    this when you are happy with default colors on the left subplot.
    - Optionally, whether you want to include subplot title
    - Optionally, whether you want to set total plot title to anything other 
    than  default; it is disregarded if `include_subplot_titles=False`.
    - optionally, whether you want to set group plot title to anything other 
    than default; it is disregarded if `include_subplot_titles=False`.

    Returns:
    A plot object, meant for when using in Jupyter or IPython. Not triggered 
    when called from command line.

    Generates:
    Depending on how called it can also generate a plot image. This is meant to
    be default for the command line; however, it can be included when calling
    main function in Jupyter or IPython.

    Main function of script. 
    Takes a dataframe either as a file or passed directly along some information 
    about columns in the dataframe and makes two donut plots. One plot is the 
    total of the specified binary data (such as present or not present, +/-, 
    True or False), and the other plot is a further breakdown of the binary 
    state per categorical classification or grouping.

    If `save_image` is True it saves an image of the plot (png by default). If
    `save_image` is False it returns a plot object. The latter being meant for
    when using the script in Jupyter notebook.

    Additional options are noted under `Takes the following` above.
    '''
    if df is None:
        #read in dataframe from file since none provided in memory
        assert df_file != None, ("If no dataframe is provided, a file with the "
            "contents of the dataframe as pickled, tab-separated text, or "
            "comma-separated text must be provided and the name of that file "
            "specified when calling the script.")
        # use file extension to decide how to parse dataframe file.
        df = extract_dataframe(df_file)


    # Check if state column to use is actually binary data. If it isn't, can
    # it be made to be by discarding NA or Nan or None, i.e., 'missing' data? 
    # That is unless the setting not to deal with missing data has been set.
    # Added that state column result in one state because could all be one of 
    # the two possible states. 
    if not 2 >= len(set(df[binary_state_col].tolist())) > 0:
        # copy original dataframe for easy comparison.
        orig_df = df.copy()
        # try removing any NA, Nan, or none & report doing that.
        df[binary_state_col].replace('None', np.nan, inplace=True) #If any `None`
        # happen to be strings, convert them now before removing.
        df.dropna(subset=[binary_state_col])
        if len(df) < len(orig_df):
            sys.stderr.write("WARNING: Rows with missing data in the state "
                "column removed.")
            sys.stderr.write("\n{} rows were removed.".format(
                len(orig_df) - len(df)))
            # if any removed, reflect that in assert message
            if len(df) < len(orig_df):
                assert 2 >= len(set(df[binary_state_col].tolist())) > 0, ("The "
                    "column designated as representing binary data contains "
                    "more than "
                    "two states, even if 'missing' values are removed.")
    assert 2 >= len(set(df[binary_state_col].tolist())) > 0, ("The column "
        "designated as representing binary data contains more than two states.")

    # Prepare derivatives of the dataframe that may be needed for delineating 
    # the plotting data
    tc = df[binary_state_col].value_counts()
    if hilolist:
        assert len(hilolist) == len(tc), "The list provided "
        "to specify the intensity degree must include all subgroups. Subgroups "
        "are: '{}'.format(list(tc.index))"
        tc = tc.reindex(hilolist)
    total_binary_names = tc.index.tolist()
    total_binary_size = tc.tolist()
    grouped = df.groupby(grouping_col)
    # use `value_counts()` on each group to get the count and name of each state
    list_o_subgroup_names_l = []
    list_o_subgroup_size_l = []
    for name,group in grouped:
        dfc = group[binary_state_col].value_counts()
        list_o_subgroup_names_l.append(dfc.index.tolist())
        list_o_subgroup_size_l.append(dfc.tolist())
    
    # Delineate data for the plot:  (SEE TEST SETTINGS BELOW)
    group_names= grouped.size().index.tolist()
    group_size= grouped.size().tolist() #len of each groupby grouping
    '''
    list_o_subgroup_names_l=[group[binary_state_col].tolist(
        ) for name, group in grouped]
    # flatten that list of lists
    subgroup_names=[i for sublt in list_o_subgroup_names_l for i in sublt]
    '''
    # flatten each list of lists made above to get the list needed
    subgroup_names=[i for sublt in list_o_subgroup_names_l for i in sublt]
    #assert len(subgroup_names) == 2 * len(grouped) <-- That would be true if
    # all states represented by all subgroups, but that may not be the case
    subgroup_size=[i for sublt in list_o_subgroup_size_l for i in sublt]
    assert len(subgroup_size) == len(subgroup_names)

    #FOR TESTING BASICS USE HARDCODED DATA based mostly on 
    # https://python-graph-gallery.com/163-donut-plot-with-subgroups/:
    '''
    group_names= ["groupA","groupB","groupC"] 
    group_size=[12,11,30] #len of each groupby grouping
    subgroup_names=['A.1', 'A.2', 'B.1', 'B.2', 'C.1', 'C.2', ]
    subgroup_size=[6,6,5.5,5.5,15,15]
    '''

    # Create colors generator
    colormp = sequential_color_maps_generator() 
    #a, b =[next(colormp)(0.6) for x in total_binary_names]
    [next(colormp) for g in range(advance_color_increments)]#advance prior to 
    # use, if initial skips specified

    # Create a switch system for the labels
    ip_it_grp_label = {
        (True,True):["{} ({:.1%} [{}])".format(
            x,y/len(df),y) for x, y in zip(group_names, group_size)],
        (True,False):["{} ({:.1%})".format(
            x,y/len(df)) for x, y in zip(group_names, group_size)],
        (False,True):["{} [{}]".format(
            x,y) for x, y in zip(group_names, group_size)],
        (False,False):["{}".format(
            x) for x, y in zip(group_names, group_size)]}

    #Set up for plot.
    fig=plt.figure(figsize=plot_figure_size) # based on 
    # https://stackoverflow.com/a/55051471/8508004; `fig=plt.figure(
    #figsize=(10, 7))` will result in much larger plot in the output cell but 
    # if you assign the plot returned by the function to a variable, say `x`, 
    # can use`x.figure.set_size_inches((17, 11))` to make large after the fact.
    # See bottom of the following notebook about that:
    # https://git.io/fjEji

    #1 row 2 cols
    ######first (and only) row, first col (LEFT subplot)
    ax1 = plt.subplot2grid((1,2),(0,0))
    ax1.axis('equal') #<- necessary? Commented out when trying to dial in 
    #dimensions because worried it complicated things; however, once dialed in I
    #ran it with it active and saw no difference. Inherited from original code 
    # at Python Graph Gallery.
    ### First Ring (outside) and only ring for first row, first col
    ### THIS WILL BE TOTAL DATA FOR BINARY STATE
    labels_with_total_each = ["{} ({:.1%} [{}])".format(x,
        y/len(df),y) for x, y in zip(total_binary_names, total_binary_size)]
    tcm = [next(colormp)(0.6) for x in total_binary_names]
    if swap_left_colors:
        tcm.reverse()
    mypie, _ = plt.pie(
        total_binary_size, radius=1.3, labels=labels_with_total_each , 
        textprops={'fontsize': main_plot_text_size}, colors=tcm )
    plt.setp( mypie, width=0.3, edgecolor='white')

    plt.margins(0,0)
    if include_subplot_titles:
        plt.title(total_plot_title, size = title_text_size, y=1.08) # offset
        # based on https://stackoverflow.com/a/23338363/8508004 and comments 
        # below that




    # following completion of left subplot, advance colors for right subplot if 
    # `advance_right_color`/`advance_right_color_increments` specified
    [next(colormp) for g in range(advance_right_color_increments)]


    #####first (and only) row, second col (RIGHT subplot)
    colorm_per_grp=[next(colormp) for g in group_names]
    ax1 = plt.subplot2grid((1,2), (0, 1))
    ax1.axis('equal') #<- necessary? Commented out when trying to dial in 
    #dimensions because worried it complicated things; however, once dialed in I
    #ran it with it active and saw no difference. Inherited from original code 
    # at Python Graph Gallery.
    ### First Ring (outside) for first row, second col
    ### This will be size of each group
    labels_with_grp_sz = ip_it_grp_label[(
        include_percent_in_grp_label,include_total_in_grp_label)]
    mypie, _ = plt.pie(
        group_size, radius=1.3, labels=labels_with_grp_sz, 
        textprops={'fontsize': main_plot_text_size},
        colors=[colormp(0.63) for colormp in colorm_per_grp] )
    plt.setp( mypie, width=0.3, edgecolor='white')

    ### Second Ring (Inside) for first row, SECOND col
    ### This will be the subgroup counting of the state for each group
    # Note that the code blocked out just below this comment would work if at
    # least one representative of each possible binary state existed for each
    # group. However that won't be the case always as some groups might 
    # represent one of the two states. (Plus this way didn't offer a way to
    # control color.)
    '''
    list_sub_grp_colors_l=[[colormp(
        0.6),colormp(0.2)] for colormp in colorm_per_grp]
    # flatten that list
    sub_grp_colors = [i for sublt in list_sub_grp_colors_l for i in sublt]
    # note that the next line works but much easier to understand this complex 
    # set of steps in last two lines of actual code to not do at once: 
    #sub_grp_colors = [i for sublt in [[colormp(0.6),colormp(
    #    0.2)] for colormp in colorm_per_grp] for i in sublt]
    '''
    # So the following color code deals with cases with just one state. Plus, 
    # try to apply primary or secondary color depending on order it is in in the 
    # states list.
    list_sub_grp_colors_l  = []
    states_represented = f7(df[binary_state_col].tolist())
    #int_degree = [0.6,0.2]
    if hilolist:
        states_represented = hilolist
    else:
        # Provide feedback on what is being used as high to low intensity list 
        # so user can adjust; using `if __name__ == "__main__"` to customize 
        # note depending if script called from command line.
        sys.stderr.write("Note: No list to specify high to low intensity "
            "coloring "
            "provided, and so using '{}',\nwhere leftmost identifer corresponds "
            "to most intense and rightmost is least.\n".format(
            ",".join(str(i) for i in states_represented))) # because subgroups 
        # could be integers as in example from 
        # https://python-graph-gallery.com/163-donut-plot-with-subgroups/, best 
        # to have conversion to string,
        if __name__ == "__main__":
            sys.stderr.write("Look into adding use of the `--hilolist` option "
                "to specify the order.\n\n")
        else:
            sys.stderr.write("Provide a Python list as `hilolist` when calling "
                "the function to specify the order.\n\n")
    # assign intensity degree settings for each subgroup so consistent among 
    # other groups
    int_degree = np.linspace(0.6, 0.2, num=len(states_represented))
    if not light_color_for_last_in_state_set:
        int_degree.reverse()
    # determine colors for each subgroup before `plt.pie` step
    for idx,subgroups_l in enumerate(list_o_subgroup_names_l):
        cm = colorm_per_grp[idx]
        grp_colors = [cm(int_degree[states_represented.index(
            sgrp)]) for sgrp in subgroups_l]
        list_sub_grp_colors_l.append(grp_colors)
    # flatten that list
    sub_grp_colors = [i for sublt in list_sub_grp_colors_l for i in sublt]
    mypie2, _ = plt.pie(
        subgroup_size, radius=1.3-0.3, labels=subgroup_names, 
        textprops={'fontsize': main_plot_text_size}, labeldistance=0.7, 
        colors=sub_grp_colors)
    plt.setp( mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    if include_subplot_titles:
        plt.title(group_plot_title, size = title_text_size, y=1.08) # offset
        # based on https://stackoverflow.com/a/23338363/8508004 and comments 
        # below that

    #FOR TESTING BASICS USE HARDCODED DATA based mostly on 
    # https://python-graph-gallery.com/163-donut-plot-with-subgroups/ &
    # https://stackoverflow.com/a/38438533/8508004  :
    '''
    # Create colors
    colormp = sequential_color_maps_generator() 
    a, b, c=[next(colormp) for g in group_names]

    #1 row 2 cols
    #first row, first col
    ax1 = plt.subplot2grid((1,2),(0,0))
    ax1.axis('equal')
    # First Ring (outside) for first row, first col
    mypie, _ = plt.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.6), b(0.6), c(0.6)] )
    plt.setp( mypie, width=0.3, edgecolor='white')

    # Second Ring (Inside) for first row, first col
    mypie2, _ = plt.pie(subgroup_size, radius=1.3-0.3, labels=subgroup_names, labeldistance=0.7, colors=[a(0.55), a(0.2), b(0.55), b(0.2), c(0.60), c(0.2)])
    plt.setp( mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    plt.title('Nested plot 1')


    #first row sec col
    group_size=[40,22,13]
    subgroup_size=[20,20,11,11,6.5,6.5]
    a, b, c=[next(colormp ),next(colormp ),next(colormp )]
    ax1 = plt.subplot2grid((1,2), (0, 1))
    ax1.axis('equal')
    # First Ring (outside) for first row, second col
    mypie, _ = plt.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.6), b(0.6), c(0.6)] )
    plt.setp( mypie, width=0.3, edgecolor='white')

    # Second Ring (Inside) for first row, second col
    mypie2, _ = plt.pie(subgroup_size, radius=1.3-0.3, labels=subgroup_names, labeldistance=0.7, colors=[a(0.55), a(0.2), b(0.55), b(0.2), c(0.60), c(0.2)])
    plt.setp( mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    plt.title('Nested plot 2')
    '''



    # Reporting and Saving
    #--------------------------------------------------------------------
    if save_image:
        if plot_figure_size == large_img_size:
            output_file_name = generate_output_file_name(
                save_plot_name_prefix+ "_larger")
        else:
            output_file_name = generate_output_file_name(save_plot_name_prefix)
        if save_vg:
            plt.savefig(output_file_name[:-4]+".svg", 
            orientation='landscape') # FOR VECTOR GRAPHICS; useful if merging 
            # into Adobe Illustrator. Based on 
            # https://neuroscience.telenczuk.pl/?p=331 ; I think ReportLab also 
            # outputs SVG?
            sys.stderr.write("\nPlot image saved to: {}\n".format(
                output_file_name[:-4]+".svg"))
        else:
            # save png
            plt.savefig(output_file_name)
            sys.stderr.write("\nPlot image saved to: {}\n".format(
                output_file_name))
    else:
        sys.stderr.write("Plot figure object returned.")
        return ax1

###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###










#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main():
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    kwargs['save_image'] = True
    kwargs['save_vg'] = save_vg
    kwargs['include_percent_in_grp_label'] = include_percent_in_grp_label
    kwargs['include_total_in_grp_label'] = include_total_in_grp_label
    kwargs['hilolist'] = hilolist
    kwargs['swap_left_colors'] = args.swap_left_colors
    kwargs['advance_color_increments'] = advance_color_increments
    kwargs['advance_right_color_increments'] = advance_right_color_increments
    donut_plot_with_total_binary_summary_and_binary_state_subgroups(
        df_file=args.df_file,binary_state_col=args.binary_state_col,
        grouping_col=args.grouping_col,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__":
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='donut_plot_with_total_binary_summary_and_binary_state_subgroups.py',
        description="donut_plot_with_total_binary_summary_and_binary_state_subgroups.py \
        takes a dataframe, and some information about columns in the dataframe \
        and makes two donut plots. One plot is the total of the specified \
        binary data (such as present or not present, +/-, True or False), and \
        the other plot is a further breakdown of the binary state per \
        categorical classification or grouping.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("df_file", help="Name of file containing the \
        dataframe. Whether it is in the form of a pickled dataframe, \
        tab-separated text, or comma-separated text needs to be indicated by \
        the file extension. So `.pkl`, `.tsv`, or `.csv` for the file \
        extension. \
        ", metavar="DF_FILE")

    parser.add_argument("binary_state_col", help="Text indicating column in \
        dataframe with the binary data. This data is to be plotted in inner \
        ring.\
        ", metavar="BINARY_COL")

    parser.add_argument("grouping_col", help="Text indicating column in \
        dataframe to use as the main groups in group break down plot.\
        ", metavar="GROUPS")

    parser.add_argument("-li", "--large_image",help=
        "add this flag to make the image saved larger than the default of \
        `{}`".format(
        plot_figure_size),action="store_true")

    #removed reporting exact size of larger one (see code below) because found 
    #inexplicably it results in a size different than one set size using 
    #`figure.set_size_inches()`, and rather not confuse things in demo notebook
    #by using same numbers and seeing slightly different results. (I suspect
    #it is a subtle glitch resulting in slightly different output via the two 
    #size setting approaches.)
    ''' 
    parser.add_argument("-li", "--large_image",help=
        "add this flag to make the image saved larger than the default of \
        `{}`. Adding this flag will set the saved file size to `{}`.".format(
        plot_figure_size,large_img_size),action="store_true")
    '''
    parser.add_argument("-lopg", "--leave_off_percent_in_group",help=
        "add this flag to not display the percent of the total for each group.\
        ",action="store_true")
    parser.add_argument("-lotg", "--leave_off_total_in_group",help=
        "add this flag to not display the total amount for each group.\
        ",action="store_true")
    parser.add_argument("-svg", "--save_vg",help=
        "add this flag to save as vector graphics \
        (**RECOMMENDED FOR PUBLICATION***) instead of default png. Not default \
        or saved alongside `.png` version normally because not as easy to deal \
        with as typical image file. ",
        action="store_true")
    parser.add_argument('-hll', '--hilolist', action='store', type=str, 
        help="This flag is used to specify that you want to control the order \
        of the subgroups to range from being dark to light in the degree of \
        color intensity in the plot because the default result does not \
        suffice. Follow the flag with an order listing, high intensity to low, \
        of the subgroup identifiers separated by \
        commas, without spaces or quotes. For example `-hll yes,maybe,no`. \
        When the script is run the identifiers and default order used will be \
        indicated so that you'll have the identifiers at hand when running \
        again.\
         ")# based on https://stackoverflow.com/a/24866869/8508004
    parser.add_argument("-slc", "--swap_left_colors",help=
        "add this flag to swap the colors used for the left subplot. \
        Typically, unless `hilolist` is specified, the first color is assigned \
        to the largest state/subgroup. When `hilolist` is specified, the first \
        listed state/subgroup/caetgory in the `hilolist` is matched with the \
        'first' color. However, because there are multiple ways to specify \
        what is the 'first' color or the 'default' outcome is not \
        satisfactory, you may find you want to \
        switch around the colors being used in the left plot. Addgng this \
        argument provides for that." ,
        action="store_true")
    parser.add_argument('-ac', '--advance_color', action='store', type=int, 
        default= '0', help="**FOR ADVANCED USE.** Allows for advancing the \
        color palette iterator a specified number of times. The idea is it \
        allows skipping a specified amount of the initial colors to help \
        'customize' the set of colors in the plot, if needed. Supply \
        the number to advance after the flag on the command line. For example, \
        `-ac 4`. If that doesn't allow dialing in a good set of colors, and \
        you know Python, you can edit the `list_of_other_good_sequences`.") 
    parser.add_argument('-arc', '--advance_right_color', action='store', 
        type=int, default= '0', help="**FOR ADVANCED USE.** Allows for \
        advancing the color palette iterator a specified number of times for \
        just the subplot on the right side, i.e., the subplot on the left \
        side, for the total, remains untouched. The idea is it \
        allows skipping a specified amount of the colors to help \
        'customize' the set of colors in the subplot on the right side when \
        you are happy with the colors on the left subplot. Supply \
        the number to advance after the flag on the command line. For example, \
        `-arc 4`. If that doesn't allow dialing in a good set of colors, and \
        you know Python, you can edit the `list_of_other_good_sequences`.")





    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    save_vg = args.save_vg
    include_percent_in_grp_label= not args.leave_off_percent_in_group
    include_total_in_grp_label= not args.leave_off_total_in_group
    if args.large_image:
        plot_figure_size = large_img_size
    hilolist = args.hilolist
    #process to a python list if it exists
    if hilolist:
        hilolist = args.hilolist.split(',')
        #if they hapen to be integers or floats, convert so will match type in 
        # dataframe
        if all([is_number(s) for s in hilolist]):
            hilolist = [cast_to_number(s) for s in hilolist]
            # make sure all float if any are float, because line above will 
            # cast to integer if possible
            if any(isinstance(x, float) for x in hilolist):
                hilolist = [float(x) for x in hilolist]
    advance_color_increments = args.advance_color
    advance_right_color_increments = args.advance_right_color



    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************