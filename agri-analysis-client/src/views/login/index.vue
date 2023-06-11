<template>
  <div class="login-page">
    <el-card class="login-card">
      <div slot="header" class="login-card-header">农产品数据分析系统</div>
      <el-form label-position="top" size="default">
        <el-form-item prop="username">
          <el-input type="text" placeholder="用户名" v-model="form.username">
            <i slot="prepend" class="el-icon-user"></i>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" placeholder="密码" v-model="form.password">
            <i slot="prepend" class="el-icon-lock"></i>
          </el-input>
        </el-form-item>
        <el-button
          class="login-card-submit-btn"
          type="primary"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script>

import { login } from "@/api/admin";
import {setToken} from '@/utils/auth'

export default {
  data() {
    return {
      form: {},
    };
  },
  methods: {
    async handleLogin() {
      const info = await login(this.form.username, this.form.password)
      if (!info.success)
        this.$message.error(info.reason)
      else {
        setToken(info.token)
        this.$message.success("登录成功")
        this.$router.replace('/')
      }
    },
  },
};
</script>

<style scoped lang="scss">
.login-page {
  width: 100%;
  height: 100%;
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;

  .login-card {
    width: 320px;

    .login-card-header {
      text-align: center;
    }

    .login-card-submit-btn {
      width: 100%;
    }
  }
}
</style>
