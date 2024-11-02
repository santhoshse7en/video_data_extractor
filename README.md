# Video Data Extractor

A Python utility for extracting and processing video file information from specified directories. 
This tool helps organize and analyze collections of video files.

## Description
The Video Data Extractor scans a directory for video files and gathers metadata such as resolution, 
size, and associated subtitles. The information is structured for easy analysis using pandas.

## Features

* Recursively searches for video files (.mp4, .mkv, .avi, .mov) and subtitle files (.srt).
* Extracts video resolution from filenames using regex.
* Formats file sizes into a human-readable format (e.g., MB, GB).
* Compiles extracted data into a Pandas DataFrame for easy manipulation and analysis.

## Installation

Ensure you have Python and the required packages installed:

```bash
pip install pandas
```

## Usage

Clone the repository:

```
git clone https://github.com/santhoshse7en/videodata-extractor.git
cd videodata-extractor
```

Use the `VideoData` class in your Python script:

```python
from video_data_extractor import VideoData

# Create an instance of the VideoData class
video_data_extractor = VideoData()

# Extract information
base_folder_path, video_info = video_data_extractor.info_extractor(
    root_dir='F:/Your/Directory',
    base_folder_name='YourBaseFolder'
)

# Create a DataFrame from the extracted data
video_dataframe = VideoData.create_dataframe(video_info)

# Print the DataFrame
print(video_dataframe)
```

### Parameters

* `root_dir` (str): The root directory to search for video files.
* `base_folder_name` (str): The name of the base folder within the root directory.
* `exclude_dirs` (list[str], optional): A list of folder names to exclude from the search.

### Methods

* `__extract_resolution_from_filename(filename: str) -> str`: Extracts video resolution from the filename.
* `__format_file_size(size: int) -> str`: Formats file sizes into a human-readable string.
* `__should_skip_folder(folder_name: str, exclude_dirs: list[str]) -> bool`: Determines if a folder should be skipped based on exclusion criteria.
* `__filter_files(filenames: list[str]) -> tuple[list[str], list[str]]`: Filters video and SRT files from the list of filenames.
* `__collect_folder_info(folder_name: str, video_files: list[str], srt_files: list[str]) -> dict`: Gathers and organizes folder-specific information.
* `info_extractor(root_dir: str, base_folder_name: str, exclude_dirs: list[str] = None) -> tuple[str, list[dict]]`: Main method to extract video file information from the specified directory and its subdirectories.
* `create_dataframe(video_data: list[dict]) -> pd.DataFrame`: Converts the collected video data into a pandas DataFrame.


## Code Structure

* Imports:

  * `os`: For file and directory handling.
  * `re`: For regular expression operations.
  * `pandas`: For data manipulation and analysis.

* Class: `VideoData`

  * Contains all methods related to video data extraction and processing.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions or 
improvements.

## Acknowledgements

Thanks to the Python community for their ongoing support and the libraries that 
make this project possible.

Feel free to adjust any specific details or add more context as needed!
