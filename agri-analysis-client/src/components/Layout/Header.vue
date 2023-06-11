<template>
  <div class="header-container">
    <div class="header-icon-wrapper" @click="$router.push('/')">
      <el-image
        class="header-icon"
        fit="contain"
        :src="require('@/assets/images/logo.png')"
      ></el-image>
    </div>
    <div class="header-title">农产品数据分析系统</div>
    <div class="header-user">
      <el-link :underline="false" type="primary" @click="$router.push('/login')" v-if="userInfo === null">登录</el-link>
      <template v-else>
        欢迎您，管理员 {{ userInfo.username }} ！
        <el-link :underline="false" type="primary" @click="handleLogout">退出</el-link>
      </template>
    </div>
  </div>
</template>

<script>
import { getUserInfo, logout } from '@/utils/auth'

export default {
  data() {
    return {
      userInfo: null,
      userInfoLoading: 0
    }
  },
  async created() {
    this.userInfo = await getUserInfo();
  },
  methods: {
    handleLogout() {
      this.userInfo = null;
      logout();
      this.$router.replace('/')
      this.$message.success("退出成功")
    }
  }
};
</script>

<style scoped lang="scss">
.header-container {
  height: 100%;
  width: 100%;
  background-color: #ebf1f6;
  display: flex;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;

  .header-icon-wrapper {
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: none;
    cursor: pointer;

    .header-icon {
      width: 120px;
      height: 50px;
    }
  }

  .header-title {
    flex: auto;
    text-align: center;
    font-size: 20px;
    line-height: 60px;
    font-weight: bold;
  }

  .header-user {
    flex: none;
    line-height: 60px;
    margin-right: 30px;
  }
}
</style>