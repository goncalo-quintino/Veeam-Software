The program gets argumets from the command line. It gets:
- source path The folder with the content that should be replicated
- replica path The folder where the content should be replicated to
- sync time Time in seconds between each update of replica
- log file path Path where log file will be created

The implementation works in the following manner:
- Looks for folders in replica that don't exist in source and deletes them.
- Finds all the folders inside the original folder and creates them in replica if necessary
- Verifies what files need to be copied or deleted in replica by comparing md5 hashes
- Repeats the operations above for all the folders inside the original folder using the recursive function "sync_folder"
- This function synchronizes all the folders inside the original folder regardless of its depth
- This process is repeated each (sync time) seconds
- The program marks the time spent in the process of synchronization so that the time interval stays constant

Notes:
- The program has tests in some of the functions to exemplify the imoprtance of testing implementation
- Some functions weren't tested for lack of time

To launch the program use the command:
python Task_Goncalo_Quintino.py (source path) (replica path) (sync time) (log path)

To run the tests use the command:
pytest Task_Goncalo_Quintino.py 