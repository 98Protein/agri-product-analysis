<template>
  <el-container class="layout-container">
    <el-header class="layout-header-wrapper" style="padding: 0"><Header /></el-header>
    <el-container class="layout-center-wrapper">
      <el-aside width="200px"><MenuBar /></el-aside>
      <el-container>
        <el-main><transition name="fade-transform" mode="out-in"><router-view /></transition></el-main>
      </el-container>
    </el-container>
    <el-footer class="layout-footer-wrapper" style="border-top: solid 1px #e6e6e6;"><Footer /></el-footer>
  </el-container>
</template>

<script>
import Header from "./Header.vue";
import MenuBar from "./MenuBar.vue";
import Footer from "./Footer.vue";

export default {
  components: {
    Header,
    MenuBar,
    Footer,
  },
};
</script>

<style scoped lang="scss">

.layout-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;

  .layout-header-wrapper {
    flex: none;
  }

  .layout-center-wrapper {
    flex: auto;
  }

  .layout-footer-wrapper {
    flex: none;
  }
}

</style>
