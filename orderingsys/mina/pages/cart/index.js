//index.js
var app = getApp();
var api = require("../../config/api.js")
Page({
  data: {},
  onLoad: function() {
    this.getCartList();
  }, 
  //每项前面的选中框 
  selectTap: function(e) {
    var index = e.currentTarget.dataset.index;
    var list = this.data.list;
    if (index !== "" && index != null) {
      list[parseInt(index)].active = !list[parseInt(index)].active;
      this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    }
  },
  //计算是否全选了
  allSelect: function() {
    var list = this.data.list;
    var allSelect = false;
    for (var i = 0; i < list.length; i++) {
      var curItem = list[i];
      if (curItem.active) {
        allSelect = true;
      } else {
        allSelect = false;
        break;
      }
    }
    return allSelect;
  },
  //计算是否都没有选
  noSelect: function() {
    var list = this.data.list;
    var noSelect = 0;
    for (var i = 0; i < list.length; i++) {
      var curItem = list[i];
      if (!curItem.active) {
        noSelect++;
      }
    }
    if (noSelect == list.length) {
      return true;
    } else {
      return false;
    }
  },
  //全选和全部选按钮
  bindAllSelect: function() {
    var currentAllSelect = this.data.allSelect;
    var list = this.data.list;
    for (var i = 0; i < list.length; i++) {
      list[i].active = !currentAllSelect;
    }
    this.setPageData(this.getSaveHide(), this.totalPrice(), !currentAllSelect, this.noSelect(), list);
  },
  //加数量
  jiaBtnTap: function(e) {
    var that = this;
    var index = e.currentTarget.dataset.index;
    var list = that.data.list;
    list[parseInt(index)].nums[index].nums++;
    that.setPageData(that.getSaveHide(), that.totalPrice(), that.allSelect(), that.noSelect(), list);
    this.setCart(list[parseInt(index)].id, list[parseInt(index)].nums[index].nums);
  },
  //减数量
  jianBtnTap: function(e) {
    var that = this;
    var index = e.currentTarget.dataset.index;
    var list = this.data.list;
    if (list[parseInt(index)].nums[index].nums > 1) {
      list[parseInt(index)].nums[index].nums--;
      this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
      this.setCart(list[parseInt(index)].id, list[parseInt(index)].nums[index].nums);
    }
  },
  //编辑默认全不选
  editTap: function() {
    var list = this.data.list;
    for (var i = 0; i < list.length; i++) {
      var curItem = list[i];
      curItem.active = false;
    }
    this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
  },
  //选中完成默认全选
  saveTap: function() {
    var list = this.data.list;
    for (var i = 0; i < list.length; i++) {
      var curItem = list[i];
      curItem.active = true;
    }
    this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
  },
  getSaveHide: function() {
    return this.data.saveHidden;
  },
  totalPrice: function() {
    var list = this.data.list;
    var totalPrice = 0.00;
    for (var i = 0; i < list.length; i++) {
      if (!list[i].active) {
        continue; 
      }
      totalPrice = totalPrice + parseFloat(list[i].price) * list[i].nums[i].nums;
    }
    return totalPrice;
  },
  setPageData: function(saveHidden, total, allSelect, noSelect, list) {
    this.setData({
      list: list,
      saveHidden: saveHidden,
      totalPrice: total,
      allSelect: allSelect,
      noSelect: noSelect,
    });
  },
  //去结算
  toPayOrder: function() {
    var data = {
      type: "cart",
      goods: [],
      totalPrice: this.data.totalPrice,
    };

    var list = this.data.list;
    for (var i = 0; i < list.length; i++) {
      if (!list[i].active) {
        continue;
      }  
      data['goods'].push({
        "id": list[i].id,
        "price": list[i].price,
        "nums": list[i].nums[i].nums,
        "yun_price": list[i].yun_price,
        "courier_type": list[i].courier_type
      });
    }
    wx.navigateTo({
      url: "/pages/order/index?data=" + JSON.stringify(data)
    });
  },
  //如果没有显示去光光按钮事件
  toIndexPage: function() {
    wx.switchTab({
      url: "/pages/food/index"
    });
  },
  //选中删除的数据
  deleteSelected: function() {
    var food = this.data.list;
    var food_id = [];
    var list = this.data.list;
    var goods = [];
    list = list.filter(function(item) {
      if (!item.active) {
        goods.push({
          "id": item.id
        })
      }else{
        food_id.push(
          item.id
        )
      }
      return !item.active;
    });
   
    this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    console.log(food_id)
    //发送请求到后台删除数据
    wx.request({
      url: api.TradeAPI,
      data: {
        food_id: food_id
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'DELETE',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        console.log(res.data)
      },
    })
  },
  getCartList: function() {
    var that = this
    wx.request({
      url: api.TradeAPI,
      data: '',
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'GET',
      dataType: 'json',
      success: (res) => {
        console.log(res.data)
        if (res.data.statu == false) { 
          return;
         }
        that.setData({
          list: res.data,
          saveHidden: true,
          totalPrice: "0.00",
          allSelect: true,
          noSelect: false,
        });
        this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), this.data.list);
      },
    })
  },
  setCart: function(id, nums) {
    var id = id;
    var nums = nums;
    //console.log(nums)
    var that = this;
    wx.request({
      url: api.TradeAPI,
      data: {
        food: id,
        nums: nums
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'POST',
      dataType: 'json',
      success: (res) => {
        console.log(res.data)
        this.onLoad()
      },
    })
  }
});