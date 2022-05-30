<template>
<div>
  <div class="top-row">
    <div class="add-button">
      <el-button type="primary" @click="isShowAdd=true" size="small">上传模型</el-button>
    </div>
  </div>
  <div>
    <el-table :data="modelList" style="width: 100%">
      <el-table-column prop="model_type" label="模型类型" :formatter="formatModelType"></el-table-column>
      <el-table-column prop="filename" label="文件名"></el-table-column>
      <el-table-column prop="acc" label="精确度"></el-table-column>
      <el-table-column prop="param" label="参数数量"></el-table-column>
      <el-table-column prop="model_size" label="模型尺寸"></el-table-column>
      <el-table-column prop="in_use" label="使用状态">
        <template slot-scope="scope">
          <i v-if="scope.row.in_use ==1" style="color:coral">
             使用中
         </i>
         <i v-else>未使用</i>
        </template>
      </el-table-column>
      <el-table-column prop="in_use" label="操作">
        <template slot-scope="scope">
          <el-button @click="switchUseStatus(scope.row.id)" v-if="scope.row.in_use==0"  size="mini" type="success">
            使用
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog title="上传模型" :visible.sync="isShowAdd" width="480px" :close-on-click-modal="false"
      :close-on-press-escape="false" :modal-append-to-body="false">
      <div class="appoinment_win">
        <div class="line">
          <div class="label">模型类型：</div>
          <div class="content">
            <el-select v-model="header.modelType" placeholder="请选择">
              <el-option
                v-for="item in modelTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
        </div>
        <div class="line">        
          <div class="label">精确度：</div>
          <div class="content">
            <el-input v-model="header.acc">
              <template slot="append">%</template>
            </el-input>
          </div>
        </div>
        <div class="line">        
          <div class="label">参数数量：</div>
          <div class="content">
            <el-input v-model="header.paramCount"></el-input>
          </div>
        </div>
        <div class="line">
          <div class="label">选择模型：</div>
          <div class="content">
            <el-upload
              class="upload-demo"
              ref="uploadModel"
              action="/api/upload_model"
              accept="model/pt, model/pth"
              :auto-upload="false"
              :on-success="uploadSuccess"
              :on-change="fileChanged"
              :headers="header"
              :limit="1"
              :file-list="fileList">
              <el-button size="small" type="primary">点击上传</el-button>
              <!-- <div slot="tip" class="el-upload__tip">只能上传pt文件</div> -->
            </el-upload>
          </div>
        </div>
        <div style="text-align:right;margin-top:20px">
          <el-button @click="isShowAdd=false" >取消</el-button>
          <el-button @click="uploadModel" >提交</el-button>
        </div>
      </div>
    </el-dialog>
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
      modelList: [],
      header:{
        acc:0,
        paramCount:0,
        modelType:0,
        filename:''
      },      
      fileList:[],
      modelTypeOptions:[
        {value:0,label:'vgg16'},
        {value:1,label:'resnet50'},
        {value:2,label:'alexnet'}
      ]
    };
  },
  created(){
  },
  mounted: function() {
    this.getModelList();
  },
  methods: {
    getModelList(){
      let that = this;
      this.req({
        url: "get_model_list",
        data: {},
        method: "POST"
        }).then(
          res => {
             if(res.success){
              that.modelList = res.content.data;
          }},
          err => {
            Message({
                message: '获取模型列表失败',
                type: 'warning',
                duration: 3 * 1000
              })
            console.log("err :", err);
          }
      );
    },
    fileChanged(file, fileList){
      this.header.filename=file.name;
    },
    uploadModel(){
      this.$refs.uploadModel.submit();
    },
    switchUseStatus(modelId){
      let that = this;
      this.req({
        url: "switch_use_status",
        data: {
          id:modelId        
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
              that.getModelList()
          }},
          err => {
            console.log("err :", err);
          }
      );
    },
    formatModelType(row, column, cellValue, index){
      for(var i=0;i<this.modelTypeOptions.length;i++){
        if(this.modelTypeOptions[i].value==cellValue){
          return this.modelTypeOptions[i].label;
        }
      }
    },
    uploadSuccess(response, file, fileList){
      this.isShowAdd=false;
      this.header = {
        acc:0,
        paramCount:0,
        modelType:0,
        filename:''
      }
      this.fileList=[]
      Message({
                message: '上传成功',
                type: 'success',
                duration: 3 * 1000
              })
      this.getModelList()
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