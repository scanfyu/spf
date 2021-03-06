**Main scripts**
- `process_data.py` process the data into 80% train, 10% test, and 1% validation sets
    - This script culls the user network such that only connections that have at least one item in common are included.
    - **Use:** `python process_data.py [ratings-file] [network-file] [output-dir]`
- `setup.sh` download code for comparison models and compile; run from scripts dir
    - **Use:** `./setup.sh`
- `study.sh` run SPF and comparison models on a specified dataset; run from scripts dir
    - **Use:** `./study [data-dir] [output-dir] [K] [directed/undirected]`
- `aggregate_results.py` aggregate results of a study into a single comma-separated file
    - **Use:** `python aggregate_results.py [study-dir] [output-file] [K]`

**Alternate data processing**
- `process_time_data.py` used to process binary data that has timestamps (ratings are 
    userID/itemID/unixTime instead of userID/itemID/rating)
    - **Use:** `python process_time_data.py [ratings-file] [network-file] [output-dir]`

**Process to data form for comparison models**
- `to_librec_form.py` process standard data form into form for LibRec; default directed network
    - **Use:** `python to_librec_form.py [data-dir] [optional:undirected]`
- `to_list_form.py` process standard data form into form for CTR/MF; same use as above
- `to_sorec_list_form.py` process standard data form into form for SoRec using CTR/MF; same use as above

**Amplification studies** (older)
- `adjust_amplification.py` create a new dataset from the src dataset,
   adjusting the percentage of items any given user shares with their
   friends
    - **Use:** `python adjust_amplification.py [ data src dir ] [ new data dir ] [ % shared ]`
- `amplify_data.py` same as above, but users will only increase their % shared, never decrease
- `deamplify_data.py` same as above, but users will only decrease their % shared, never increase
- `amplification_check.py` print out the percent of items shared with friends, averaged across all users
    - **Use:** `python amplification_check.py [data-dir]`
- `sim_data.sh` create a set of datasets, each with the same seed data, but different amplification settings
    - **Use:** `./sim_data.sh [data-dir]`
- `aggregate_amp_results.py` aggregate results of an amplification study (on a range of amplification settings)
    - **Use:** `python aggregate_amp_results [fits-dir] [out-filename]`
