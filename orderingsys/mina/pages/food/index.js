//index.js
//获取应用实例
var app = getApp();
var api = require("../../config/api.js")

Page({
  data: {
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    loadingHidden: false, // loading
    swiperCurrent: 0,
    categories: [],
    activeCategoryId: 0,
    goods: [],
    scrollTop: "0",
    loadingMoreHidden: true,
    searchInput: '',
    categoryId: '',
    processing: false
  },
  tapCategories: function(e) {
    var categoryId = e.currentTarget.dataset.id
    console.log(e)
    this.setData({
      categoryId: categoryId
    })
    console.log(this.data.categoryId)
    wx.request({
      //url: api.CategoryAPI + this.data.categoryId + '/',
      url:api.FoodAPI,
      data: {
        pk: this.data.categoryId
      },
      method: 'GET',
      dataType: 'json',
      success: (res) => {
        var that = this;
        console.log(res.data)
        if (this.data.categoryId==0){
          that.setData({
            //categories: res.data.category,
            activeCategoryId: this.data.categoryId,
            goods: res.data,
            loadingMoreHidden: true,
            p: 1,
          })
        }
        else{
          that.setData({
            //categories: res.data.category,
            activeCategoryId: this.data.categoryId,
            goods: res.data[0].food,
            loadingMoreHidden: true,
            p: 1,
          })
        }
        
      },
    })
  },
  onLoad: function() {
    var that = this;
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    });
    wx.request({
      url: api.IndexAPI,
      data: '',
      method: 'GET',
      dataType: 'json',
      success: (res) => {
        var that = this;
        console.log(res.data)
        that.setData({
          //categories: res.data,
          goods: res.data[0].food,
          banners: res.data[0].image_list
        })
        this.getFoodcategories();
      },
    })
    
  },
  getFoodcategories: function () {
    var that = this
      wx.request({
        url: api.CategoryAPI,
        method: 'GET',
        dataType: 'json',
        responseType: 'text',
        success: function(res) {
          that.setData({
            categories: res.data
          })
        },
        
      })
   },
  scroll: function(e) {
    var that = this,
      scrollTop = that.data.scrollTop;
    that.setData({
      scrollTop: e.detail.scrollTop
    });
  },
  //事件处理函数
  swiperchange: function(e) {
    this.setData({
      swiperCurrent: e.detail.current
    })
  },
  listenerSearchInput: function(e) {
    this.setData({
      searchInput: e.detail.value
    });
  },
  toSearch: function(e) {
    this.setData({
      p: 1,
      goods: [],
      loadingMoreHidden: true
    });
    this.getFoodList();
  },
  tapBanner: function(e) {
    if (e.currentTarget.dataset.id != 0) {
      wx.navigateTo({
        url: "/pages/food/info?id=" + e.currentTarget.dataset.id
      });
    }
  },
  toDetailsTap: function(e) {
    wx.navigateTo({
      url: "/pages/food/info?id=" + e.currentTarget.dataset.id
    });
  },
  getFoodList: function() {
    var that = this;
    if (that.data.processing) {
      return;
    }

    if (!that.data.loadingMoreHidden) {
      return;
    }

    that.setData({
      processing: true
    });

    wx.request({
      url: api.SearchAPI,
      data: {
        //cat_id: that.data.activeCategoryId,
        mix_kw: that.data.searchInput,
        //p: that.data.p,
      },
      method: 'GET',
      dataType: 'json',
      success: function(res) {
        if (res.data.statu == false) {
          app.alert({ "content": res.data.msg });
         
          that.setData({
            goods:[],
            processing: false
          });
        }
        else{
          that.setData({
            goods: res.data,
            //p: that.data.p + 1,
            processing: false
          });
        }
      }
    });
  }
});