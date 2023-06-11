<template>
  <div class="page-wrapper">
    <el-form inline label-position="right" class="search-pane">
      <el-form-item label="日期范围">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        >
        </el-date-picker>
      </el-form-item>

      <el-form-item label="时间间隔">
        <el-select v-model="dateInterval" placeholder="请选择">
          <el-option label="年" value="year" />
          <el-option label="月" value="month" />
          <el-option label="日" value="day" />
        </el-select>
      </el-form-item>

      <el-form-item label="地区">
        <el-cascader
          v-model="searchMarket"
          :props="{
            lazy: true,
            lazyLoad: loadMarketCascade,
          }"
        />
      </el-form-item>

      <el-form-item label="种类">
        <el-cascader
          v-model="searchType"
          :props="{
            lazy: true,
            lazyLoad: loadTypeCascade,
          }"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleQuery" :loading="!!searchLoading"
          >查询</el-button
        >
      </el-form-item>
    </el-form>

    <el-empty v-if="!queried" description="暂无内容" />
    <v-chart
      v-else
      v-loading="!!searchLoading"
      class="chart"
      autoresize
      :option="chartOption"
    />
  </div>
</template>

<script>
import {
  getProvinceList,
  getMarketList,
  getCityList,
  getTypeList,
  getVarietyList,
} from "@/api/category";

import chartOption from "./chartOption";
import { getYearSellData, getMonthSellData, getDaySellData } from "@/api/sell";

export default {
  data() {
    return {
      dateRange: null,
      dateInterval: null,
      searchType: null,
      searchMarket: null,
      searchLoading: 0,
      getTypeOptionsFuns: [
        async () =>
          (await getTypeList()).map((item) => ({
            label: item.name,
            value: item.id,
            leaf: false,
          })),
        async (typeId) =>
          (await getVarietyList(typeId)).map((item) => ({
            label: item.name,
            value: item.id,
            leaf: true,
          })),
      ],
      getMarketOptionsFuns: [
        async () =>
          (await getProvinceList()).map((item) => ({
            label: item.name,
            value: item.id,
            leaf: false,
          })),
        async (provinceId) =>
          (await getCityList(provinceId)).map((item) => ({
            label: item.name,
            value: item.id,
            leaf: false,
          })),
        async (cityId) =>
          (await getMarketList(cityId)).map((item) => ({
            label: item.name,
            value: item.id,
            leaf: true,
          })),
      ],

      chartOption,
      queried: false,
    };
  },
  methods: {
    loadTypeCascade(node, resolve) {
      this.getTypeOptionsFuns[node.level](node.value).then((res) =>
        resolve(res)
      );
    },
    loadMarketCascade(node, resolve) {
      this.getMarketOptionsFuns[node.level](node.value).then((res) =>
        resolve(res)
      );
    },
    async handleQuery() {
      if (this.dateRange === null || this.dateRange.length === 0)
        return this.$message.error("日期范围不能为空");
      if (this.searchMarket === null || this.searchMarket.length === 0)
        return this.$message.error("市场不能为空");
      if (this.searchType === null || this.searchType.length === 0)
        return this.$message.error("种类不能为空");

      this.searchLoading++;

      let records = [];

      if (this.dateInterval === "year") {
        records = await getYearSellData(
          this.dateRange,
          this.searchMarket[2],
          this.searchType[1]
        );
      } else if (this.dateInterval === "month") {
        records = await getMonthSellData(
          this.dateRange,
          this.searchMarket[2],
          this.searchType[1]
        );
      } else {
        records = await getDaySellData(
          this.dateRange,
          this.searchMarket[2],
          this.searchType[1]
        );
      }
      records.sort((a, b) => a.time.localeCompare(b.time));

      this.chartOption.xAxis.data = records.map((item) => item.time);
      this.chartOption.series[0].data = records.map((item) => item.sum);

      this.searchLoading--;
      this.queried = true;
    },
  },
};
</script>

<style scoped lang="scss">
.page-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;

  .search-pane {
    flex: none;
    display: flex;
    justify-content: center;
    border-bottom: 1px solid #dcdfe6;
    margin-bottom: 24px;
  }

  .chart {
    width: 100%;
    flex: auto;
  }
}
</style>