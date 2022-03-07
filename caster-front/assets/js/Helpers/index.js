/* eslint-disable */

export default class Helpers {
  constructor(scope) {
    this.params = {}
  }

  hrtimestamp(d) {
    let hour = new Intl.DateTimeFormat('en', {
      hour: '2-digit',
      // hour12: false,
      hourCycle: 'h23',
      // hourCycle: '24',
    }).format(d)
    let minute = new Intl.DateTimeFormat('en', {
      minute: '2-digit',
    }).format(d)
    let second = new Intl.DateTimeFormat('en', {
      second: '2-digit',
    }).format(d)

    // 2 digits somehow not working
    hour = hour.length < 2 ? '0' + hour : hour
    minute = minute.length < 2 ? '0' + minute : minute
    second = second.length < 2 ? '0' + second : second

    const timestring = `${hour}:${minute}:${second}`
    return timestring
  }
}
