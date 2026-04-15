const { request } = require('../../utils/request')

Page({
  data: {
    input: '',
    messages: [],
    userInfo: null,
    toView: ''
  },

  onLoad() {
    const userInfo = wx.getStorageSync('userInfo')

    const welcomeMessage = {
      role: 'ai',
      content: '你好，我是你的 AI 健身教练。你可以问我训练、饮食、减脂、增肌、恢复等问题。'
    }

    this.setData({
      messages: [welcomeMessage],
    })
    

    if (userInfo) {
      this.setData({
        userInfo
      })
    }
    this.scrollToBottom()
  },

  scrollToBottom() {
    this.setData({
      toView: ''
    })

    setTimeout(() => {
      this.setData({
        toView: 'bottom-anchor'
      })
    }, 50)
  },

  onInput(e) {
    this.setData({
      input: e.detail.value
    })
  },


  quickAsk(e) {
    const question = e.currentTarget.dataset.question
    this.sendMessage(question)
  },

  sendMessage(arg) {
    let msg = ''

    // 1. 快捷提问传进来的是字符串
    if (typeof arg === 'string') {
      msg = arg.trim()
    } else {
      // 2. 按钮点击 / 回车发送传进来的是事件对象，走 input
      msg = (this.data.input || '').trim()
    }

    if (!msg) return

    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先去体脂页填写身体信息',
        icon: 'none'
      })
      return
    }

    const userMessage = { role: 'user', content: msg }
    const loadingMessage = { role: 'ai', content: 'AI 正在思考...' }

    const updatedMessages = [...this.data.messages, userMessage, loadingMessage]

    this.setData({
      messages: updatedMessages,
      input: ''
    })

    this.scrollToBottom()

    request({
      url: '/ai/chat',
      method: 'POST',
      data: {
        message: msg,
        history: this.data.messages,
        user_info: this.data.userInfo
      }
    })
      .then((res) => {
        const finalMessages = [...this.data.messages]
        finalMessages[finalMessages.length - 1] = {
          role: 'ai',
          content: res.data.reply,
          actions: res.data.actions || []
        }

        this.setData({
          messages: finalMessages
        })

        this.scrollToBottom()
      })
      .catch((err) => {
        console.error('聊天请求失败:', err)

        const finalMessages = [...this.data.messages]
        finalMessages[finalMessages.length - 1] = {
          role: 'ai',
          content: '抱歉，我刚刚开小差了，请再试一次。'
        }

        this.setData({
          messages: finalMessages
        })

        this.scrollToBottom()

        wx.showToast({
          title: '请求失败',
          icon: 'none'
        })
      })
  },
  handleAction(e) {
    const type = e.currentTarget.dataset.type

    if (type === 'go_training') {
      wx.navigateTo({ url: '/pages/training/training' })
    }

    if (type === 'go_diet') {
      wx.navigateTo({ url: '/pages/diet/diet' })
    }

    if (type === 'go_bodyfat') {
      wx.navigateTo({ url: '/pages/bodyfat/bodyfat' })
    }
  }
})