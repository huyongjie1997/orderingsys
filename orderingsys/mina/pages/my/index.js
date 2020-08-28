//获取应用实例
var app = getApp();
Page({
  data: { 
    userInfo: null
  },
    onLoad() {

    },
    onShow: function () {
    //本地storage中获取值
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },
  /**
  * 用户注销
  */
  onClickLogout: function () {
    app.delUserInfo();
    this.setData({
      userInfo: null
    })
  },
  ToOrder() {
    //跳转页面order_list
    //API：wx
    wx.navigateTo({
      url:"/pages/my/order_list",
    })
  },
  ToAddress() {
    //跳转页面card
    //API：wx
    wx.navigateTo({
      url: "/pages/my/addressList",
    })
  },
  ToComment() {
    //跳转页面card
    //API：wx
    wx.navigateTo({
      url: "/pages/my/commentList",
    })
  },
});