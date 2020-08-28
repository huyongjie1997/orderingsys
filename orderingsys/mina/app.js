//app.js
App({
  onLaunch: function() {
    var userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },
  globalData: {
    userInfo: null,
    version: "1.0",
    shopName: "微信小程序订餐系统",
  },
  initUserInfo: function(res, localInfo) {
    var info = {
      token: res.token,
      phone: res.phone,
      nickName: localInfo.nickName,
      avatarUrl: localInfo.avatarUrl
    }
    // 1.去公共的app.js中调用globalData，在里面赋值。(在全局变量赋值)
    this.globalData.userInfo = info; //{phone:xxx,token:xxxx}

    // 2.在本地“cookie”中赋值
    wx.setStorageSync("userInfo", info);

  },
  delUserInfo: function() {
    this.globalData.userInfo = null;
    wx.removeStorageSync("userInfo")
  },
  tip: function(params) {
    var that = this;
    var title = params.hasOwnProperty('title') ? params['title'] : '提示信息';
    var content = params.hasOwnProperty('content') ? params['content'] : '';
    wx.showModal({
      title: title,
      content: content,
      success: function(res) {

        if (res.confirm) { //点击确定
          if (params.hasOwnProperty('cb_confirm') && typeof(params.cb_confirm) == "function") {
            params.cb_confirm();
          }
        } else { //点击否
          if (params.hasOwnProperty('cb_cancel') && typeof(params.cb_cancel) == "function") {
            params.cb_cancel();
          }
        }
      }
    })
  },
  alert: function(params) {
    var title = params.hasOwnProperty('title') ? params['title'] : '提示信息';
    var content = params.hasOwnProperty('content') ? params['content'] : '';
    wx.showModal({
      title: title,
      content: content,
      showCancel: false,
      success: function(res) {
        if (res.confirm) { //用户点击确定
          if (params.hasOwnProperty('cb_confirm') && typeof(params.cb_confirm) == "function") {
            params.cb_confirm();
          }
        } else {
          if (params.hasOwnProperty('cb_cancel') && typeof(params.cb_cancel) == "function") {
            params.cb_cancel();
          }
        }
      }
    })
  },
  console: function(msg) {
    console.log(msg);
  },
  getRequestHeader: function() {
    return {
      'content-type': 'application/x-www-form-urlencoded'
    }
  }
});