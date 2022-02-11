[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/donut_plots_with_subgroups/master?filepath=index.ipynb)

# donut_plots_with_subgroups
Several generalized scripts for making donut plots that include subgroups

Click on `launch binder` badge above to spin up a sesion where you can make plots.

*These scripts/approaches take dataframes or tabular text (tables as text) as input.* 

If you have data as a table from elsewhere you can convert it/export into tabular text as tab-separated or comma-separated form and that can be used as input by any of the approaches here.

-----

## Demonstration notebooks

There are  **five** demo notebooks:  
The **first** notebook that opens in the active session demonstrates a script that makes it easy to make a plot like the following from a dataframe or data table.  
Typical input for first two notebooks (only a portion is represented; red annotation added for illustrating terminology):

![typical_input_repr](imgs/repr_df.png)  

Typical results (**two separate images shown**):

![typical1](imgs/donut_plot_with_subgroups_from_dataframe1.png)  

----


![typical2](imgs/donut_plot_with_subgroups_from_dataframe2.png)

The **second** notebook shows the underlying code that runs that script and makes a plot like shown in [the example from The Python Graph Gallery](https://python-graph-gallery.com/163-donut-plot-with-subgroups/).  
Typical result:

![typical_basics](imgs/basics_output.png)


The **third** notebook shows how to make a plot that includes a summary of the subgroups on the left with a plot with the subgroups on the right.  
Typical input (red annotation added for illustrating terminology):

![data_for_subgroups](imgs/subgrp_to_donut_guide.png)

Typical result:

![typical_nb3](imgs/nb3_example.png)

The **fourth** notebook shows how to make a plot much like the third notebook produces; however, this script is specialized for binary data for the subgroups, i.e., they can only have two resulting states at most.  
Typical input (red annotation added for illustrating terminology):

![df_for_binary](imgs/binary_donut_guide.png)


Typical result:

![typical_nb4](imgs/nb4_example.png)


The **fifth** notebook shows how to use a custom list of colors with the idea that you can finetune the plot for matching a color palette:

Typical result:

![typical_nb5](imgs/nb5_example.png)

-----

Click on a `launch binder` badge on this page to spin up a sesion where you can make plots.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/donut_plots_with_subgroups/master?filepath=index.ipynb)

------------------------------------

### Related 

- [gos: (epi)genomic visualization in python](https://gosling-lang.github.io/gos/) looks to create donut-plot like heat maps according to that page (although at the time I was unable to find an example of that type among the gallery that included code)