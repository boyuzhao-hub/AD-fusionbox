# ContiRadarObject.msg
# SRR308-21 Single Object Properity Definition

int32 id                  # Object ID (0~255)
float32 dist_long         # Longitude Distance (m)
float32 dist_lat          # Lateral Distance (m)
float32 vrel_long         # Longitude Relative Velocity (m/s)
float32 vrel_lat          # Lateral Relative Velocity (m/s)
float32 arel_long         # Longitude Relative Acceleration (m/s^2)
float32 arel_lat          # Lateral Realtive Acceleration (m/s^2)
float32 length            # Length of the Object (m)
float32 width             # Wideth of the Object (m)
int8 dyn_prop             # Dynamics Properity (0: moving, 1: stationary, 2: oncoming...)
int8 meas_state           # Measusre State (0: deleted, 1: new, 2: measured, 3: predicted...)
int8 prob_of_exist        # Probablity of exist (0~100%)