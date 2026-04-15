const { request } = require('../../utils/request')
Page({
  data: {
    goalOptions: ['fat_loss', 'maintain', 'muscle_gain'],
    goalTextOptions: ['减脂', '保持', '增肌'],
    goalIndex: 0,

    experienceOptions: ['beginner', 'intermediate'],
    experienceTextOptions: ['新手', '进阶'],
    experienceIndex: 0,

    daysOptions: [3, 4, 5, 6],
    daysTextOptions: ['3天', '4天', '5天', '6天'],
    daysIndex: 0,

    result: null
  },

  onGoalChange(e) {
    this.setData({
      goalIndex: Number(e.detail.value)
    })
  },

  onExperienceChange(e) {
    this.setData({
      experienceIndex: Number(e.detail.value)
    })
  },

  onDaysChange(e) {
    this.setData({
      daysIndex: Number(e.detail.value)
    })
  },

  getTrainingPlan() {
    const {
      goalOptions,
      goalIndex,
      experienceOptions,
      experienceIndex,
      daysOptions,
      daysIndex
    } = this.data

  request({
  url: '/training/plan',
  method: 'POST',
  data: {
    goal: goalOptions[goalIndex],
    experience: experienceOptions[experienceIndex],
    days_per_week: daysOptions[daysIndex]
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