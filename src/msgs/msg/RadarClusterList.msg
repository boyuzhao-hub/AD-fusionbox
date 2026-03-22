# ContiRadarClusterList.msg
# Pack all Clusters from one CAN Frame

std_msgs/Header header             # timestamp + frame id
int32 no_of_clusters               # Number of clusters in this CAN Frame
ContiRadarCluster[] clusters       # Array contains all the cluster information