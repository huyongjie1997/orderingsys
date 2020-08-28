//获取应用实例
var app = getApp();
var api = require("../../config/api.js")
Page({
  data: {
    "content": "",
    "score": 10,
    "order_sn": ""
  },
  onLoad: function(e) {
    this.setData({
      "order_sn": e.order_sn
    });
  },
  scoreChange: function(e) {
    console.log(e.detail.value)
    this.setData({
      "score": e.detail.value
    });
  },
  bindCommentInput: function(e) {
    console.log(e.detail.value)
    this.setData({
      "content": e.detail.value
    });
  },
  doComment: function() {
    var that = this;
    wx.request({
      url: api.FoodCommentAPI,
      data: {
        order_sn: that.data.order_sn,
        comment: that.data.content,
        score: that.data.score
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        if (res.status == false) {
          app.alert({
            "content": res.data.msg
          });
          return;
        }else{
          app.alert({
            "content": res.data.msg
          });
          return;
        }
       /* that.setData({
          user_info: res.data.info
        });*/
      },
    })
  }
});