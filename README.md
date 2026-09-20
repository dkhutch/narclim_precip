# Narclim Precip
Scripts to calculate precipitation Rx1day indices from NarCLIM2.0 database. Below is a quick description of each step I took to derive Rx1day plots.

1. **get_precip_filenames.py** : Scans through the NarCLIM2.0 Thredds database for each model output, and creates a list of input files (from the database) and output files for outputting Rx1day indices.
2. **calc_pr_rx1day.py** : Reads in a daily precipitation file and calculates Rx1day on a monthly basis. Requires a text file list of inputs, where each line of text contains a comma-separated ```input_file,output_file```.
3. **send_jobs.sh** : Splits the list of files to be processed into batches of 50, which are then run using qsub on the Gadi copyq. Copyq is necessary because the job needs access to the internet (for the OpenDAP access), not available on normal queue.
4. **precip_mean_20yr.py** : Calculates 20-year means of precip Rx1day indices for each model.
5. **av_mon.py** : Generic script to turn multi-year monthly data into an averaged monthly climatology (called in step 4)
6. **ens_mean_precip.py** : Calculates ensemble mean of the 20-year Rx1day averages.
7. **plot_hist_scen.py** : Generates plots of percentage change in ensemble-mean Rx1day precipitation, showing the change from 2081-2100 minus 1991-2010 for each climate change scenario.

Each script was written entirely by David Hutchinson. It's rough and ready, but can be readily adapted to different metrics or averaging techniques.