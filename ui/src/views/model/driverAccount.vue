<template>
<div>
  <div class="top-row">
    <!-- <div class="add-button">
      <el-button type="primary" @click="isShowAdd=true">新增司机</el-button>
    </div> -->
  </div>
  <div>
    <el-table :data="driverList" style="width: 100%">
      <el-table-column prop="name" label="姓名" width=80></el-table-column>
      <el-table-column prop="id_number" label="身份证"></el-table-column>
      <el-table-column prop="car_number" label="车牌号" width=120></el-table-column>  
      <el-table-column prop="username" label="账户名" ></el-table-column>
      <el-table-column prop="company_name" label="所属企业" ></el-table-column>
      <el-table-column prop="phone" label="电话" width=140></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="address" label="地址" ></el-table-column>
      <el-table-column prop="status" label="状态">
        <template slot-scope="scope">
          {{scope.row.status==0?"正常":"禁用"}}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template slot-scope="scope">
          <el-button @click="switchDriverStatus(scope.row.id)">
            {{scope.row.status==0?"禁用":"启用"}}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
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
      isShowAdd: false,
      driverList: []
    };
  },
  created(){
  },
  mounted: function() {
    this.getDriverInfo();
  },
  methods: {
    deleteDriver(driverID){
      let that = this;
      this.req({
        url: "delete_driver",
        data: {
          id:driverID        
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              Message({
                message: '删除成功',
                type: 'success',
                duration: 3 * 1000
              })
              that.getDriverInfo()
          }},
          err => {
            console.log("err :", err);
          }
      );
    },
    switchDriverStatus(companyID){
      let that = this;
      this.req({
        url: "switch_company_status",
        data: {
          id:companyID        
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              Message({
                message: '修改成功',
                type: 'success',
                duration: 3 * 1000
              })
              that.getDriverInfo()
          }},
          err => {
            console.log("err :", err);
          }
      );
    },
    getDriverInfo(){
      let that = this;
      this.req({
        url: "get_all_driver_list",
        data: {
          id:localStorage.getItem("userId")          
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.driverList = res.content.data;
          }},
          err => {
            Message({
                message: '获取司机列表失败',
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