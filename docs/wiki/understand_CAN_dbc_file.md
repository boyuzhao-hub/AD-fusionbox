# How the CAN Frame is organized？How to understand a dbc file?

## How the CAN frame is organized?
There are multiple variants of CAN exist currently, please refer the difference in the table below.

| Property | Fault-tolerant CAN<br>(low-speed CAN) | Classical CAN 2.0<br>(high-speed CAN) | CAN FD<br>(Flexible Data-rate) | CAN XL |
| :--- | :--- | :--- | :--- | :--- |
| **Max baud rate speed** | 0.125 Mbit/s | 1 Mbit/s | 8 Mbit/s (data phase) | 20 Mbit/s |
| **Max data payload size** | 8 bytes | 8 bytes | 64 bytes | 2048 bytes |
| **Baud rate type** | Fixed | Fixed | Variable (faster data field) | Variable (higher rates) |
| **Use cases** | Fault-tolerant, body control modules | Real-time automotive applications | High data throughput, ADAS, EV applications | Future high-data applications |
| **Key features** | Fault-tolerant operation, continue even if one bus line is damaged | Low cost, robust error detection, most commonly deployed | Increased payload, speed and reliability | Increased payload, speed and reliability |

Here, we talk about some details regarding classic CAN 2.0 with 11 bits idertifier. 
<div align="center">
  <img src="/docs/assets/CAN_Standard_Frame.svg" alt="Standard CAN Frame" width="90%">
  <p><i>Image Source: <a href="https://www.csselectronics.com/pages/can-bus-simple-intro-tutorial">CAN Bus Explained - A Simple Intro [2025] </a></i></p>
</div>

| Field | Full Name | Bits | Description |
| :--- | :--- | :--- | :--- |
| **SOF** | Start of Frame | 1 | The Start of Frame is a 'dominant 0' to tell the other nodes that a CAN node intends to talk. |
| **ID** | Standard Identifier | 11 | The ID is the frame identifier - lower values have higher priority. |
| **RTR** | Remote Transmission Request | 1 | The Remote Transmission Request indicates whether a node sends data or requests dedicated data from another node. |
| **Control** | Control Field | 6 | The Control contains the Identifier Extension Bit (IDE) which is a 'dominant 0' for 11-bit. It also contains the 4-bit Data Length Code (DLC) that specifies the length of the data bytes to be transmitted (0 to 8 bytes). |
| **Data** | Data Field | 0-64 | The Data contains the data bytes aka payload, which includes CAN signals that can be decoded for information. |
| **CRC** | Cyclic Redundancy Check | 16 | The Cyclic Redundancy Check is used to ensure data integrity. |
| **ACK** | Acknowledgement | 2 | The ACK slot indicates if the node has acknowledged and received the data correctly. |
| **EOF** | End of Frame | 7 | The EOF marks the end of the CAN frame. |

Raw CAN bus data is not human-readable. A DBC file, in this case, provided by OEM is designed for the engineers to decode raw CAN bus data into physical values.

## How to understand a dbc file?
The following fields are normally used in DBC file. For Python programming, [```cantools```](https://cantools.readthedocs.io/en/latest/) is a package to parse the CAN BUS data. 
- **NS_** (New Symbol) Claim the keywords that will be used in the dbc file.
- **BS_** (Bus Speed) Define the Baud Rate of the CAN Bus. Normally it is configured in through hardware or ROS2 Driver.
- **BU_** (Bus Unit) Define the ECU or hardware name that connected to the CAN Bus.
- **BO_** (Message) Define the message of one CAN Bus frame, include **message id**, **message name**, **data length (bytes)**, and **transmitter**. 
  - Syntax: ```B0_ [MessageID] [Message Name]: [DLC] [Transmitter]```
  - For example: ```BO_ 1579 Obj_1_General_2: 8 SRR308```
    - ```1579``` is CAN ID in decimal.
    - ```Obj_1_General_2``` is the name of the message.
    - ```8``` this frmae of CAN message include 8 bytes。
    - ```SRR308``` this message is sent by radar SRR308.
- **SG_** (Signal) Define what physical value does one range of bits in this message represent, include **signal name**, **start bit|length@byte order+value type**, **(factor, offset)**,**minimum|maximum**,**unit**, **receiver**.
  - Syntax ```SG_ [SignalName] : [StartBit]|[Length]@[ByteOrder][ValueType] ([Factor],[Offset]) [[Min]|[Max]] "[Unit]" [Receiver]```
  - For example: ```SG_ Obj_VrelLat : 45|9@0+ (0.25,-64) [-64|63.75] "m/s"  ExternalUnit```
    - ```Obj_VrelLat``` Name of the signal. Object relative lateral velocity.
    - ```45|9``` Start from no. 45 bit, occupied 9 bits.
    - ```@0``` represents Motorola format.
    - ```+``` stands for Unsigned.
    - ```(0.25,-64)``` Physical Value = Raw Value $\times$ 0.25 + (-64).
    - ```[-64|63.75]``` the valid range of this physical value.
    - ```m/s``` unit.
    - ```ExternalUnit``` Reveiver of this signal is an external unit.
- **CM_** (Comment) the comment of message, signal for human reading.
- **VAL_** (Value Table) map the numbers into a string with actual meanings.
  - Syntax ```VAL_ [MessageId] [SignalName] [Value1] "[String1]" [Value2] "[String2]" ... ;```
  - For example ```VAL_ 1661 Obj_Class 7 "Description for the value '0x7'" 6 "Wide" 5 "Bicycle" 4 "Motorcycle" 3 "Pedestrian" 2 "Truck" 1 "Car" 0 "Point" ;```
    - If ```Obj_Class``` is ```1```, then the object is a Car. 
  
- **EV_** (Environment Variable) Vitural Variable that only for simulation.
- **VAL_TABLE_** (Value Table) A table that for global lookup.
  - Syntax ```VAL_TABLE_ [TableName] [Value1] "[String1]" [Value2] "[String2]" ...;```

<br/>
<small>
A good reference: <a href="https://www.csselectronics.com/pages/can-dbc-file-database-intro">CAN DBC File Introduction</a>
</small>