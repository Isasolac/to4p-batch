import os
import datetime
import parse_fs as fs

def handle_fs_data(filesystem: fs.FileSystem):
    filesystem_info = "Not Analysed<br><br>"
    metadata_info = ""
    content_info = ""

    if filesystem.type == fs.SupportedTypes.NTFS:
        type = "NTFS"
        filesystem_info = f"""
            <p><b>File System Information</b><br>
                File System Type: {type}<br>
                Volume Serial Number: {filesystem.volume_serial_number}</p>
        """    
        metadata_info = f"""
            <p><b>Metadata Information</b><br>
                First Cluster of MFT: {filesystem.first_cluster_of_mft}<br>
                First Cluster of MFT Mirror: {filesystem.first_cluster_of_mft_mirror}<br>
                Size of MFT Entries: {filesystem.size_of_mft_entries}</p>
        """
        content_info = f"""
            <p><b>Content Information</b><br>
                Sector Size: {filesystem.sector_size}<br>
                Cluster Size: {filesystem.cluster_size}</p>
        """
    elif filesystem.type == fs.SupportedTypes.FAT16 or filesystem.type == fs.SupportedTypes.FAT32:
        type = "FAT16" if filesystem.type == fs.SupportedTypes.FAT16 else "FAT32"
        
        filesystem_info = f"""
            <p><b>File System Information</b><br>
                File System Type: {type}<br>
                Volume ID: {filesystem.volume_id}</p>
        """

        metadata_info = f"""
            <p><b>Metadata Information</b><br>
                Sectors before file system: {filesystem.sectors_before_file_system}<br>
                Total Range: {filesystem.total_range}</p>
        """

        content_info = f"""
            <p><b>Content Information</b><br>
                Sector Size: {filesystem.sector_size}<br>
                Cluster Size: {filesystem.cluster_size}</p>
        """
    return filesystem_info, metadata_info, content_info

def write_hash_data(f, hash_data):
    if len(hash_data) == 0:
        return
    f.write(f"<p><b>Hash Search Result</b><br>")
    f.write(f"""
            <table border="1">
                <tr><b>
                    <th>Inode</th>
                    <th>File</th>
                    <th>Type</th>
                    <th>Last Access Time</th>
                    <th>MD5 Hash</th>
                    <th>SHA1 Hash</th>
                </tr></b>
    """)
    for entry in hash_data:
        f.write("<tr>\n")
        f.write("<td>" + entry['inode'] + "</td>\n")
        f.write("<td>" + entry["filename"] + "</td>\n")
        f.write("<td>" + entry["type"] + "</td>\n")
        f.write("<td>" + entry["atime"] + "</td>\n")
        if entry["matching_hash"] == "md5":
            f.write("<td><b>" + entry["md5"] + "</b></td>\n")
            f.write("<td>" + entry["sha1"] + "</td>\n")
        else:
            f.write("<td>" + entry["md5"] + "</td>\n")
            f.write("<td><b>" + entry["sha1"] + "</b></td>\n")
        f.write("</tr>\n")

    f.write("</table></p>")


def generate_report(volume_data, fs_data: dict, wordlist_data = None):
    
    # Get current date and time
    now = datetime.datetime.now()
    current_date = now.strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")

    # Define report variable
    report_title = "Disk Analysis Report"
    team_name = "TeamOf4People (Ankshit Jain, Isabel Gardner, Matthew Woo, Thanyanun Charoensiritanasin)"

    # Image Variable
    image_file_name = volume_data["Name"]
    MD5_result = volume_data["MD5"]
    SHA1_result = volume_data["SHA1"]

    # Define HTML Output file name
    htmloutputfile = image_file_name + ".html"

    # Disk Image Information Variable
    DiskInfoLine1_DOSorGPT = volume_data["Volume"]
    DiskInfoLine2_OffsetSector = volume_data["Offset_Sector"]
    DiskInfoLine3_BytePerSector = volume_data["Sector_Size"]

    # Define HTML report structure
    html_opening = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{report_title}</title>
        </head>
        <body style="background-color: rgb(223, 207, 190);">
            <center><h1><b>{report_title}</b></h1></center>
            <center><p>Generated on: {current_date} {current_time} EST <br>
            By {team_name}</p></center><br>
    """

    html_imageinfo = f"""
        <p><b>Image File:</b> {image_file_name}</p>
                <p><b>Hash Result</b><br>
                MD5: {MD5_result}<br>
                SHA-1: {SHA1_result}</p>
    """

    html_diskinfo = f"""
        <p><b>Disk Image Information</b><br>
            {DiskInfoLine1_DOSorGPT}<br>
            Offset Sector: {DiskInfoLine2_OffsetSector}<br>
            Units are in {DiskInfoLine3_BytePerSector}-byte sectors</p>
    """

    html_partitiontableheader = f"""
            <table border="1">
                <tr><b>
                    <th>Partition ID</th>
                    <th>Slot</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Length</th>
                    <th>Description</th>
                </tr></b>
    """

    html_separatesection = f"""
        <b>---------------------------------------------------------------------------------------</b>
    """

    html_closing = f"""
    </body>
    </html>
    """

    # Open the output file in write mode
    with open(htmloutputfile, "w") as f:
        # HTML Opening
        f.write(html_opening)
        
        # Input Image Information
        f.write(html_imageinfo)

        # Disk Image Information (Adding loop later)
        f.write(html_diskinfo)

        # Add portion about filesystem matches here
        if volume_data["File_Matches"] is not None:
            write_filematch_data(f, volume_data["File_Matches"], volume_data["Name"])

        # Partition Information (Adding loop later)
        for partition_id in fs_data:
            data = fs_data[partition_id]
            if not data["Partition"]:
                continue

            f.write(html_separatesection)
            f.write(f"<p><b>## Partition {partition_id}: </b><br>")
            f.write(html_partitiontableheader)
            f.write("<tr>\n")
            f.write("<td>" + partition_id + "</td>\n")
            f.write("<td>" + data["Slot"] + "</td>\n")
            f.write("<td>" + data["Start"] + "</td>\n")
            f.write("<td>" + data["End"] + "</td>\n")
            f.write("<td>" + data["Size"] + "</td>\n")
            f.write("<td>" + data["Description"] + "</td>\n")
            f.write("</tr>\n")

            f.write("</table></p>")
            f.write(f"""
                <p><b>Hash Result</b><br>
                MD5: {data["MD5"]}<br>
                SHA-1: {data["SHA1"]}</p>
            """)
            filesystem_info, metadata_info, content_info = handle_fs_data(data["Object"])
            f.write(filesystem_info)
            f.write(metadata_info)
            f.write(content_info)
            if data["HashList"] is not None:
                write_hash_data(f, data["HashList"])
            if data["WordList"] is not None:
                write_wordlist_data(f, data)

        # Searching Section
        f.write(html_separatesection)

        # HTML Closing
        f.write(html_closing)

'''
file_matches: dict where keys are image names
and values are a triple of (hash, filename, matched image name)
'''
def write_filematch_data(f, file_matches, name):

    f.write(f"<p><b>File Match Search Results</b><br>")

    if len(file_matches) == 0:
        f.write(f"No matches found across images.")
        return
    elif len(file_matches[name]) == 0:
        f.write(f"No matches found for this image.")
    
    file_list = file_matches[name]
    f.write(f"""
            <table border="1">
                <tr><b>
                    <th>Matched Hash</th>
                    <th>Filename</th>
                    <th>Matched Image</th>
                </tr></b>
    """)

    for file_info in file_list:
        matched_hash = file_info[0]
        filename = file_info[1]
        matched_image = file_info[2]

        f.write("<tr>\n")
        f.write("<td>" + matched_hash + "</td>\n")
        f.write("<td>" + filename + "</td>\n")
        f.write("<td>" + matched_image + "</td>\n")
        f.write("</tr>\n")
    
    f.write("</table></p>")

def write_wordlist_data(f, fs_data):
    if len(fs_data["WordList"]["Found_Files"]) == 0:
        return
    f.write(f"<p><b>Word List Search Results</b><br>")
    f.write(f"""
            <table border="1">
                <tr><b>
                    <th>Found Words</th>
                    <th>File Location</th>
                    <th>Inode Address</th>
                    <th>Last Access Time</th>
                    <th>Tampered With?</th>
                </tr></b>
    """)
    fs_type = fs_data["Object"].type
    for match, entry in fs_data["WordList"]["Found_Files"].items():
        f.write("<tr>\n")
        f.write("<td>" + ", ".join(entry["Matched_Words"]) + "</td>\n")
        f.write("<td>" + entry["Filepath"] + "</td>\n")
        f.write("<td>" + entry["Inode"] + "</td>\n")
        if entry["Metadata"] is None:
            f.write("<td>Not found</td>\n")
            f.write("<td>Unknown</td>\n")
        elif fs_type == fs.SupportedTypes.NTFS:
            f.write("<td>" + entry["Metadata"]["Standard_Info_Times"][3].split(":", 1)[1] + "</td>\n")
            f.write("<td>" + ("No" if all(entry["Metadata"]["Matching"]) else "Unlikely" if entry["Metadata"]["Matching"][0] and entry["Metadata"]["Matching"][2] else "Maybe") + "</td>\n")
        elif fs_type == fs.SupportedTypes.FAT16 or fs_type == fs.SupportedTypes.FAT32:
            f.write("<td>" + entry["Metadata"]["Times"][1].split(":", 1)[1] + "</td>\n")
            f.write("<td>N/a</td>\n")
        else:
            f.write("<td></td>\n")
            f.write("<td></td>\n")
        f.write("</tr>\n")

    f.write("</table></p>")

