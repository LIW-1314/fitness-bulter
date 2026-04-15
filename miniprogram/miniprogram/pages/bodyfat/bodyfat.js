
const { request } = require('../../utils/request')
Page({
  data: {
    genderOptions: ['male', 'female'],
    genderIndex: 0,
    age: '',
    height_cm: '',
    weight_kg: '',
    result: null
  },
  
  onLoad() {
  const userInfo = wx.getStorageSync('userInfo')

  if (userInfo) {
      this.setData({
      genderIndex: userInfo.genderIndex || 0,
      age: userInfo.age || '',
      height_cm: userInfo.height_cm || '',
      weight_kg: userInfo.weight_kg || ''
      })
    }
  },

  onGenderChange(e) {
    this.setData({
      genderIndex: e.detail.value
    })
  },

  onAgeInput(e) {
    this.setData({
      age: e.detail.value
    })
  },

  onHeightInput(e) {
    this.setData({
      height_cm: e.detail.value
    })
  },

  onWeightInput(e) {
    this.setData({
      weight_kg: e.detail.value
    })
  },

  calculateBodyFat() {
    const { genderOptions, genderIndex, age, height_cm, weight_kg } = this.data

    if (!age || !height_cm || !weight_kg) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }
    // 保存用户信息
    wx.setStorageSync('userInfo', {
    genderIndex,
    age,
    height_cm,
    weight_kg
    })

    request({
      url: '/bodyfat/calculate',
      method: 'POST',
      data: {
        gender: genderOptions[genderIndex],
        age: Number(age),
        height_cm: Number(height_cm),
        weight_kg: Number(weight_kg)
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
  }
})