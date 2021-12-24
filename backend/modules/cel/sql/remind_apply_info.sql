SELECT au.uid, au.username, au.phone, uc.name, uc.count
FROM `auth_user` au
JOIN (
    SELECT ru.repo_id, rr.name, COUNT(ru.u_type) 'count'
    FROM `repo_user` ru
    JOIN `repo_repo` rr ON ru.repo_id = rr.id
    WHERE ru.u_type = '{}'
    GROUP BY ru.repo_id
) uc
JOIN `repo_user` ru
WHERE au.phone
AND ru.repo_id = uc.repo_id
AND ru.uid = au.uid
AND ru.u_type IN ('{}', '{}')