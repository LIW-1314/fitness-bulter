const { request } = require('../../utils/request')
Page({
  data: {
    latitude: '',
    longitude: '',

    goalOptions: ['fat_loss', 'maintain', 'muscle_gain'],
    goalTextOptions: ['减脂', '保持', '增肌'],
    goalIndex: 0,

    trainingOptions: ['rest', 'cardio', 'strength'],
    trainingTextOptions: ['休息', '有氧', '力量'],
    trainingIndex: 1,

    result: null
  },

  onLoad() {
    this.getUserLocation()
  },

  onGoalChange(e) {
    this.setData({
      goalIndex: Number(e.detail.value)
    })
  },

  onTrainingChange(e) {
    this.setData({
      trainingIndex: Number(e.detail.value)
    })
  },

  getUserLocation(callback) {
    wx.getLocation({
      type: 'wgs84',
      success: (res) => {
        console.log('定位成功:', res)

        this.setData({
          latitude: res.latitude,
          longitude: res.longitude
        })

        wx.showToast({
          title: '定位成功',
          icon: 'success'
        })

        if (callback) callback()
      },
      fail: (err) => {
        console.error('定位失败:', err)

        wx.showModal({
          title: '定位失败',
          content: '当前无法获取定位，请先在开发者工具中设置模拟位置，或后续在真机上授权定位。',
          showCancel: false
        })
      }
    })
  },

  getTodayAdvice() {
    const {
      latitude,
      longitude,
      goalOptions,
      goalIndex,
      trainingOptions,
      trainingIndex
    } = this.data

    if (!latitude || !longitude) {
      wx.showToast({
        title: '暂无定位信息',
        icon: 'none'
      })
      return
    }

  request({
  url: '/advice/today',
  method: 'POST',
  data: {
    latitude: Number(latitude),
    longitude: Number(longitude),
    training_goal: goalOptions[goalIndex],
    planned_training: trainingOptions[trainingIndex]
  }
  })
  .then((res) => {
    this.setData({
      result: res.data
    })
  })
  .catch((err) => {
    wx.showToast({
      title: '请求失败',
      icon: 'none'
    })
    console.error(err)
  })

  },

  refreshAndGetAdvice() {
    this.getUserLocation(() => {
      this.getTodayAdvice()
    })
  }
})