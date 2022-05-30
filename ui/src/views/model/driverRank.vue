<template>
<div>
  <div class="top-row">
    <div class="add-button">
      <el-select v-model="driverID" placeholder="请选择司机账户" @change="getSelectedDriverInfo">
              <el-option
                v-for="item in driverList"
                :key="item.id"
                :label="item.username"
                :value="item.id">
              </el-option>
            </el-select>
    </div>
  </div>
  <div>
    <div class="main_content">
    <div class="main_title">司机信息</div>
    <div class="line">
      <div class="left_div">用户名：</div>
      <div class="right_div">{{selectedDriverInfo.username}}</div>
    </div>
    <div class="line">
      <div class="left_div">所属企业：</div>
      <div class="right_div">{{selectedDriverInfo.company_name}}</div>
    </div>
    <div class="line">
      <div class="left_div">姓名：</div>
      <div class="right_div">{{selectedDriverInfo.name}}</div>
    </div>
    <div class="line">
      <div class="left_div">年龄：</div>
      <div class="right_div">{{selectedDriverInfo.age}}</div>
    </div>
    <div class="line">
      <div class="left_div">被投诉次数：</div>
      <div class="right_div">{{selectedDriverInfo.complain_times}}次</div>
    </div>
    <div class="line">
      <div class="left_div">违章次数：</div>
      <div class="right_div">{{selectedDriverInfo.violation_times}}次</div>
    </div>
    <div class="line">
      <div class="left_div">好人好事：</div>
      <div class="right_div">{{selectedDriverInfo.good_times}}次</div>
    </div>
    <div class="line">
      <div class="left_div">最近五次收入情况：</div>
      <div class="right_div">
        <el-button @click="isShowLast5Income=true" type="success" :plain="true" size="mini">查看</el-button>
      </div>
    </div>
    <div class="line">
      <div class="left_div">最近五次评级情况：</div>
      <div class="right_div">
        <el-button @click="isShowLast5Rank=true" type="success" :plain="true" size="mini">查看</el-button>
      </div>
    </div>
    <div class="line">
      <div class="left_div">
        <el-button type="primary" @click="isShowEdit=true">评级</el-button>
      </div>
    </div>
  </div>
  </div>
</div>
</template>

<script>
import {
  Message
} from 'element-ui'
export default {
  data() {
    return {
      isShowLast5Income: false,
      isShowLast5Rank: false,
      driverID:"",
      driverList: [],
      selectedDriverInfo:{
        "username":"",
        "name":"",
        "age":"",
        "id_number":"",
        "company_name":"",
        "complain_times":0,
        "violation_times":0,
        "good_times":0,
        "last5_income":[],
        "last5_rank":[]
      }
    };
  },
  created(){
  },
  mounted: function() {
    this.getDriverInfo();
  },
  methods: {
    getDriverInfo(){
      let that = this;
      this.req({
        url: "get_all_driver_list",
        data: {
          
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.driverList = res.content.data;
          }},
          err => {
            Message({
                message: '获取司机信息失败',
                type: 'warning',
                duration: 3 * 1000
              })
            console.log("err :", err);
          }
      );
    },
    getSelectedDriverInfo(){
      let that = this;
      this.req({
        url: "get_selected_driver_info",
        data: {
          id:that.driverID      
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.selectedDriverInfo = res.content.data;
          }},
          err => {
            Message({
                message: '获取司机信息失败',
                type: 'warning',
                duration: 3 * 1000
              })
            console.log("err :", err);
          }
      );
    }
  }
};
</script>

<style lang="scss">
.top-row {
  width: 100%;
  height: 40px;
  margin-top:20px;
  margin-left:20px;
  .add-button{
    display: inline-block;
    margin-right: 10px;
  }
  .left_div{
    display: inline-block;
  }
  .right_div{
    display: inline-block;
  }
}
.main_content {
  width: 80%;
  height: 900px;
  min-width: 600px;
  padding:20px 20px 15px 20px;
  .main_title{
    font-size: 18px;
  }
  .line{
    margin-top: 20px;
    .left_div{
      display: inline-block;
    }
    .right_div{
      display: inline-block;
    }
  }
}
.appoinment_win{
  .line{
    margin-left:10px;
    margin-top:20px;
    .label{
      display: inline-block;
      width:100px;
    }
    .content{
      display: inline-block;
    }
  }
}
</style>