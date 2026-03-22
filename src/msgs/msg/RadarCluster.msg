# ContiRadarCluster.msg
# SRR308-21 Single Cluster Property Definition

int32 id                  # Cluster ID (0~255)
float32 dist_long         # Longitude Distance (m)
float32 dist_lat          # Lateral Distance (m)
float32 vrel_long         # Longitude Relative Velocity (m/s)
float32 vrel_lat          # Lateral Relative Velocity (m/s)
float32 rcs               # Radar Cross Section (dBm^2)