UPDATE
    `auth_user` au,
    (
        SELECT au.uid, au.active_index, LOG(IFNULL(dc.comment_count, 0) + 1) + LOG(IFNULL(dd.doc_count, 0) + 1) * 10 new_index
        FROM `auth_user` au
        LEFT JOIN (
            SELECT au.uid, COUNT(d.id) doc_count
            FROM `auth_user` au
            LEFT JOIN `doc_doc` d ON d.creator = au.uid
            WHERE d.update_at > ADDDATE(CURDATE(), -30)
            AND NOT d.is_deleted
            GROUP BY au.uid
        ) dd ON dd.uid = au.uid
        LEFT JOIN (
            SELECT au.uid, COUNT(dc.id) comment_count
            FROM `auth_user` au
            LEFT JOIN `doc_comment` dc ON dc.creator = au.uid
            WHERE dc.update_at > ADDDATE(CURDATE(), -30)
            AND not dc.is_deleted
            GROUP BY au.uid
        ) dc ON dc.uid = au.uid
    ) s
SET au.active_index = IF(s.new_index >= s.active_index, s.new_index, IF(s.active_index > 1, s.active_index - 1, 0))
WHERE s.uid = au.uid;
