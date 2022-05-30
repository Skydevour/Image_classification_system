<template>
  <div style="height:100%">
    <!-- <div id="allmap" ref="allmap" width="100%" height="100%"></div> -->
    <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">图像分类系统</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          id="account"
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          id="psw"
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-button
        id="login_btn"
        :loading="loading"
        type="primary"
        style="width:48%;margin-bottom:6px;display:inline-block"
        @click.native.prevent="handleLogin"
      >登录</el-button>
      <el-button
        style="width:48%;margin-bottom:6px;display:inline-block;"
        @click="isShowSignUp=true"
      >注册</el-button>
      <el-button type="text" @click="isShowChangePsd=true">忘记密码？</el-button>
    </el-form>
    </div>
    <el-dialog title="注册" :visible.sync="isShowSignUp" width="480px" :close-on-click-modal="false"
      :close-on-press-escape="false" :modal-append-to-body="false">
      <div class="appoinment_win">
        <div class="line">
          <div class="label">用户名：</div>
          <div class="content">
            <el-input v-model="signUpInfo.username"></el-input>
          </div>
        </div>
        <div class="line">        
          <div class="label">密码：</div>
          <div class="content">
            <el-input v-model="signUpInfo.psd" show-password></el-input>
          </div>
        </div>
        <div class="line">        
          <div class="label">确认密码：</div>
          <div class="content">
            <el-input v-model="signUpInfo.confirmPsd" show-password></el-input>
          </div>
        </div>
        <div class="line">
          <div class="label">电话：</div>
          <div class="content">
            <el-input v-model="signUpInfo.phone"></el-input>
          </div>
        </div>
        <div class="line">
          <div  class="label">邮箱：</div>
          <div class="content">
            <el-input v-model="signUpInfo.email"></el-input>
          </div>
        </div>
        <div style="text-align:right;margin-top:20px">
          <el-button @click="isShowSignUp=false" >取消</el-button>
          <el-button @click="signUp" >提交</el-button>
        </div>
      </div>
    </el-dialog>
    <el-dialog title="找回密码" :visible.sync="isShowChangePsd" width="480px" :close-on-click-modal="false"
      :close-on-press-escape="false" :modal-append-to-body="false">
      <div class="appoinment_win">
        <div class="line">
          <div class="label">邮箱：</div>
          <div class="content">
            <el-input v-model="changePsdInfo.email"></el-input>
          </div>
        </div>
        <div class="line">        
          <div class="label">密码：</div>
          <div class="content">
            <el-input v-model="changePsdInfo.psd" show-password></el-input>
          </div>
        </div>
        <div class="line">        
          <div class="label">确认密码：</div>
          <div class="content">
            <el-input v-model="changePsdInfo.confirmPsd" show-password></el-input>
          </div>
        </div>
        <div style="text-align:right;margin-top:20px">
          <el-button @click="isShowChangePsd=false" >取消</el-button>
          <el-button @click="changePsd" >提交</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  Message
} from 'element-ui'
import md5 from "js-md5";
import qs from 'qs';
export default {
  name: "Login",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 3) {
        callback(new Error("Please enter the correct user name"));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (value.length < 2) {
        callback(new Error("The password can not be less than 2 digits"));
      } else {
        callback();
      }
    };
    return {
      loginForm: {
        username: "",
        password: ""
      },
      loginRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ]
      },
      loading: false,
      passwordType: "password",
      redirect: undefined,
      isShowSignUp:false,
      isShowChangePsd:false,
      signUpInfo:{
        username:'',
        psd:'',
        confirmPsd:'',
        phone:'',
        email:''
      },
      changePsdInfo:{
        email:'',
        psd:'',
        confirmPsd:''
      }
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  mounted() { 
  },
  methods: {
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    handleLogin() {
      let that = this;
      this.loading = true;
      this.req({
        url: "login",
        data: {
          username: that.loginForm.username,
          psd: that.loginForm.password //对密码进行加盐md5处理
        },
        method: "POST"
        }).then(
          res => {
            if(res.content.result){
              localStorage.setItem("hasLogin", true);
              this.loading = false;
              localStorage.setItem("token", res.content.token);
              localStorage.setItem("userId", res.content.id);
              localStorage.setItem("isAdmin", res.content.is_admin);
              localStorage.setItem("userType", res.content.user_type);
              this.$router.go(0);
              console.log(localStorage.getItem("userType"));
              if(localStorage.getItem("userType")==1){
                this.$router.push({ path: "/info" });
              }else if(localStorage.getItem("userType")==2){
                this.$router.push({ path: "/violation_manage" });
              }else{
                this.$router.push({ path: "/manage" });
              }
            }else{
               Message({
                message: '用户名或密码错误',
                type: 'warning',
                duration: 2 * 1000
              })
              this.loading = false;
            }
          },
          err => {
            console.log("err :", err);
            this.passwordError = true;
            this.loading = false;
          }
        );
        console.log(localStorage.getItem("userType"));
        // localStorage.setItem("hasLogin", true);
        // this.$router.push({ path: "/" });
      },
    signUp(){
      let that = this
      if(!that.signUpInfo.username){
        Message({
                message: '请输入用户名',
                type: 'warning',
                duration: 2 * 1000
              })
        return
      }
      if(!that.signUpInfo.psd){
        Message({
                message: '请输入密码',
                type: 'warning',
                duration: 2 * 1000
              })
              return
      }
      if(that.signUpInfo.confirmPsd!=that.signUpInfo.psd){
        Message({
                message: '密码不一致，请确认',
                type: 'warning',
                duration: 2 * 1000
              })
              return
      }
      if(!that.signUpInfo.email){
        Message({
                message: '请输入邮箱',
                type: 'warning',
                duration: 2 * 1000
              })
              return
      }
      this.req({
        url: "signup",
        data: that.signUpInfo,
        method: "POST"
        }).then(
          res => {
            if(res.success){
              Message({
                message: '注册成功，请登录',
                type: 'success',
                duration: 3 * 1000
              })
              this.isShowSignUp=false
            }else{
              Message({
                message: '注册失败',
                type: 'error',
                duration: 3 * 1000
              })
            }
          },
          err => {
            console.log("err :", err);
            this.passwordError = true;
            this.loading = false;
          }
        )
    },
    changePsd(){
      let that = this
      if(!that.changePsdInfo.email){
        Message({
                message: '请输入邮箱',
                type: 'warning',
                duration: 2 * 1000
              })
        return
      }
      if(!that.changePsdInfo.psd){
        Message({
                message: '请输入密码',
                type: 'warning',
                duration: 2 * 1000
              })
              return
      }
      if(that.changePsdInfo.confirmPsd!=that.changePsdInfo.psd){
        Message({
                message: '密码不一致，请确认',
                type: 'warning',
                duration: 2 * 1000
              })
              return
      }
      this.req({
        url: "reset_psd",
        data: that.changePsdInfo,
        method: "POST"
        }).then(
          res => {
            if(res.success){
              Message({
                message: '重置密码成功，请前往登录',
                type: 'success',
                duration: 3 * 1000
              })
              this.isShowChangePsd=false
            }else{
              Message({
                message: '重置密码失败',
                type: 'error',
                duration: 3 * 1000
              })
            }
          },
          err => {
            console.log("err :", err);
          }
        )
    },
  }
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */
.info {
  position: fixed;
  bottom: 20px;
  width: 100%;
  text-align: center;
  color: gainsboro;
}
$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  height:100%;
  width:100%;
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
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
