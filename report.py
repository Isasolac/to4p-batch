import os
import datetime

def generate_report(volume_data, fs_data, wordlist_data = None, hash_data = None):
    # TODO: what form should our data be stored in?
    # TODO: how can we generate a report?

    # PERSON 4
    
#output_html_path=os.getcwd()+"//"+"out.html"

    # Get current date and time
    now = datetime.datetime.now()
    current_date = now.strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")

    # Define report variable
    report_title = "Disk Analysis Report"
    team_name = "TeamOf4People (Ankshit Jain, Isabel Gardner, Matthew Woo, Thanyanun Charoensiritanasin)"

    # Image Variable
    image_file_name = "image1.dd"
    MD5_result = "MD5resulthere"
    SHA1_result = "SHA1resulthere"

    # Define HTML Output file name
    htmloutputfile = image_file_name + ".html"

    # Disk Image Information Variable
    DiskInfoLine1_DOSorGPT = "DOS Partition Table // GUID Partition Table (EFI)"
    DiskInfoLine2_OffsetSector = "0"
    DiskInfoLine3_BytePerSector = "512"

    partition1 = ["11", "12", "13", "14", "15", "16"]
    partition2 = ["21", "22", "23", "24", "25", "26"]

    filesystemtype = "NTFS" # FAT or NTFS

    # File System Information Variable
    FSInfoLine1_FileSystemType = filesystemtype
    FSInfoLine2_VolumeSerialNumber = "VolumeSerialNumberHere"

    # Metadata Information Variable for NTFS
    MetadataInfoLine1_NTFS_FirstClusterofMFT = "16"
    MetadataInfoLine2_NTFS_FirstClusterofMFTMirror = "32759"
    MetadataInfoLine3_NTFS_SizeofMFTEntries = "1024"

    # Metadata Information Variable for FAT
    MetadataInfoLine1_FAT_SectorBeforeFileSystem = "128"
    MetadataInfoLine2_FAT_TotalRange = "0 - 204799"

    # Content Information Variable
    ContentInfoLine1_SectorSize = "512"
    ContentInfoLine2_Clustersize = "1024"

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

    html_filesysteminfo_NTFS = f"""
        <p><b>File System Information</b><br>
            File System Type: {FSInfoLine1_FileSystemType}<br>
            Volume Serial Number: {FSInfoLine2_VolumeSerialNumber}</p>
    """

    html_metadatainto_NTFS = f"""
        <p><b>Metadata Information</b><br>
            First Cluster of MFT: {MetadataInfoLine1_NTFS_FirstClusterofMFT}<br>
            First Cluster of MFT Mirror: {MetadataInfoLine2_NTFS_FirstClusterofMFTMirror}<br>
            Size of MFT Entries: {MetadataInfoLine3_NTFS_SizeofMFTEntries} bytes</p>
    """

    html_contentinto_NTFS = f"""
        <p><b>Content Information</b><br>
            Sector Size: {ContentInfoLine1_SectorSize}<br>
            Cluster Size: {ContentInfoLine2_Clustersize}</p>
    """

    html_filesysteminfo_FAT = f"""
        <p><b>File System Information</b><br>
            File System Type: {FSInfoLine1_FileSystemType}<br>
            Volume ID: {FSInfoLine2_VolumeSerialNumber}</p>
    """

    html_metadatainto_FAT = f"""
        <p><b>Metadata Information</b><br>
            Sectors before file system: {MetadataInfoLine1_FAT_SectorBeforeFileSystem}<br>
            Total Range: {MetadataInfoLine2_FAT_TotalRange}</p>
    """

    html_contentinto_FAT = f"""
        <p><b>Content Information</b><br>
            Sector Size: {ContentInfoLine1_SectorSize}<br>
            Cluster Size: {ContentInfoLine2_Clustersize}</p>
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
        f.write(html_separatesection)
        f.write("<p><b>## Partition ID:</b><br>")
        f.write(html_partitiontableheader)

        f.write("<tr>\n")
        for item in partition1:
            f.write("<td>" + str(item) + "</td>\n")
        f.write("</tr>\n")

        f.write("</table></p>")

        f.write(html_partitioninfo)

        if filesystemtype == "NTFS":
            f.write(html_filesysteminfo_NTFS)
            f.write(html_metadatainto_NTFS)
            f.write(html_contentinto_NTFS)
        
        elif filesystemtype == "FAT":
            f.write(html_filesysteminfo_FAT)
            f.write(html_metadatainto_FAT)
            f.write(html_contentinto_FAT)
        

        # Searching Section
        f.write(html_separatesection)
        
        if wordlist_data is not None:
            write_wordlist_data(f, wordlist_data, filesystemtype)

        # HTML Closing
        f.write(html_closing)

def write_wordlist_data(f, wordlist_data, filesystemtype):
    FILE_NAME_TIME_MISMATCH = "Doesn't match FILE_NAME time:"
    SearchResult_number = 1
    for part_id, part_data in wordlist_data.items():
        if part_id == "Total_Occurrences":
            continue
        elif part_id == "Relevant_Partitions":
            continue
        for match, match_info in part_data["Found_Files"].items():
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
                File Location: {SearchResultLine4_FileLocation}<br>
                Partition ID: {part_id}<br></p>
            """

            f.write(html_searchresult)

            # Search result (Adding loop later)
            f.write(f"<p><b>## Search Result no. {SearchResult_number}</b><br>")
            f.write(html_searchresultinfo)

            # TODO: double check these fs type values
            if filesystemtype == "NTFS":
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
            elif filesystemtype == "FAT":
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
generate_report(1)