import sys #lib for system parameters

#function for details about error message. It will take input error and error details and return us the same message in our custom formatting.
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() #.exc_info() is a fun that gives details about location, line, time of error
    file_name=exc_tb.tb_frame.f_code.co_filename # to get name of file where error occured.
    error_message = "Error occured in python script name [{0}] line number[{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)) #{0},{1},{2} are the placeholders for variables file_name,exc_tb.tb_lineno, error

    return error_message


# creating custom class to call the above function when the error raises
class CustomException(Exception): #inheriting Exception class
    def __init__(self, error_message, error_detail:sys): #initiating the constructor
        super().__init__(error_message) #inheriting the __init__() function from exception
        self.error_message=error_message_detail(error_message, error_detail=error_detail)

    # inheriting one more function. 
    # Whenever we print this we will get below info from __str__() fun
    def __str__(self):
        return self.error_message
