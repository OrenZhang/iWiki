UPDATE
    `auth_user` au,
    (
        SELECT
            au.uid,
            LOG(IFNULL(dc.comment_count, 0) + 1) + LOG(IFNULL(dd.doc_count, 0) + 1) * 10 + LOG(IFNULL(dgl.visit_count, 0) + 1) new_index
        FROM `auth_user` au
        LEFT JOIN (
            SELECT au.uid, COUNT(d.id) doc_count
            FROM `auth_user` au
            LEFT JOIN `doc_doc` d ON d.creator = au.uid
            WHERE d.update_at > ADDDATE(CURDATE(), -14)
            AND NOT d.is_deleted
            GROUP BY au.uid
        ) dd ON dd.uid = au.uid
        LEFT JOIN (
            SELECT au.uid, COUNT(dc.id) comment_count
            FROM `auth_user` au
            LEFT JOIN `doc_comment` dc ON dc.creator = au.uid
            WHERE dc.update_at > ADDDATE(CURDATE(), -14)
            AND not dc.is_deleted
            GROUP BY au.uid
        ) dc ON dc.uid = au.uid
        LEFT JOIN (
            SELECT ldv.visitor uid, COUNT(1) visit_count
            FROM `log_doc_visit` ldv
            WHERE ldv.visitor IS NOT NULL
            AND ldv.visit_at > ADDDATE(CURDATE(), -14)
            GROUP BY ldv.visit_at
        ) dgl ON dgl.uid = au.uid
    ) s
SET au.active_index = s.new_index
WHERE s.uid = au.uid;
