#!/usr/bin/env python
# donut_plot_with_subgroups_from_dataframe.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# donut_plot_with_subgroups_from_dataframe.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.7; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a dataframe, and some information about columns in the 
# dataframe and makes a donut plot similar to the one at 
# https://python-graph-gallery.com/163-donut-plot-with-subgroups/. The plot is 
# a breakdown of the main groups to subgroups with the main groups in an outer
# ring of the dount plot and the subgroups on the inner ring.
#
# The dataframe can be pickled, tab-separated form, or comma-separated form. The 
# script will use the extension to decide how to read it in, and so use `.pkl`
# for saving pickled dataframes or `.tsv` or `.csv` for the tab- or comma-
# separated text versions, respectively. If using inside Jupyter or IPython, you 
# can use the main function of the script, 
# `donut_plot_with_subgroups_from_dataframe()` and when 
# calling it supply the dataframe in memory to avoid needing a file 
# intermediate.
#
#
#
#
#
#
# Based on `donut_plot_with_total_summary_and_subgroups_from_dataframe.py`
# but made simpler by removing the plot of the total states and just having
# the plot reminiscent of the one at 
# https://python-graph-gallery.com/163-donut-plot-with-subgroups/ made from a 
# dataframe / tabular text.
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
# -  
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python donut_plot_with_subgroups_from_dataframe.py data.tsv groups_col subgroups_col
#-----------------------------------
# Issue `donut_plot_with_subgroups_from_dataframe.py -h` for 
# details.
# 
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the file of annotations:
# from donut_plot_with_subgroups_from_dataframe import donut_plot_with_subgroups_from_dataframe
# donut_plot_with_subgroups_from_dataframe(df_file="data.tsv",groups_col="status",subgroups_col="subtype");
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from donut_plot_with_subgroups_from_dataframe import donut_plot_with_subgroups_from_dataframe
donut_plot_with_subgroups_from_dataframe(df_file="data.tsv",groups_col="Manufacturer",subgroups_col="In_Stock");
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

plot_figure_size = (7,8) # width by height written as `(width,height)`; 
# If you change this to substantial degree, you may also want to 
# adjust text size settings below and possibly turn off plot titles using 
# `include_title=False`in favor of adding your own in post-processing.
outer_ring_radius = 1.3 # radius of the outer ring of the donut plot
inner_ring_radius = outer_ring_radius-0.3 # radius of the inner ring of donut
outer_ring_width=0.3
inner_ring_width=0.4
include_title = True
plot_title = "BREAKDOWN"
title_text_size = 20     # font size for title above plot
plot_text_size = 14 # font size for text in the plot
large_img_size = (14,15) # size to be used with `--large_image` `flag. Width 
# by height written as `(width,height)`
light_color_for_last_in_subgroup = True # Set this to False to reverse the 
# order of the subgroup coloring.
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

def donut_plot_with_subgroups_from_dataframe(
    df_file=None, df=None, groups_col=None, subgroups_col=None,
    save_image=False, save_vg=False, include_percent_in_grp_label=True,
    include_total_in_grp_label=True, hilolist = None, 
    sort_on_subgroup_name=False, advance_color_increments=0, 
    include_title=include_title):
    '''
    Takes the following:
    - name of a dataframe file (string) or a dataframe
    - text of name of column to use as main group data in the outer ring
    - text of name of column to use in subgroupings for the inner ring
    - Whether you want an image saved or not. If no image file saved, it tries
    to return a plot figure object.
    - optionally, for when `save_image=True`, whether you want to save the plot 
    image as vector graphics 
    - Optionally including the percent of total for each group in the plot 
    label.
    - Optionally including the total amount for each group in the plot label.
    - optionally, a list to use as the high to low intensity degree for coloring
    the subgroups can be specified.
    - optionally, to use subgroup name in sorting subgroups. This needs to be
    set to `True` to get arrangment of subgroups lile in the example
    https://python-graph-gallery.com/163-donut-plot-with-subgroups/
    - optionally, how many cycles you want the sequential color palette 
    generator to advance through its first colors.
    - optionally, whether you want to include plot title

    Returns:
    A plot, meant for when using in Jupyter or IPython. Not triggered when 
    called from command line.

    Generates:
    Depending on how called it can also generate a plot image. This is meant to
    be default for the command line; however, it can be included when calling
    main function in Jupyter or IPython.

    Main function of script. 
    Takes a dataframe either as a file or passed directly along some information 
    about columns in the dataframe and makes a donut plot.  The plot is a 
    breakdown of the main groups to subgroups with the main groups in an outer
    ring of the dount plot and the subgroups on the inner ring. The style sought 
    is seen at https://python-graph-gallery.com/163-donut-plot-with-subgroups/ .

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



    # Prepare derivatives of the dataframe that may be needed for delineating 
    # the plotting data
    tc = df[subgroups_col].value_counts()
    total_state_names = tc.index.tolist()
    total_state_size = tc.tolist()
    grouped = df.groupby(groups_col)
    # use `value_counts()` on each group to get the count and name of each state
    list_o_subgroup_names_l = []
    list_o_subgroup_size_l = []
    subgroups_per_group_l = []
    for name,group in grouped:
        dfc = group[subgroups_col].value_counts()
        if sort_on_subgroup_name:
            dfc = group[subgroups_col].value_counts().sort_index()
        list_o_subgroup_names_l.append(dfc.index.tolist())
        list_o_subgroup_size_l.append(dfc.tolist())
        subgroups_per_group_l.append(f7(group[subgroups_col].tolist()))
    
    # Delineate data for the plot:  
    group_names= grouped.size().index.tolist()
    group_size= grouped.size().tolist() #len of each groupby grouping
    '''
    list_o_subgroup_names_l=[group[subgroups_col].tolist(
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

    # Create colors generator and colors
    colormp = sequential_color_maps_generator()
    [next(colormp) for g in range(advance_color_increments)]#advance prior to 
    # use, if initial skips specified
    colorm_per_grp=[next(colormp) for g in group_names]

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
    fig, ax = plt.subplots(figsize=plot_figure_size)
    ax.axis('equal')


    ### First Ring (outside)
    ### This will be the main groups
    labels_with_grp_sz = ip_it_grp_label[(
        include_percent_in_grp_label,include_total_in_grp_label)]
    mypie, _ = plt.pie(
        group_size, radius=outer_ring_radius, labels=labels_with_grp_sz, 
        textprops={'fontsize': plot_text_size},
        colors=[colormp(0.63) for colormp in colorm_per_grp] )
    plt.setp( mypie, width=outer_ring_width, edgecolor='white')
     
    ### Second Ring (Inside)
    ### This will be the subgroup counting for each group
    list_sub_grp_colors_l  = []
    subgroups_represented = f7(df[subgroups_col].tolist())
    #int_degree = [0.6,0.2]
    if hilolist:
        assert len(hilolist) == len(subgroups_represented), "The list provided "
        "to specify the intensity degree must include all subgroups. Subgroups "
        "are: '{}'.format(subgroups_represented)"
        subgroups_represented = hilolist
    else:
        # Provide feedback on what is being used as high to low intensity list 
        # so user can adjust; using `if __name__ == "__main__"` to customize 
        # note depending if script called from command line.
        sys.stderr.write("Note:No list to specify high to low intensity coloring "
            "provided and so using '{}',\nwhere leftmost identifer corresponds "
            "to most intense and rightmost is least.\n".format(
            ",".join(str(i) for i in subgroups_represented))) # because subgroups 
        # could be integers as in example from 
        # https://python-graph-gallery.com/163-donut-plot-with-subgroups/, best 
        # to have conversion to string,
        if __name__ == "__main__":
            sys.stderr.write("Look into adding use of the `--hilolist` opition "
                "to specify the order.\n\n")
        else:
            sys.stderr.write("Provide a Python list as `hilolist` when calling "
                "the function to specify the order.\n\n")
    # assign intensity degree settings for each subgroup so consistent among 
    # other groups
    int_degree = np.linspace(0.6, 0.2, num=len(subgroups_represented))
    if not light_color_for_last_in_subgroup:
        int_degree.reverse()
    # determine colors for each subgroup before `plt.pie` step
    for idx,subgroups_l in enumerate(subgroups_per_group_l):
        cm = colorm_per_grp[idx]
        grp_colors = [cm(int_degree[subgroups_represented.index(
            sgrp)]) for sgrp in subgroups_l]
        list_sub_grp_colors_l.append(grp_colors)
    # flatten that list
    sub_grp_colors = [i for sublt in list_sub_grp_colors_l for i in sublt]
    mypie2, _ = plt.pie(
        subgroup_size, radius=inner_ring_radius, labels=subgroup_names, 
        textprops={'fontsize': plot_text_size}, labeldistance=0.7, 
        colors=sub_grp_colors)
    plt.setp( mypie2, width=inner_ring_width, edgecolor='white')
    plt.margins(0,0)
    if include_title:
        plt.title(plot_title, size = title_text_size)


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
        return ax

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
    kwargs['sort_on_subgroup_name'] = sort_on_subgroup_name
    kwargs['advance_color_increments'] = advance_color_increments
    donut_plot_with_subgroups_from_dataframe(
        df_file=args.df_file,groups_col=args.groups_col,
        subgroups_col=args.subgroups_col,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__":
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='donut_plot_with_subgroups_from_dataframe.py',
        description="donut_plot_with_subgroups_from_dataframe.py \
        takes a dataframe, and some information about columns in the dataframe \
        and makes a donut plot. FILLL IN HERE. AND GENERALIZE COLORING SO CONISTENT ACROSS GROUPS!!! <---BACK FILL IN OTHER TWO SCRIPTS OR AT LEAST NOT THE BINARY. CONTEMPLATE IF WILL WORK FOR BINARY TOO.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("df_file", help="Name of file containing the \
        dataframe. Whether it is in the form of a pickled dataframe, \
        tab-separated text, or comma-separated text needs to be indicated by \
        the file extension. So `.pkl`, `.tsv`, or `.csv` for the file \
        extension. \
        ", metavar="DF_FILE")

    parser.add_argument("groups_col", help="Text indicating column in \
        dataframe to use as main group data in the outer ring of the plot.\
        ", metavar="GROUPS")

    parser.add_argument("subgroups_col", help="Text indicating column in \
        dataframe to use as subgroupings for the inner ring.\
        ", metavar="SUBGROUPS")

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
    parser.add_argument("-ssn", "--sort_on_subgroup_name",help=
        "add this flag to sort the subgroups based on the subgroup name like \
        in example at \
        https://python-graph-gallery.com/163-donut-plot-with-subgroups/. ",
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
    parser.add_argument('-ac', '--advance_color', action='store', type=int, 
        default= '0', help="**FOR ADVANCED USE.** Allows for advancing the \
        color palette iterator a specified number of times. The idea is it \
        allows skipping a specified amount of the initial colors to help \
        'customize' the set of colors in the plot, if needed. Supply \
        the number to advance after the flag on the command line. For example, \
        `-ac 4`. If that doesn't allow dialing in a good set of colors, and \
        you know Python, you can edit the `list_of_other_good_sequences`") 




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
    #process to a python list id it exists
    if hilolist:
        hilolist = args.hilolist.split(',')
        #if they hapen to be integers or floats, convert so will match type in 
        # dataframe
        if all([is_number(s) for s in string_list]):
            hilolist = [cast_to_number(s) for s in string_list]
            # make sure all float if any are float, because line above will 
            # cast to integer if possible
            if any(isinstance(x, float) for x in hilolist):
                hilolist = [float(x) for x in hilolist]
    sort_on_subgroup_name = args.sort_on_subgroup_name
    advance_color_increments = args.advance_color




    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************