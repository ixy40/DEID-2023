# import re
# import sys
# phone_pattern ='(\d{3}[-\.\s/]??\d{3}[-\.\s/]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s/]??\d{4})'

# # compiling the reg_ex would save sime time!
# ph_reg = re.compile(phone_pattern)


# def check_for_phone(patient,note,chunk, output_handle):
#     """
#     Inputs:
#         - patient: Patient Number, will be printed in each occurance of personal information found
#         - note: Note Number, will be printed in each occurance of personal information found
#         - chunk: one whole record of a patient
#         - output_handle: an opened file handle. The results will be written to this file.
#             to avoid the time intensive operation of opening and closing the file multiple times
#             during the de-identification process, the file is opened beforehand and the handle is passed
#             to this function. 
#     Logic:
#         Search the entire chunk for phone number occurances. Find the location of these occurances 
#         relative to the start of the chunk, and output these to the output_handle file. 
#         If there are no occurances, only output Patient X Note Y (X and Y are passed in as inputs) in one line.
#         Use the precompiled regular expression to find phones.
#     """
#     # The perl code handles texts a bit differently, 
#     # we found that adding this offset to start and end positions would produce the same results
#     offset = 27

#     # For each new note, the first line should be Patient X Note Y and then all the personal information positions
#     output_handle.write('Patient {}\tNote {}\n'.format(patient,note))

#     # search the whole chunk, and find every position that matches the regular expression
#     # for each one write the results: "Start Start END"
#     # Also for debugging purposes display on the screen (and don't write to file) 
#     # the start, end and the actual personal information that we found
#     for match in ph_reg.finditer(chunk):
                
#             # debug print, 'end=" "' stops print() from adding a new line
#             print(patient, note,end=' ')
#             print((match.start()-offset),match.end()-offset, match.group())
                
#             # create the string that we want to write to file ('start start end')    
#             result = str(match.start()-offset) + ' ' + str(match.start()-offset) +' '+ str(match.end()-offset) 
            
#             # write the result to one line of output
#             output_handle.write(result+'\n')

            
            
# def deid_phone(text_path= 'id.text', output_path = 'phone.phi'):
#     """
#     Inputs: 
#         - text_path: path to the file containing patient records
#         - output_path: path to the output file.
    
#     Outputs:
#         for each patient note, the output file will start by a line declaring the note in the format of:
#             Patient X Note Y
#         then for each phone number found, it will have another line in the format of:
#             start start end
#         where the start is the start position of the detected phone number string, and end is the detected
#         end position of the string both relative to the start of the patient note.
#         If there is no phone number detected in the patient note, only the first line (Patient X Note Y) is printed
#         to the output
#     Screen Display:
#         For each phone number detected, the following information will be displayed on the screen for debugging purposes 
#         (these will not be written to the output file):
#             start end phone_number
#         where `start` is the start position of the detected phone number string, and `end` is the detected end position of the string
#         both relative to the start of patient note.
    
#     """
#     # start of each note has the patter: START_OF_RECORD=PATIENT||||NOTE||||
#     # where PATIENT is the patient number and NOTE is the note number.
#     start_of_record_pattern = '^start_of_record=(\d+)\|\|\|\|(\d+)\|\|\|\|$'

#     # end of each note has the patter: ||||END_OF_RECORD
#     end_of_record_pattern = '\|\|\|\|END_OF_RECORD$'

#     # open the output file just once to save time on the time intensive IO
#     with open(output_path,'w+') as output_file:
#         with open(text_path) as text:
#             # initilize an empty chunk. Go through the input file line by line
#             # whenever we see the start_of_record pattern, note patient and note numbers and start 
#             # adding everything to the 'chunk' until we see the end_of_record.
#             chunk = ''
#             for line in text:
#                 record_start = re.findall(start_of_record_pattern,line,flags=re.IGNORECASE)
#                 if len(record_start):
#                     patient, note = record_start[0]
#                 chunk += line

#                 # check to see if we have seen the end of one note
#                 record_end = re.findall(end_of_record_pattern, line,flags=re.IGNORECASE)

#                 if len(record_end):
#                     # Now we have a full patient note stored in `chunk`, along with patient numerb and note number
#                     # pass all to check_for_phone to find any phone numbers in note.
#                     check_for_phone(patient,note,chunk.strip(), output_file)
                    
#                     # initialize the chunk for the next note to be read
#                     chunk = ''
                
# if __name__== "__main__":
        
    
    
#     deid_phone(sys.argv[1], sys.argv[2])
    


import re
import sys

# Regular expression pattern to match capitalized words (names)
name_pattern = r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b'

# Compiling the regex pattern to save time
name_regex = re.compile(name_pattern)


def check_for_names(patient, note, chunk, output_handle):
    """
    Inputs:
        - patient: Patient Number, will be printed in each occurrence of personal information found
        - note: Note Number, will be printed in each occurrence of personal information found
        - chunk: one whole record of a patient
        - output_handle: an opened file handle. The results will be written to this file.
            to avoid the time-intensive operation of opening and closing the file multiple times
            during the de-identification process, the file is opened beforehand and the handle is passed
            to this function.
    Logic:
        Search the entire chunk for name occurrences. Find the location of these occurrences
        relative to the start of the chunk, and output these to the output_handle file.
        If there are no occurrences, only output Patient X Note Y (X and Y are passed in as inputs) in one line.
        Use the precompiled regular expression to find names.
    """
    # For each new note, the first line should be Patient X Note Y and then all the personal information positions
    output_handle.write('Patient {}\tNote {}\n'.format(patient, note))

    # Search the whole chunk, and find every position that matches the regular expression
    # For each one, write the results: "Start Start END"
    for match in name_regex.finditer(chunk):
        # Create the string that we want to write to file ('start start end')
        result = str(match.start()) + ' ' + str(match.start()) + ' ' + str(match.end())

        # Write the result to one line of output
        output_handle.write(result + '\n')


def deid_names(text_path='id.txt', output_path='names.phi'):
    """
    Inputs:
        - text_path: path to the file containing patient records (default: id.txt)
        - output_path: path to the output file (default: names.phi)

    Outputs:
        for each patient note, the output file will start by a line declaring the note in the format of:
            Patient X Note Y
        then for each name found, it will have another line in the format of:
            start start end
        where the start is the start position of the detected name string, and end is the detected
        end position of the string both relative to the start of the patient note.
        If there is no name detected in the patient note, only the first line (Patient X Note Y) is printed
        to the output
    Screen Display:
        For each name detected, the following information will be displayed on the screen for debugging purposes
        (these will not be written to the output file):
            start end name
        where `start` is the start position of the detected name string, and `end` is the detected end position of the string
        both relative to the start of patient note.

    """
    # start of each note has the pattern: START_OF_RECORD=PATIENT||||NOTE||||
    # where PATIENT is the patient number and NOTE is the note number.
    start_of_record_pattern = r'^START_OF_RECORD=(\d+)\|\|\|\|(\d+)\|\|\|\|$'

    # end of each note has the pattern: ||||END_OF_RECORD
    end_of_record_pattern = r'\|\|\|\|END_OF_RECORD$'

    # open the output file just once to save time on the time-intensive IO
    with open(output_path, 'w+') as output_file:
        with open(text_path) as text:
            # initialize an empty chunk. Go through the input file line by line
            # whenever we see the START_OF_RECORD pattern, note patient and note numbers and start
            # adding everything to the 'chunk' until we see the END_OF_RECORD.
            chunk = ''
            for line in text:
                record_start = re.findall(start_of_record_pattern, line)
                if len(record_start):
                    patient, note = record_start[0]
                chunk += line

                # check to see if we have seen the end of one note
                record_end = re.findall(end_of_record_pattern, line)

                if len(record_end):
                    # Now we have a full patient note stored in `chunk`, along with patient number and note number
                    # pass all to check_for_names to find any names in note.
                    check_for_names(patient, note, chunk.strip(), output_file)

                    # initialize the chunk for the next note to be read
                    chunk = ''


if __name__ == "__main__":
    # Run deid_names with provided or default paths
    text_path = sys.argv[1] if len(sys.argv) > 1 else 'id.txt'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'names.phi'

    deid_names(text_path, output_path)
