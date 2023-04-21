import os
import datetime

def generate_report(data):
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

    # content search
    searchwordlist = "wordlist here"

    # Search result information
    SearchResultLine1_inodeaddress = "inode address here"
    SearchResultLine2_Filename = "file name here"
    SearchResultLine3_FileLocation = "File Location here"

    # Standard information Attribute Value for NTFS
    StdInfoAttLine1_Created = "created timestamp here"
    StdInfoAttLine2_FileModified = "modifired timestamp here"
    StdInfoAttLine3_MFTModified = "MFT modified timestamp here"
    StdInfoAttLine4_Accessed = "accessed timestamp here"

    # Directory Entry Times for both NTFS and FAT
    DirInfoLine1_Written = "Written timestamp here"
    DirInfoLine2_Accessed = "Accessed timestamp here"
    DirInfoLine3_Created = "Created timestamp here"

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

    html_searchresult = f"""
        <p><b>Wordlist Search Result</b><br><br>
            Search for: {searchwordlist}<br>
    """

    html_searchresultinfo = f"""
        <p>Inode address:: {SearchResultLine1_inodeaddress}<br>
        File name: {SearchResultLine2_Filename}<br>
        File Location: {SearchResultLine3_FileLocation}<br></p>
    """

    html_StdInfoAtt_NTFS = f"""
        <p><b>Standard information Attribute Value</b><br>
            Created: {StdInfoAttLine1_Created}<br>
            File Modified: {StdInfoAttLine2_FileModified}<br>
            MFT Modified: {StdInfoAttLine3_MFTModified}<br>
            Accessed: {StdInfoAttLine4_Accessed}</p>
    """

    html_DirectoryEntryTimes = f"""
        <p><b>Directory Entry Times</b><br>
            Written: {DirInfoLine1_Written}<br>
            Accessed: {DirInfoLine2_Accessed}<br>
            Created: {DirInfoLine3_Created}</p>
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
        f.write(html_searchresult)

        # Search result (Adding loop later)
        f.write("<p><b>## Search Result no. </b><br>")
        f.write(html_searchresultinfo)

        if filesystemtype == "NTFS":
            f.write(html_StdInfoAtt_NTFS)
        
        f.write(html_DirectoryEntryTimes)

        # HTML Closing
        f.write(html_closing)




    pass

generate_report(1)