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
    MD5_result = "MD5resulthere"
    SHA1_result = "SHA1resulthere"

    # Define HTML Output file name
    htmloutputfile = image_file_name + ".html"

    # Disk Image Information Variable
    DiskInfoLine1_DOSorGPT = volume_data["Volume"]
    DiskInfoLine2_OffsetSector = volume_data["Offset_Sector"]
    DiskInfoLine3_BytePerSector = volume_data["Sector_Size"]

    partition1 = ["11", "12", "13", "14", "15", "16"]
    partition2 = ["21", "22", "23", "24", "25", "26"]

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

    html_partitioninfo = f"""
        <p><b>Hash Result</b><br>
        MD5: {MD5_result}<br>
        SHA-1: {SHA1_result}</p>
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
        f.write("<p><b>List Partition Information</b><br>")
        f.write(html_partitiontableheader)

        f.write("<tr>\n")
        for item in partition1:
            f.write("<td>" + str(item) + "</td>\n")
        f.write("</tr>\n")

        f.write("<tr>\n")
        for item in partition2:
            f.write("<td>" + str(item) + "</td>\n")
        f.write("</tr>\n")

        f.write("</table></p>")

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
            # FIXME: Add hash data
            f.write(html_partitioninfo)
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
        if wordlist_data is not None:
            write_wordlist_data(f, wordlist_data, fs_data)

        # HTML Closing
        f.write(html_closing)

def write_wordlist_data(f, fs_data):
    FILE_NAME_TIME_MISMATCH = "Doesn't match FILE_NAME time:"
    SearchResult_number = 1
    fs_type = fs_data["Object"].type
    for match, match_info in fs_data["WordList"]["Found_Files"].items():
        # Content search
        searchwordlist = match

        # Search result information
        SearchResultLine1_cluster = match_info["Cluster"]
        SearchResultLine2_inodeaddress = match_info["Inode"]
        SearchResultLine3_Filename = match_info["Filename"] if match_info["Filename"] is not None else "Not Found"
        SearchResultLine4_FileLocation = match_info["Filepath"] if match_info["Filepath"] is not None else "Not Found"

        html_searchresult = f"""
            <p><b>Wordlist Search Result</b><br><br>
                Search for: {searchwordlist}<br>
        """

        html_searchresultinfo = f"""
            <p>Cluster: {SearchResultLine1_cluster}<br>
            Inode address: {SearchResultLine2_inodeaddress}<br>
            File name: {SearchResultLine3_Filename}<br>
            File Location: {SearchResultLine4_FileLocation}<br></p>
        """

        f.write(html_searchresult)

        # Search result (Adding loop later)
        f.write(f"<p><b>## Search Result no. {SearchResult_number}</b><br>")
        f.write(html_searchresultinfo)

        # TODO: double check these fs type values
        if fs_type == fs.SupportedTypes.NTFS:
            FileNameTime_Created = match_info["Metadata"]["File_Name_Times"][0]
            FileNameTime_FileModified = match_info["Metadata"]["File_Name_Times"][1]
            FileNameTime_MFTModified = match_info["Metadata"]["File_Name_Times"][2]
            FileNameTime_Accessed = match_info["Metadata"]["File_Name_Times"][3]

            # Standard information Attribute Value for NTFS
            StdInfoAttLine1_Created = match_info["Metadata"]["Standard_Info_Times"][0] + ("" if match_info["Metadata"]["Matching"][0] else f" ({FILE_NAME_TIME_MISMATCH} {FileNameTime_Created})")
            StdInfoAttLine2_FileModified = match_info["Metadata"]["Standard_Info_Times"][1] + ("" if match_info["Metadata"]["Matching"][1] else f" ({FILE_NAME_TIME_MISMATCH} {FileNameTime_FileModified})")
            StdInfoAttLine3_MFTModified = match_info["Metadata"]["Standard_Info_Times"][2] + ("" if match_info["Metadata"]["Matching"][2] else f" ({FILE_NAME_TIME_MISMATCH} {FileNameTime_MFTModified})")
            StdInfoAttLine4_Accessed = match_info["Metadata"]["Standard_Info_Times"][3] + ("" if match_info["Metadata"]["Matching"][3] else f" ({FILE_NAME_TIME_MISMATCH} {FileNameTime_Accessed})")

            html_StdInfoAtt_NTFS = f"""
                <p><b>Standard Information Attribute Value</b><br>
                    Created: {StdInfoAttLine1_Created}<br>
                    File Modified: {StdInfoAttLine2_FileModified}<br>
                    MFT Modified: {StdInfoAttLine3_MFTModified}<br>
                    Accessed: {StdInfoAttLine4_Accessed}<br>
                    Mismatching times may indicate anti-forensic tampering.</p>
            """
            f.write(html_StdInfoAtt_NTFS)
        elif fs_type == fs.SupportedTypes.FAT16 or fs_type == fs.SupportedTypes.FAT32:
            # Directory Entry Times for FAT
            DirInfoLine1_Written = match_info["Metadata"]["Times"][0]
            DirInfoLine2_Accessed = match_info["Metadata"]["Times"][1]
            DirInfoLine3_Created = match_info["Metadata"]["Times"][2]

            html_DirectoryEntryTimes = f"""
                <p><b>Directory Entry Times</b><br>
                    Written: {DirInfoLine1_Written}<br>
                    Accessed: {DirInfoLine2_Accessed}<br>
                    Created: {DirInfoLine3_Created}</p>
            """
            f.write(html_DirectoryEntryTimes)
        SearchResult_number += 1

