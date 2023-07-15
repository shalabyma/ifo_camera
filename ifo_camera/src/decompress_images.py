import sys
# if sys.version_info.major == 3 and sys.version_info.minor >= 10:
#     import collections
#     setattr(collections, "MutableMapping", collections.abc.MutableMapping)
import rospy
import rosbag
from cv_bridge import CvBridge

def uncompress_bag(input_bag, output_bag):
    bridge = CvBridge()
    with rosbag.Bag(output_bag, 'w') as bag_out:
        for topic, msg, t in rosbag.Bag(input_bag).read_messages():
            if rospy.is_shutdown():
                break
            if msg._type == 'sensor_msgs/CompressedImage':
                try:
                    cv_image = bridge.compressed_imgmsg_to_cv2(msg)
                    image_msg = bridge.cv2_to_imgmsg(cv_image)
                    image_msg.header = msg.header
                    bag_out.write(topic.split("/compressed")[0], image_msg, t)
                except Exception as e:
                    rospy.logwarn('Error uncompressing color image: {}'.format(e))
            else:
                bag_out.write(topic.split("/compressed")[0], msg, t)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Not enough arguments. Usage: python image_uncompress.py input_bag output_bag")
        sys.exit(1)
    
    input_bag = sys.argv[1]
    output_bag = sys.argv[2]

    rospy.init_node('image_uncompress_node')
    uncompress_bag(input_bag, output_bag)