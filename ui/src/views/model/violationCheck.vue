<template>
<div>
  <div class="top-row">
    <!-- <div class="add-button">
      <el-button type="primary" @click="isShowAdd=true">新增司机</el-button>
    </div> -->
  </div>
  <div>
    <el-table :data="violationList" style="width: 100%">
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="id_number" label="身份证"></el-table-column>
      <el-table-column prop="company_name" label="所属企业" ></el-table-column>
      <el-table-column prop="violation_time" label="时间" ></el-table-column>
      <el-table-column prop="violation_content" label="违章内容"></el-table-column>
      <el-table-column prop="appeal_content" label="申诉内容" ></el-table-column>
      <el-table-column prop="video_path" label="视频" ></el-table-column>
      <el-table-column prop="verify" label="状态" ></el-table-column>
      <el-table-column label="操作" width="280">
        <template slot-scope="scope">
          <el-button @click="checkVio(scope.row.id, 3)" type="success" size="mini" :disabled="scope.row.verify==3||scope.row.verify==1">申诉通过</el-button>
          <el-button @click="checkVio(scope.row.id, 2)" type="warning" size="mini" :disabled="scope.row.verify==2||scope.row.verify==1">申诉不通过</el-button>
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
      violationList: []
    };
  },
  created(){
  },
  mounted: function() {
    this.getViolationList();
  },
  methods: {
    getViolationList(){
      let that = this;
      this.req({
        url: "get_all_vio_list",
        data: {
          id:localStorage.getItem("userId")          
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.violationList = res.content.data;
          }},
          err => {
            Message({
                message: '获取违章列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
            console.log("err :", err);
          }
      );
    },
    checkVio(id, state){
      let that = this;
      this.req({
        url: "set_vio_status",
        data: {
          id:id,        
          state:state        
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              Message({
                message: '操作成功',
                type: 'success',
                duration: 2 * 1000
              })
              that.getViolationList()
          }},
          err => {
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