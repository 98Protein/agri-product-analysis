<template>
  <el-menu :default-active="currentRoutePath" router style="height: 100%">
    <fragment v-for="route in routes" :key="route.path">
      <el-menu-item
        v-if="
          !route.meta.hasChildren &&
          (!route.meta.allow ||
            (userInfo && route.meta.allow.indexOf(userInfo.identity) !== -1))
        "
        :index="route.path"
      >
        <i :class="route.meta.icon"></i>
        <span slot="title">{{ route.meta.title }}</span>
      </el-menu-item>
      <el-submenu v-else :index="route.path">
        <template slot="title">
          <i :class="route.meta.icon"></i>
          <span>{{ route.meta.title }}</span>
        </template>
        <template v-for="subRoute in route.children">
          <el-menu-item
            v-if="
              !subRoute.meta.allow ||
              (userInfo &&
                subRoute.meta.allow.indexOf(userInfo.identity) !== -1)
            "
            :key="subRoute.path"
            :index="subRoute.path"
          >
            <i :class="subRoute.meta.icon"></i>
            <span slot="title">{{ subRoute.meta.title }}</span>
          </el-menu-item>
        </template>
      </el-submenu>
    </fragment>
  </el-menu>
</template>

<script>
import { dashboardRoutes } from "@/routes";
import { subscribe, getUserInfo } from "@/utils/auth";

export default {
  data() {
    return {
      routes: dashboardRoutes,
      userInfo: null,
    };
  },
  computed: {
    currentRoutePath() {
      return this.$route.path;
    },
  },
  async created() {
    this.userInfo = await getUserInfo();
    const that = this;
    subscribe((val) => {
      that.userInfo = val;
    });
  },
};
</script>

<style scoped>
</style>
