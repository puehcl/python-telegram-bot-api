
MULTIPLE_UPDATES_LAST_ID = 483858683
MULTIPLE_UPDATES_SENDER_ID = 4858386
MULTIPLE_UPDATES_SENDER_USERNAME = "johndoe"
MULTIPLE_UPDATES_CHAT_ID = 4858386
MULTIPLE_UPDATES_TEXTS = ["first foobar", "second to last foobar", "last foobar"]

MULTIPLE_UPDATES = "{   \"ok\":true, \
                        \"result\":[ { \
                            \"update_id\":" + str(MULTIPLE_UPDATES_LAST_ID) + ", \
                                \"message\": { \
                                    \"message_id\":34, \
                                    \"from\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_SENDER_ID) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"chat\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_CHAT_ID) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"date\":1435233444, \
                                    \"text\":\"" + MULTIPLE_UPDATES_TEXTS[2] + "\" \
                                    }}, { \
                            \"update_id\":" + str(MULTIPLE_UPDATES_LAST_ID-1) + ", \
                                \"message\": { \
                                    \"message_id\":33, \
                                    \"from\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_SENDER_ID) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"chat\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_CHAT_ID-1) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"date\":1435233444, \
                                    \"text\":\"" + MULTIPLE_UPDATES_TEXTS[1] + "\" \
                                    }}, { \
                            \"update_id\":" + str(MULTIPLE_UPDATES_LAST_ID-2) + ", \
                                \"message\": { \
                                    \"message_id\":32, \
                                    \"from\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_SENDER_ID) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"chat\": { \
                                        \"id\":" + str(MULTIPLE_UPDATES_CHAT_ID-2) + ", \
                                        \"first_name\":\"john\", \
                                        \"username\":\"" + MULTIPLE_UPDATES_SENDER_USERNAME + "\" }, \
                                    \"date\":1435233444, \
                                    \"text\":\"" + MULTIPLE_UPDATES_TEXTS[0] + "\" }}]}".replace(" ", "")


MESSAGE_RESPONSE = "{   \"ok\":true, \
                        \"result\": { \
                            \"message_id\":344, \
                            \"from\": { \
                                \"id\":483848483, \
                                \"first_name\":\"TestBot\", \
                                \"username\":\"test_bot\"}, \
                            \"chat\": { \
                                \"id\":4838586, \
                                \"first_name\": \"tester\", \
                                \"username\":\"tester\"}, \
                            \"date\":1234567890, \
                            \"text\":\"testtext\"}}"

USER_RESPONSE = "{  \"id\": 22342342, \
                    \"first_name\": \"TestBot\", \
                    \"user_name\": \"test_bot\" }"


JSON_DICT  ={   "intattr": 5, \
                "strattr": "teststr", \
                "listattr": [ \
                    {"listitem1": 1}, \
                    {"listitem2": "foo"} \
                ], \
                "subobj": { \
                    "subobj_intattr": 4, \
                    "subobj_strattr": "substr", \
                    "subobj_listattr": [ \
                        {"sublistitem1": "subliststr"}\
                    ]}}
