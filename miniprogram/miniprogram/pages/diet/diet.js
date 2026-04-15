const { request } = require('../../utils/request')
Page({
  data: {
    genderOptions: ['male', 'female'],
    genderIndex: 0,

    goalOptions: ['fat_loss', 'maintain', 'muscle_gain'],
    goalTextOptions: ['减脂', '维持', '增肌'],
    goalIndex: 0,

    activityOptions: ['low', 'medium', 'high'],
    activityTextOptions: ['低活动', '中等活动', '高活动'],
    activityIndex: 1,

    age: '',
    height_cm: '',
    weight_kg: '',

    result: null
  },

  onGenderChange(e) {
    this.setData({
      genderIndex: Number(e.detail.value)
    })
  },

  onGoalChange(e) {
    this.setData({
      goalIndex: Number(e.detail.value)
    })
  },

  onActivityChange(e) {
    this.setData({
      activityIndex: Number(e.detail.value)
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

  getDietPlan() {
    const {
      genderOptions,
      genderIndex,
      goalOptions,
      goalIndex,
      activityOptions,
      activityIndex,
      age,
      height_cm,
      weight_kg
    } = this.data

    if (!age || !height_cm || !weight_kg) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }

  request({
    url: '/diet/recommend',
    method: 'POST',
    data: {
      gender: genderOptions[genderIndex],
      age: Number(age),
      height_cm: Number(height_cm),
      weight_kg: Number(weight_kg),
      goal: goalOptions[goalIndex],
      activity_level: activityOptions[activityIndex]
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