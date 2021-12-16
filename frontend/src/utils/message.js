import { ElMessage } from 'element-plus'

export default function message (msg, type = 'success', duration = 6000) {
    ElMessage({
        message: msg,
        type: type,
        duration: duration,
        'show-close': true
    })
}
