// 计算 距离指定时间差值
export const calculateTime = function (siteStartup,format = ['天','小时','分钟','秒']) {
     //当前日期
     let nowDate = new Date()
     //开始时间日期格式化后
     let startDateTime = new Date(siteStartup.replace(/-/g, '/'))
     //两时间戳差值
     let diff = (nowDate - startDateTime)

     let days = Math.floor(diff / (24 * 3600 * 1000)) < 10 ? '0' +  Math.floor(diff / (24 * 3600 * 1000)) : Math.floor(diff / (24 * 3600 * 1000)) // 计算出天数
     let leavel1 = diff % (24 * 3600 * 1000)// 计算天数后剩余的时间
     let hours = Math.floor(leavel1 / (3600 * 1000)) < 10 ? '0' + Math.floor(leavel1 / (3600 * 1000)):Math.floor(leavel1 / (3600 * 1000)) // 计算天数后剩余的小时数
     let leavel2 = diff % (3600 * 1000) // 计算剩余小时后剩余的毫秒数
     let minutes = Math.floor(leavel2 / (60 * 1000)) < 10 ? '0' + Math.floor(leavel2 / (60 * 1000)) : Math.floor(leavel2 / (60 * 1000)) // 计算剩余的分钟数
     let leavel3 = diff %(60 * 1000) // 计算剩余的秒数
     let second = Math.floor(leavel3 / 1000) < 10 ? '0' + Math.floor(leavel3 / 1000) : Math.floor(leavel3 / 1000) //计算秒数
     return `${days} ${format[0]} ${hours} ${format[1]} ${minutes} ${format[2]} ${second} ${format[3]}`
}