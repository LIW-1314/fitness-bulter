const { BASE_URL } = require('./config')

function request({ url, method = 'GET', data = {} }) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      success: (res) => {
        resolve(res)
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

module.exports = {
  request
}