const { request } = require('../../utils/request')

Page({
  data: {
    result: "还没有请求"
  },

  testPing() {
    request({
      url: '/ping',
      method: 'GET'
    })
      .then((res) => {
        this.setData({
          result: JSON.stringify(res.data)
        })
      })
      .catch((err) => {
        this.setData({
          result: '请求失败：' + JSON.stringify(err)
        })
      })
  },

  goBodyFat() {
    wx.navigateTo({
      url: '/pages/bodyfat/bodyfat'
    })
  },

  goDiet() {
    wx.navigateTo({
      url: '/pages/diet/diet'
    })
  },

  goTraining() {
    wx.navigateTo({
      url: '/pages/training/training'
    })
  },

  goAdvice() {
    wx.navigateTo({
      url: '/pages/advice/advice'
    })
  },

  goChat() {
  wx.navigateTo({
    url: '/pages/chat/chat'
  })
}
})