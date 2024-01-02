import glob
import logging
import re

all_files = glob.glob("raw_data/*chat_history.sql")


"""
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for league_chat_history
-- ----------------------------
DROP TABLE IF EXISTS `league_chat_history`;
CREATE TABLE `league_chat_history`  (
  `obj_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lid` int(11) NOT NULL DEFAULT 0,
  `rid` bigint(20) NOT NULL,
  `server_id` int(11) NULL DEFAULT NULL,
  `send_time` bigint(20) NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `args` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`obj_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `league_chat_history` VALUES ('003bd95db6c4496ea2db8f3ffb5ea4bf', 430005, 17847410005, 5, 1683746393, 'dipti coming', '{\"LID\":430005,\"VipLevel\":7,\"Country\":\"IN\",\"Icon\":{\"Avatar\":44,\"CustomAvatar\":\"\",\"Frame\":1020001},\"isUserInput\":true,\"LeagueShortName\":\"HHH\",\"ServerId\":5,\"Name\":\"Shruti\",\"RID\":17847410005}');
"""
for file in all_files:
    with open(file, "r") as f:
        for line in f:
            if not re.search("INSERT INTO", line):
                continue
            # extract "content"
            matched_obj = re.match(
                r"INSERT INTO `.*` VALUES \('(.*?)', (.*?), (.*?), (.*?), (.*?), '(.*?)(?<!\\)'.*",
                line,
            )
            if not matched_obj:
                logging.error("line not matched: %s", line)
                continue
            content = matched_obj.group(6)

            if re.match(r"^\[\{", content):
                continue
            if content:
                print(content)
