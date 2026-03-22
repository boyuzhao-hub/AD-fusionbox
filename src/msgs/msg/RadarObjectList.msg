# ContiRadarObjectList.msg
# Pack all the object in one CAN Frame

std_msgs/Header header             # Timestamp + Frame
int32 no_of_objects                # Number of Objects in the current CAN Frame
ContiRadarObject[] objects         # Arry contains all the objects information