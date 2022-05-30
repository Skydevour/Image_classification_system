<template>
<div>
<div style="display:inline-block;width:100%;vertical-align: top">
  <div style="display:inline-block;width:38%;margin-left: 1%;">
    <el-upload
      action="/api/process_img"
      accept="image/png, image/jpeg, image/jpg"
      :show-file-list="false"
      :on-success="handleAvatarSuccess" class="" style="width:100%;margin: 0;padding: 0;">
      <img v-if="imageUrl" :src="imageUrl" style="width:100%;">
      <img v-else src="@/assets/upload.png"  style="width:100%;">
    </el-upload>
  </div>
  <div style="display:inline-block;width:38%;margin-left: 2%;">
    <img v-if="heatMapSrc" :src="heatMapSrc" class="avatar" style="width:100%;">
    <img v-else src="@/assets/none.png"  style="width:100%;">
  </div>
  <div style="display:inline-block;width:18%;margin-left: 2%;vertical-align: top;margin-top:10px">
    <div style="margin-top:20px">分类结果(top5)：</div>
    <div>
      <el-table :data="classifyResult" style="width: 100%">
        <el-table-column label="#" :formatter="formatRank" width="30px"></el-table-column>
        <el-table-column prop="name" label="类别"></el-table-column>
      </el-table>
    </div>
    <div style="margin-top:20px">模型类别：{{classifyType!=-1?modelTypeOp[classifyType]:''}}</div>
    <div style="margin-top:20px">模型文件名：{{modelName}}</div>
  </div>
</div>
</div>
</template>

<script>
import {
  Message
} from 'element-ui'
import VueCoreImageUpload from 'vue-core-image-upload'
export default {
  components: {
    'vue-core-image-upload': VueCoreImageUpload,
  },
  data() {
    return {
      imageUrl: '',
      heatMapSrc:'',
      classifyType:-1,
      classifyResult:[],
      modelName:'',
      modelTypeOp:{
        0:'vgg16',
        1:'resnet50',
        2:'alexnet'
      }
    };
  },
  created(){
  },
  mounted: function() {
  },
  methods: {
    handleAvatarSuccess(res, file){
      this.imageUrl = URL.createObjectURL(file.raw);
      console.log(res.content);
      this.classifyResult = res.content.result;
      this.classifyType = res.content.model_type;
      this.modelName = res.content.model_name;
      this.heatMapSrc = "data:image/jpg;base64,"+res.content.heatmap;
    },
    formatRank(row, column, cellValue, index){
      return index+1;
    },
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
.el-upload{
  margin: 0;
  padding: 0;
  width:100%;
}
.el-upload--text{
  margin: 0;
  padding: 0;
  width:100%;
}
</style>