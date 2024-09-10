# Checks the integrity of Septentrio SBF binary files

# Written by: Paul Clark
# Last update: September 10th, 2024

# Reads a SBF file and checks the integrity of SBF, NMEA and RTCM data
# Will rewind and re-sync if an error is found
# Will create a repaired file if desired

# SparkFun code, firmware, and software is released under the MIT License (http://opensource.org/licenses/MIT)
#
# The MIT License (MIT)
#
# Copyright (c) 2024 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os

# Add byte to CRC-24Q (RTCM) checksum
def crc24q(byte, sum):
    crc = sum # Seed is 0

    crc ^= byte << 16 # XOR-in incoming

    for i in range(8):
        crc <<= 1
        if (crc & 0x1000000):
            # CRC-24Q Polynomial:
            # gi = 1 for i = 0, 1, 3, 4, 5, 6, 7, 10, 11, 14, 17, 18, 23, 24
            # 0b 1 1000 0110 0100 1100 1111 1011
            crc ^= 0x1864CFB # CRC-24Q

    return crc & 0xFFFFFF

#    SBF Message
#
#    |<-- Preamble --->|
#    |                 |
#    +--------+--------+---------+---------+---------+---------+
#    |  SYNC  |  SYNC  |   CRC   |   ID    | Length  | Payload |
#    | 8 bits | 8 bits | 16 bits | 2 bytes | 2 bytes | n bytes |
#    |  0x24  |  0x40  |         |         |         |         |
#    +--------+--------+---------+---------+---------+---------+
#                                |                             |
#                                |<-------- Checksum --------->|
#
#  The generator polynomial for the CRC is the so-called CRC-CCITT
#  polynomial: x16 +x12 +x5 +x0. The CRC is computed in the forward
#  direction using a seed of 0, no reverse and no final XOR.

ccitt_crc_table = [
    0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
    0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
    0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
    0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
    0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
    0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
    0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
    0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
    0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
    0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
    0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
    0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
    0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
    0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
    0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
    0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
    0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
    0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
    0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
    0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
    0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
    0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
    0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
    0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
    0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0 
]

def ccitt_crc_update(crc, data):
    tbl_idx = ((crc >> 8) ^ data) & 0xFF
    new_crc = (ccitt_crc_table[tbl_idx]) ^ (crc << 8)
    return new_crc & 0xFFFF

print('SBF Integrity Checker')
print()

filename = ''

if filename == '':
    # Check if the bin filename was passed in argv
    if len(sys.argv) > 1: filename = sys.argv[1]

# Find first .sbf file in the current directory
firstfile = ''
for root, dirs, files in os.walk("."):
    if len(files) > 0:
        if root == ".": # Comment this line to check sub-directories too
            for afile in files:
                if afile[-4:] == '.sbf':
                    if firstfile == '': firstfile = os.path.join(root, afile)

# Ask user for filename offering firstfile as the default
if filename == '': filename = input('Enter the SBF filename (default: ' + firstfile + '): ') # Get the filename
if filename == '': filename = firstfile

# Ask user if the data contains NMEA messages
response = input('Could this file contain any NMEA messages? (Y/n): ') # Get the response
if (response == '') or (response == 'Y') or (response == 'y'):
    containsNMEA = True
else:
    containsNMEA = False

# Ask user if the data contains RTCM messages
response = input('Could this file contain any RTCM messages? (Y/n): ') # Get the response
if (response == '') or (response == 'Y') or (response == 'y'):
    containsRTCM = True
else:
    containsRTCM = False

# Ask user if the file should be repaired
response = input('Do you want to repair the file? (y/N): ') # Get the response
if (response == '') or (response == 'N') or (response == 'n'):
    repairFile = False
else:
    repairFile = True
    if (filename[-4] == '.'):
        repairFilename = filename[:-4] + '.repair' + filename[-4:]
    else:
        repairFilename = filename + '.repair'

print()
print('Processing',filename)
print()
filesize = os.path.getsize(filename) # Record the file size

# Try to open file for reading
try:
    fi = open(filename,"rb")
except:
    raise Exception('Invalid file!')

# Try to open repair file for writing
if (repairFile):
    try:
        fo = open(repairFilename,"wb")
    except:
        raise Exception('Could not open repair file!')

processed = -1 # The number of bytes processed
messages = {} # The collected message types
keepGoing = True

# Sync 'state machine'
looking_for_dollar_D3       = 0 # Looking for SBF '$', NMEA '$' or RTCM 0xD3
looking_for_at_char         = 1 # Looking for SBF '@' or NMEA char (A-Z)
looking_for_crc1            = 2 # Looking for SBF CRC byte 1 (LSB)
looking_for_crc2            = 3 # Looking for SBF CRC byte 2 (MSB)
looking_for_id1             = 4 # Looking for SBF ID byte 1 (LSB)
looking_for_id2             = 5 # Looking for SBF ID byte 2 (MSB)
looking_for_length_LSB      = 6 # Looking for SBF Length LSB
looking_for_length_MSB      = 7 # Looking for SBF Length MSB
processing_SBF_payload      = 8 # Processing the SBF payload. Keep going until (length - 8) bytes have been processed
sync_lost                   = 9 # Go into this state if sync is lost (bad checksum etc.)
looking_for_asterix         = 10 # Looking for NMEA '*'
looking_for_csum1           = 11 # Looking for NMEA checksum bytes
looking_for_csum2           = 12
looking_for_term1           = 13 # Looking for NMEA terminating bytes (CR and LF)
looking_for_term2           = 14
looking_for_RTCM_len1       = 15 # Looking for RTCM length byte (2 MS bits)
looking_for_RTCM_len2       = 16 # Looking for RTCM length byte (8 LS bits)
looking_for_RTCM_type1      = 17 # Looking for RTCM Type byte (8 MS bits, first byte of the payload)
looking_for_RTCM_type2      = 18 # Looking for RTCM Type byte (4 LS bits, second byte of the payload)
looking_for_RTCM_subtype    = 19 # Looking for RTCM Sub-Type byte (8 LS bits, third byte of the payload)
processing_RTCM_payload     = 20 # Processing RTCM payload bytes
looking_for_RTCM_csum1      = 21 # Looking for the first 8 bits of the CRC-24Q checksum
looking_for_RTCM_csum2      = 22 # Looking for the second 8 bits of the CRC-24Q checksum
looking_for_RTCM_csum3      = 23 # Looking for the third 8 bits of the CRC-24Q checksum

sbf_nmea_state = sync_lost # Initialize the state machine

# Storage for SBF messages
sbf_checksum = 0
sbf_expected_checksum = 0
sbf_ID = 0
sbf_ID_rev = 0
sbf_length = 0
sbf_bytes_remaining = 0
longest_SBF = 0 # The length of the longest SBF message
longest_SBF_candidate = 0 # Candidate for the length of the longest valid SBF message

# Storage for NMEA messages
nmea_length = 0
nmea_char_1 = 0 # e.g. G
nmea_char_2 = 0 # e.g. P
nmea_char_3 = 0 # e.g. G
nmea_char_4 = 0 # e.g. G
nmea_char_5 = 0 # e.g. A
nmea_csum = 0
nmea_csum1 = 0
nmea_csum2 = 0
nmea_expected_csum1 = 0
nmea_expected_csum2 = 0
longest_NMEA = 0 # The length of the longest valid NMEA message

# Storage for RTCM messages
rtcm_length = 0
rtcm_type = 0
rtcm_subtype = 0
rtcm_expected_csum = 0
rtcm_actual_csum = 0
longest_rtcm = 0 # The length of the longest valid RTCM message
longest_rtcm_candidate = 0 # Candidate for the length of the longest valid RTCM message

max_nmea_len = 128 # Maximum length for an NMEA message: use this to detect if we have lost sync while receiving an NMEA message
max_rtcm_len = 1023 + 6 # Maximum length for a RTCM message: use this to detect if we have lost sync while receiving a RTCM message
sync_lost_at = -1 # Record where we lost sync
rewind_to = -1 # Keep a note of where we should rewind to if sync is lost
rewind_attempts = 0 # Keep a note of how many rewinds have been attempted
max_rewinds = 100 # Abort after this many rewinds
rewind_in_progress = False # Flag to indicate if a rewind is in progress
resyncs = 0 # Record the number of successful resyncs
resync_in_progress = False # Flag to indicate if a resync is in progress
message_start_byte = 0 # Record where the latest message started (for resync reporting)

rewind_repair_file_to = 0 # Keep a note of where to rewind the repair file to if sync is lost
repaired_file_bytes = 0 # Keep a note of how many bytes have been written to the repair file

try:
    while keepGoing:

        # Read one byte from the file
        fileBytes = fi.read(1)
        if (len(fileBytes) == 0):
            print('ERROR: Read zero bytes. End of file?! Or zero file size?!')
            raise Exception('End of file?! Or zero file size?!')
        c = fileBytes[0]

        processed = processed + 1 # Keep a record of how many bytes have been read and processed

        # Write the byte to the repair file if desired
        if (repairFile):
            fo.write(fileBytes)
            repaired_file_bytes = repaired_file_bytes + 1

        # Process data bytes according to sbf_nmea_state
        # For SBF messages:
        # Preamble 1: '$'
        # Preamble 2: '@'
        # CRC (CCITT): two bytes, little endian
        # ID: two bytes, little endian
        # Length: two bytes, little endian
        # Payload: (length - 8) bytes
        #
        # For NMEA messages:
        # Starts with a '$'
        # The next five characters indicate the message type (stored in nmea_char_1 to nmea_char_5)
        # Message fields are comma-separated
        # Followed by an '*'
        # Then a two character checksum (the logical exclusive-OR of all characters between the $ and the * as ASCII hex)
        # Ends with CR LF
        # Only allow a new file to be opened when a complete packet has been processed and sbf_nmea_state has returned to "looking_for_B5_dollar_D3"
        # Or when a data error is detected (sync_lost)
        #
        # For RTCM messages:
        # Byte0 is 0xD3
        # Byte1 contains 6 unused bits plus the 2 MS bits of the message length
        # Byte2 contains the remainder of the message length
        # Byte3 contains the first 8 bits of the message type
        # Byte4 contains the last 4 bits of the message type and (optionally) the first 4 bits of the sub type
        # Byte5 contains (optionally) the last 8 bits of the sub type
        # Payload
        # Checksum: three bytes CRC-24Q (calculated from Byte0 to the end of the payload, with seed 0)

        if (sbf_nmea_state == looking_for_dollar_D3) or (sbf_nmea_state == sync_lost):
            if (c == 0x24): # Have we found SBF / NMEA $ if we were expecting one?
                if (sbf_nmea_state == sync_lost):
                    print("SBF / NMEA Preamble (0x24) found at byte "+str(processed))
                    print()
                sbf_nmea_state = looking_for_at_char # Now look for SBF Preamble 2 (@) or NMEA char (A-Z)
                message_start_byte = processed # Record the message start byte for resync reporting
            elif (c == 0xD3) and (containsRTCM == True): # Have we found 0xD3 if we were expecting one?
                if (sbf_nmea_state == sync_lost):
                    print("RTCM 0xD3 found at byte "+str(processed))
                    print()
                sbf_nmea_state = looking_for_RTCM_len1 # Now keep going until we receive the checksum
                rtcm_expected_csum = 0 # Reset the RTCM csum with a seed of 0. Update it as each character arrives
                rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
                message_start_byte = processed # Record the message start byte for resync reporting
            else:
                #print("Was expecting SBF / NMEA $ or RTCM 0xD3 but did not receive one!")
                if (c == 0xD3):
                    print("Warning: 0xD3 found at byte "+str(processed)+"! Are you sure this file does not contain RTCM messages?")
                    print()
                sync_lost_at = processed
                sbf_nmea_state = sync_lost

        # SBF / NMEA messages
        elif (sbf_nmea_state == looking_for_at_char):
            if (c == 0x40): # Have we found an SBF '@'?
                sbf_nmea_state = looking_for_crc1 # Now look for CRC1 (LSB)
            elif ((chr(c) >= 'A') and (chr(c) <= 'Z')) and (containsNMEA == True): # Have we found an NMEA char (A-Z) if we were expecting one?
                sbf_nmea_state = looking_for_asterix # Now keep going until we receive an asterix
                nmea_length = 1 # Reset nmea_length then use it to check for excessive message length
                nmea_csum = 0 ^ c # Reset the nmea_csum. Update it as each character arrives
                nmea_char_1 = c
                nmea_char_2 = 0x30 # Reset the next four NMEA chars to something invalid
                nmea_char_3 = 0x30
                nmea_char_4 = 0x30
                nmea_char_5 = 0x30
            else:
                if (chr(c) >= 'A') and (chr(c) <= 'Z'):
                    print("Warning: " + chr(c) + " found at byte " + str(processed) + "! Are you sure this file does not contain NMEA messages?")
                    print()
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost

        # SBF messages
        elif (sbf_nmea_state == looking_for_crc1):
            sbf_expected_checksum = c
            sbf_nmea_state = looking_for_crc2 # Now look for CRC2 (MSB)
        elif (sbf_nmea_state == looking_for_crc2):
            sbf_expected_checksum |= c << 8
            sbf_checksum = 0
            sbf_nmea_state = looking_for_id1 # Now look for ID byte
        elif (sbf_nmea_state == looking_for_id1):
            sbf_checksum = ccitt_crc_update(sbf_checksum, c)
            sbf_ID = c
            sbf_nmea_state = looking_for_id2
        elif (sbf_nmea_state == looking_for_id2):
            sbf_checksum = ccitt_crc_update(sbf_checksum, c)
            sbf_ID |= c << 8
            sbf_ID &= 0x1FFF # Limit ID to 13 bits
            message_type = str(sbf_ID)
            sbf_ID_rev = c >> 5 # ID Rev is 3 bits
            sbf_nmea_state = looking_for_length_LSB
        elif (sbf_nmea_state == looking_for_length_LSB):
            sbf_checksum = ccitt_crc_update(sbf_checksum, c)
            sbf_length = c
            sbf_nmea_state = looking_for_length_MSB
        elif (sbf_nmea_state == looking_for_length_MSB):
            sbf_checksum = ccitt_crc_update(sbf_checksum, c)
            sbf_length |= c << 8
            if sbf_length % 4 == 0:
                sbf_bytes_remaining = sbf_length - 8
                longest_SBF_candidate = sbf_length # Update the longest SBF message length candidate
                rewind_to = processed # If we lose sync due to dropped bytes then rewind to here
                sbf_nmea_state = processing_SBF_payload
            else:
                print("Panic!! SBF length is not modulo 4!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync.")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
        elif (sbf_nmea_state == processing_SBF_payload):
            sbf_checksum = ccitt_crc_update(sbf_checksum, c)
            sbf_bytes_remaining = sbf_bytes_remaining - 1
            if (sbf_bytes_remaining == 0):
                sbf_nmea_state = looking_for_dollar_D3 # All bytes received so go back to looking for a new Sync Char 1 unless there is a checksum error
                if (sbf_checksum != sbf_expected_checksum):
                    print("Panic!! SBF checksum error!")
                    print("Sync lost at byte "+str(processed)+". Attemting to re-sync.")
                    print()
                    sync_lost_at = processed
                    resync_in_progress = True
                    sbf_nmea_state = sync_lost
                else:
                    # Valid SBF message was received. Check if we have seen this message type before
                    if message_type in messages:
                        messages[message_type] += 1 # if we have, increment its count
                    else:
                        messages[message_type] = 1 # if we have not, set its count to 1
                    if (longest_SBF_candidate > longest_SBF): # Update the longest SBF message length
                        longest_SBF = longest_SBF_candidate
                    rewind_in_progress = False # Clear rewind_in_progress
                    rewind_to = -1
                    if (resync_in_progress == True): # Check if we are resyncing
                        resync_in_progress = False # Clear the flag now that a valid message has been received
                        resyncs += 1 # Increment the number of successful resyncs
                        print("Sync successfully re-established at byte "+str(processed)+". The SBF message started at byte "+str(message_start_byte))
                        print()
                        if (repairFile):
                            fo.seek(rewind_repair_file_to) # Rewind the repaired file
                            repaired_file_bytes = rewind_repair_file_to
                            fi.seek(message_start_byte) # Copy the valid message into the repair file
                            repaired_bytes_to_write = processed - message_start_byte
                            fileBytes = fi.read(repaired_bytes_to_write)
                            fo.write(fileBytes)
                            repaired_file_bytes = repaired_file_bytes + repaired_bytes_to_write
                    else:
                        if (repairFile):
                            rewind_repair_file_to = repaired_file_bytes # Rewind repair file to here if sync is lost

        # NMEA messages
        elif (sbf_nmea_state == looking_for_asterix):
            nmea_length = nmea_length + 1 # Increase the message length count
            if (nmea_length > max_nmea_len): # If the length is greater than max_nmea_len, something bad must have happened (sync_lost)
                print("Panic!! Excessive NMEA message length!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
                continue
            # If this is one of the first five characters, store it
            if (nmea_length <= 5):
                if (nmea_length == 1):
                    nmea_char_1 = c
                    rewind_to = processed # If we lose sync due to dropped bytes then rewind to here
                elif (nmea_length == 2):
                    nmea_char_2 = c
                elif (nmea_length == 3):
                    nmea_char_3 = c
                elif (nmea_length == 4):
                    nmea_char_4 = c
                else: # nmea_length == 5
                    nmea_char_5 = c
                    message_type = chr(nmea_char_1) + chr(nmea_char_2) + chr(nmea_char_3) + chr(nmea_char_4) + chr(nmea_char_5) # Record the message type
                    if (message_type == "PSSN,"): # Remove the comma from PSSN
                        message_type = "PSSN"
            # Now check if this is an '*'
            if (c == 0x2A):
                # Asterix received
                # Don't exOR it into the checksum
                # Instead calculate what the expected checksum should be (nmea_csum in ASCII hex)
                nmea_expected_csum1 = ((nmea_csum & 0xf0) >> 4) + 0x30 # Convert MS nibble to ASCII hex
                if (nmea_expected_csum1 >= 0x3A): # : follows 9 so add 7 to convert to A-F
                    nmea_expected_csum1 += 7
                nmea_expected_csum2 = (nmea_csum & 0x0f) + 0x30 # Convert LS nibble to ASCII hex
                if (nmea_expected_csum2 >= 0x3A): # : follows 9 so add 7 to convert to A-F
                    nmea_expected_csum2 += 7
                # Next, look for the first csum character
                sbf_nmea_state = looking_for_csum1
                continue # Don't include the * in the checksum
            # Now update the checksum
            # The checksum is the exclusive-OR of all characters between the $ and the *
            nmea_csum = nmea_csum ^ c
        elif (sbf_nmea_state == looking_for_csum1):
            # Store the first NMEA checksum character
            nmea_csum1 = c
            sbf_nmea_state = looking_for_csum2
        elif (sbf_nmea_state == looking_for_csum2):
            # Store the second NMEA checksum character
            nmea_csum2 = c
            # Now check if the checksum is correct
            if ((nmea_csum1 != nmea_expected_csum1) or (nmea_csum2 != nmea_expected_csum2)):
                # The checksum does not match so sync_lost
                print("Panic!! NMEA checksum error!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
            else:
                # Checksum was valid so wait for the terminators
                sbf_nmea_state = looking_for_term1
        elif (sbf_nmea_state == looking_for_term1):
            # Check if this is CR
            if (c != 0x0D):
                print("Panic!! NMEA CR not found!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
            else:
                sbf_nmea_state = looking_for_term2
        elif (sbf_nmea_state == looking_for_term2):
            # Check if this is LF
            if (c != 0x0A):
                print("Panic!! NMEA LF not found!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
            else:
                # Valid NMEA message was received. Check if we have seen this message type before
                if message_type in messages:
                    messages[message_type] += 1 # if we have, increment its count
                else:
                    messages[message_type] = 1 # if we have not, set its count to 1
                if (nmea_length > longest_NMEA): # Update the longest NMEA message length
                    longest_NMEA = nmea_length
                # Print GNTXT
                # LF was received so go back to looking for B5 or a $
                sbf_nmea_state = looking_for_dollar_D3
                rewind_in_progress = False # Clear rewind_in_progress
                rewind_to = -1
                if (resync_in_progress == True): # Check if we are resyncing
                    resync_in_progress = False # Clear the flag now that a valid message has been received
                    resyncs += 1 # Increment the number of successful resyncs
                    print("Sync successfully re-established at byte "+str(processed)+". The NMEA message started at byte "+str(message_start_byte))
                    print()
                    if (repairFile):
                        fo.seek(rewind_repair_file_to) # Rewind the repaired file
                        repaired_file_bytes = rewind_repair_file_to
                        fi.seek(message_start_byte) # Copy the valid message into the repair file
                        repaired_bytes_to_write = processed - message_start_byte
                        fileBytes = fi.read(repaired_bytes_to_write)
                        fo.write(fileBytes)
                        repaired_file_bytes = repaired_file_bytes + repaired_bytes_to_write
                else:
                    if (repairFile):
                        rewind_repair_file_to = repaired_file_bytes # Rewind repair file to here if sync is lost
        
        # RTCM messages
        elif (sbf_nmea_state == looking_for_RTCM_len1):
            rtcm_length = (c & 0x03) << 8 # Extract length
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            rewind_to = processed # If we lose sync due to dropped bytes then rewind to here
            sbf_nmea_state = looking_for_RTCM_len2
        elif (sbf_nmea_state == looking_for_RTCM_len2):
            rtcm_length |= c # Extract length
            longest_rtcm_candidate = rtcm_length + 6 # Update the longest RTCM message length candidate. Include the header, length and checksum bytes
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            if (rtcm_length > 0):
                sbf_nmea_state = looking_for_RTCM_type1
            else:
                sbf_nmea_state = looking_for_RTCM_csum1
        elif (sbf_nmea_state == looking_for_RTCM_type1):
            rtcm_type = c << 4 # Extract type
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            rtcm_length = rtcm_length - 1 # Decrement length by one
            if (rtcm_length > 0):
                sbf_nmea_state = looking_for_RTCM_type2
            else:
                sbf_nmea_state = looking_for_RTCM_csum1
        elif (sbf_nmea_state == looking_for_RTCM_type2):
            rtcm_type |= c >> 4 # Extract type
            message_type = '%04i'%rtcm_type # Record the message type
            rtcm_subtype = (c & 0x0F) << 8 # Extract sub-type
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            rtcm_length = rtcm_length - 1 # Decrement length by one
            if (rtcm_length > 0):
                sbf_nmea_state = looking_for_RTCM_subtype
            else:
                sbf_nmea_state = looking_for_RTCM_csum1
        elif (sbf_nmea_state == looking_for_RTCM_subtype):
            rtcm_subtype |= c # Extract sub-type
            if (rtcm_type == 4072): # Record the sub-type but only for 4072 messages
                message_type = message_type + '_%i'%rtcm_subtype
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            rtcm_length = rtcm_length - 1 # Decrement length by one
            if (rtcm_length > 0):
                sbf_nmea_state = processing_RTCM_payload
            else:
                sbf_nmea_state = looking_for_RTCM_csum1
        elif (sbf_nmea_state == processing_RTCM_payload):
            rtcm_expected_csum = crc24q(c, rtcm_expected_csum) # Update expected checksum
            rtcm_length = rtcm_length - 1 # Decrement length by one
            if (rtcm_length == 0):
                sbf_nmea_state = looking_for_RTCM_csum1
        elif (sbf_nmea_state == looking_for_RTCM_csum1):
            rtcm_actual_csum = c << 8
            sbf_nmea_state = looking_for_RTCM_csum2
        elif (sbf_nmea_state == looking_for_RTCM_csum2):
            rtcm_actual_csum |= c
            rtcm_actual_csum <<= 8
            sbf_nmea_state = looking_for_RTCM_csum3
        elif (sbf_nmea_state == looking_for_RTCM_csum3):
            rtcm_actual_csum |= c
            sbf_nmea_state = looking_for_dollar_D3 # All bytes received so go back to looking for a new Sync Char 1 unless there is a checksum error
            if (rtcm_expected_csum != rtcm_actual_csum):
                print("Panic!! RTCM checksum error!")
                print("Sync lost at byte "+str(processed)+". Attemting to re-sync.")
                print()
                sync_lost_at = processed
                resync_in_progress = True
                sbf_nmea_state = sync_lost
            else:
                # Valid RTCM message was received. Check if we have seen this message type before
                if (longest_rtcm_candidate >= 8): # Message must contain at least 2 (+6) bytes to include a valid mesage type
                    if message_type in messages:
                        messages[message_type] += 1 # if we have, increment its count
                    else:
                        messages[message_type] = 1 # if we have not, set its count to 1
                    if (longest_rtcm_candidate > longest_rtcm): # Update the longest RTCM message length
                        longest_rtcm = longest_rtcm_candidate
                rewind_in_progress = False # Clear rewind_in_progress
                rewind_to = -1
                if (resync_in_progress == True): # Check if we are resyncing
                    resync_in_progress = False # Clear the flag now that a valid message has been received
                    resyncs += 1 # Increment the number of successful resyncs
                    print("Sync successfully re-established at byte "+str(processed)+". The RTCM message started at byte "+str(message_start_byte))
                    print()
                    if (repairFile):
                        fo.seek(rewind_repair_file_to) # Rewind the repaired file
                        repaired_file_bytes = rewind_repair_file_to
                        fi.seek(message_start_byte) # Copy the valid message into the repair file
                        repaired_bytes_to_write = processed - message_start_byte
                        fileBytes = fi.read(repaired_bytes_to_write)
                        fo.write(fileBytes)
                        repaired_file_bytes = repaired_file_bytes + repaired_bytes_to_write
                else:
                    if (repairFile):
                        rewind_repair_file_to = repaired_file_bytes # Rewind repair file to here if sync is lost


        # Check if the end of the file has been reached
        if (processed >= filesize - 1): keepGoing = False

        # Check if we should attempt to rewind
        # Don't rewind if we have not yet seen a valid message
        # Don't rewind if a rewind is already in progress
        if (sbf_nmea_state == sync_lost) and (len(messages) > 0) and (rewind_in_progress == False) and (rewind_to >= 0):
            rewind_attempts += 1 # Increment the number of rewind attempts
            if (rewind_attempts > max_rewinds): # Only rewind up to max_rewind times
                print("Panic! Maximum rewind attempts reached! Aborting...")
                keepGoing = False
            else:
                print("Sync has been lost. Currently processing byte "+str(processed)+". Rewinding to byte "+str(rewind_to))
                print()
                fi.seek(rewind_to) # Rewind the file
                processed = rewind_to - 1 # Rewind processed too! (-1 is needed as processed is incremented at the start of the loop)
                rewind_in_progress = True # Flag that a rewind is in progress
            

finally:
    fi.close() # Close the file

    if (repairFile):
        fo.close()
        
    # Print the file statistics
    print()
    processed += 1
    print('Processed',processed,'bytes')
    print('File size was',filesize)
    if (processed != filesize):
        print('FILE SIZE MISMATCH!!')
    print('Longest valid SBF message was %i bytes'%longest_SBF)
    if (containsNMEA == True):
        print('Longest valid NMEA message was %i characters'%longest_NMEA)
    if (containsRTCM == True):
        print('Longest valid RTCM message was %i bytes'%longest_rtcm)
    if len(messages) > 0:
        print('Message types and totals were:')
        for key in messages.keys():
            spaces = ' ' * (9 - len(key))
            print('Message type:',key,spaces,'Total:',messages[key])
    if (resyncs > 0):
        print('Number of successful resyncs:',resyncs)
    print()
    if (repairFile):
        print('Repaired data written to:', repairFilename)
    print()
    print('Bye!')
