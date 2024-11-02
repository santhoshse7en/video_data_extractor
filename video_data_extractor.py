import os
import re
import pandas as pd


class VideoData:
    """A class to extract and process video file information from a specified directory."""

    def info_extractor(
            self,
            root_dir: str,
            base_folder_name: str,
            exclude_dirs: list[str] = None
    ) -> tuple[str, list[dict]]:
        """Extract video file information from the specified directory and its subdirectories."""
        video_data = []
        exclude_dirs = exclude_dirs or []
        base_folder_path = os.path.join(root_dir, base_folder_name)

        # Check if the base folder exists
        if not os.path.exists(base_folder_path):
            print(f"The folder '{base_folder_path}' does not exist.")
            return base_folder_path, video_data

        for folder_name, subfolders, filenames in os.walk(base_folder_path):
            if self.__should_skip_folder(folder_name, exclude_dirs):
                continue

            video_files, srt_files = self.__filter_files(filenames)

            if video_files or srt_files:
                folder_info = self.__collect_folder_info(folder_name, video_files, srt_files)
                video_data.append(folder_info)

        return base_folder_path, video_data

    @staticmethod
    def create_dataframe(video_data):
        """Create a DataFrame from video data."""
        return pd.DataFrame(video_data)

    @staticmethod
    def __extract_resolution_from_filename(filename):
        """Extract resolution from the filename using regex."""
        match = re.search(r"(\d{3,4})p", filename, re.IGNORECASE)
        if match:
            return f"{match.group(1)}P"  # Return resolution in the format "720P", "1080P", etc.
        return ""

    @staticmethod
    def __format_file_size(size):
        """Convert file size to a human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"  # Format the size in the appropriate unit
            size /= 1024.0
        return f"{size:.1f} TB"

    @staticmethod
    def __should_skip_folder(folder_name: str, exclude_dirs: list[str]) -> bool:
        """Check if the folder should be skipped based on exclusion criteria."""
        return (
                any(excluded in folder_name for excluded in exclude_dirs) or
                "subs" in folder_name.lower()
        )

    @staticmethod
    def __filter_files(filenames: list[str]) -> tuple[list[str], list[str]]:
        """Filter video and SRT files from the list of filenames."""
        video_files = [f for f in filenames if f.endswith((".mp4", ".mkv", ".avi", ".mov"))]
        srt_files = [f for f in filenames if f.endswith(".srt")]
        return video_files, srt_files

    def __collect_folder_info(
            self,
            folder_name: str,
            video_files: list[str],
            srt_files: list[str]
    ) -> dict:
        """Collect information about the folder and its video and SRT files."""
        folder_path = os.path.abspath(folder_name)
        name = os.path.basename(folder_name)
        year = name.split("[")[-1].split("]")[0].strip() if "[" in name else ""
        total_files = video_files + srt_files

        # Calculate sizes of video files
        video_files_size = sum(os.path.getsize(os.path.join(folder_name, f)) for f in video_files)
        resolution = self.__extract_resolution_from_filename(video_files[0]) if video_files else ""
        resolution_count = 1 if resolution else 0

        return {
            "Name": name,
            "Year": year,
            "Resolution": resolution,
            "Resolution Count": resolution_count,
            "Video Files": video_files,
            "Video Files Count": len(video_files),
            "Video Files Size": self.__format_file_size(video_files_size),
            "Video Files Size Count": len(video_files),
            "SRT Files": srt_files,
            "SRT Files Count": len(srt_files),
            "folder_paths": [folder_path],
            "folder_paths Count": 1,
            "Total Files List": total_files,
            "Total Files Count": len(total_files),
            "File Formats": list(set(f.split(".")[-1] for f in total_files)),  # Unique file formats
            "Location": folder_path
        }
