<template>
<div>
  <div class="top-row">
    <!-- <div class="add-button">
      <el-button type="primary" @click="isShowAdd=true">新增司机</el-button>
    </div> -->
  </div>
  <div>
    <el-table :data="goodthingList" style="width: 100%">
      <el-table-column prop="name" label="姓名" width=80></el-table-column>
      <el-table-column prop="id_number" label="身份证"></el-table-column>
      <el-table-column prop="company_name" label="所属企业" ></el-table-column>
      <el-table-column prop="happen_time" label="发生时间" ></el-table-column>
      <el-table-column prop="thing_content" label="内容"></el-table-column>
      <el-table-column prop="video_path" label="视频" ></el-table-column>
      <el-table-column prop="verify" label="状态" ></el-table-column>
      <el-table-column label="操作" width="280">
        <template slot-scope="scope">
          <el-button @click="checkGoodthing(scope.row.id, 1)" type="success" size="mini" :disabled="scope.row.verify==1">通过</el-button>
          <el-button @click="checkGoodthing(scope.row.id, 2)" type="warning" size="mini" :disabled="scope.row.verify==2">不通过</el-button>
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
      goodthingList: []
    };
  },
  created(){
  },
  mounted: function() {
    this.getgoodthingList();
  },
  methods: {
    getgoodthingList(){
      let that = this;
      this.req({
        url: "get_all_good_thing_list",
        data: {
          id:localStorage.getItem("userId")          
        },
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.goodthingList = res.content.data;
          }},
          err => {
            Message({
                message: '获取好人好事列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
            console.log("err :", err);
          }
      );
    },
    checkGoodthing(id, state){
      let that = this;
      this.req({
        url: "set_good_thing_status",
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
              that.getgoodthingList()
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