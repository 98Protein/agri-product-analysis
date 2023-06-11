<template>
  <div class="password-form-wrapper">
    <el-form class="password-form" status-icon label-width="100px" v-loading="loading">
      <el-form-item label="原密码" prop="oldPassword">
        <el-input
          type="password"
          v-model="passwordObj.oldPassword"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input
          type="password"
          v-model="passwordObj.newPassword"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPassword">
        <el-input
          type="password"
          v-model="passwordObj.checkPassword"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">
          确定
        </el-button>
        <el-button @click="passwordObj = {}">清空</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { changePassword } from '@/api/admin'
export default {
  data() {
    return {
      passwordObj: {},
      loading: false
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.passwordObj.oldPassword)
        return this.$message.error("原密码不能为空")
      if (!this.passwordObj.newPassword)
        return this.$message.error("新密码不能为空")
      if (!this.passwordObj.checkPassword)
        return this.$message.error("确认密码不能为空")
      if (this.passwordObj.checkPassword !== this.passwordObj.newPassword)
        return this.$message.error("两次密码输入不同")
      this.loading = true;
      const res = await changePassword(this.passwordObj.oldPassword, this.passwordObj.newPassword)
      this.loading = false
      if (!res.success)
        return this.$message.error(res.reason);
      this.$message.success('修改密码成功')
      this.passwordObj = {}
    }
  }
};
</script>

<style scoped lang="scss">
.password-form-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;

  .password-form {
    width: 40%;
    min-width: 600px;
  }
}
</style>