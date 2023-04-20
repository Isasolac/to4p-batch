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
    DiskInfoLine1 = "DOS Partition Table"
    DiskInfoLine2 = "Offset Sector: 0"
    DiskInfoLine3 = "Units are in 512-byte sectors"

    partition1 = ["11", "12", "13", "14", "15", "16"]
    partition2 = ["21", "22", "23", "24", "25", "26"]

    # File System Information Variable
    FSInfoLine1 = "FAT/NTFS"
    FSInfoLine2 = "VolumeSerialNumber"
    FSInfoLine3 = "OEMName"
    FSInfoLine4 = "VolumeName"
    FSInfoLine5 = "Version"

    # Metadata Information Variable
    MetadataInfoLine1 = "16"
    MetadataInfoLine2 = "32759"
    MetadataInfoLine3 = "1024"
    MetadataInfoLine4 = "4096"
    MetadataInfoLine5 = "0 - 251"
    MetadataInfoLine6 = "5"

    # Content Information Variable
    ContentInfoLine1 = "512"
    ContentInfoLine2 = "1024"
    ContentInfoLine3 = "0 - 65518"
    ContentInfoLine4 = "0 - 131038"

    # content search
    searchwordlist = "wordlist here"

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
            {DiskInfoLine1}<br>
            {DiskInfoLine2}<br>
            {DiskInfoLine3}</p>
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

    html_filesysteminfo = f"""
        <p><b>Disk Image Information</b><br>
            File System Type: {FSInfoLine1}<br>
            {FSInfoLine2}<br>
            {FSInfoLine3}<br>
            {FSInfoLine4}<br>
            {FSInfoLine5}</p>
    """

    html_metadatainto = f"""
        <p><b>Metadata Information</b><br>
            First Cluster of MFT: {MetadataInfoLine1}<br>
            First Cluster of MFT Mirror: {MetadataInfoLine2}<br>
            Size of MFT Entries: {MetadataInfoLine3} bytes<br>
            Size of Index Records {MetadataInfoLine4} bytes <br>
            Range: {MetadataInfoLine5}<br>
            Root Directory: {MetadataInfoLine6}</p>
    """

    html_contentinto = f"""
        <p><b>Content Information</b><br>
            Sector Size: {ContentInfoLine1}<br>
            Cluster Size: {ContentInfoLine2}<br>
            Total Cluster Range: {ContentInfoLine3}<br>
            Total Sector Range: {ContentInfoLine4}</p>
    """

    html_searchresult = f"""
        <p><b>Search Result</b><br><br>
            Search for: {searchwordlist}<br>
            Result:<br>
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
        f.write("<p>List Partition Information<br>")
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
        f.write("<p><b>## Partition no.</b><br>")
        f.write(html_partitiontableheader)

        f.write("<tr>\n")
        for item in partition1:
            f.write("<td>" + str(item) + "</td>\n")
        f.write("</tr>\n")

        f.write("</table></p>")

        f.write(html_partitioninfo)
        f.write(html_filesysteminfo)
        f.write(html_metadatainto)
        f.write(html_contentinto)

        # Searching Section
        f.write(html_separatesection)
        f.write(html_searchresult)

        # HTML Closing
        f.write(html_closing)







    pass