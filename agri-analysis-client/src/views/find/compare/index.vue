<template>
  <div class="page-wrapper">
    <div class="page-header">
      <el-date-picker
        v-model="timeRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="loadData"
      >
      </el-date-picker>
      <div style="height: 40px; border-left: 1px solid #DCDFE6; margin: 0 40px" />
      <el-form inline label-position="right" class="search-pane">
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
          <el-button
            type="primary"
            icon="el-icon-plus"
            @click="handleAddCompareItem"
            >添加</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <div class="page-main" v-loading="!!loading">
      <el-table class="page-main-left" :data="compareList">
        <el-table-column label="地区">
          <template v-slot="scope">{{ scope.row.market.name }}</template>
        </el-table-column>
        <el-table-column label="种类" :width="120">
          <template v-slot="scope">{{ scope.row.variety.name }}</template>
        </el-table-column>
        <el-table-column label="操作" :width="80">
          <template v-slot="scope"
            ><el-button
              size="mini"
              type="danger"
              @click="handleRemoveCompareItem(scope.$index)"
              >删除</el-button
            ></template
          >
        </el-table-column>
      </el-table>
      <el-empty class="page-main-right" v-if="!compareList || compareList.length == 0" description="暂无内容"/>
      <v-chart ref="myChart" v-else class="page-main-right" autoresize :option="chartOption" />
    </div>
  </div>
</template>

<script>
import chartOption, {generateSeries} from "./chartOption";
import { getPriceDatas } from "@/api/compare"
import {
  getProvinceList,
  getMarketList,
  getCityList,
  getTypeList,
  getVarietyList,
  getMarket,
  getVariety,
} from "@/api/category";
import dayjs from 'dayjs';

export default {
  data() {
    return {
      timeRange: [],
      searchType: null,
      searchMarket: null,
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

      compareList: [],
      loading: 0,
      chartOption,
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
    async handleAddCompareItem() {
      if (this.searchMarket === null || this.searchMarket.length === 0)
        return this.$message.error('市场不能为空')
      if (this.searchType === null || this.searchType.length === 0)
        return this.$message.error('种类不能为空')
      if (this.timeRange === null || this.timeRange.length === 0)
        return this.$message.error('日期范围不能为空')
      const [market, variety] = await Promise.all([
        getMarket(this.searchMarket[2]),
        getVariety(this.searchType[1]),
      ]);
      this.compareList.push({
        market,
        variety,
      });
      await this.loadData();
    },
    async handleRemoveCompareItem(index) {
      this.compareList.splice(index, 1);
      await this.loadData();
    },
    async loadData() {
      this.loading++;
      const records = await getPriceDatas(
        this.timeRange.map(item => dayjs(item).format('YYYY-MM-DD')),
        this.compareList.map(item => ({
          marketId: item.market.id,
          varietyId: item.variety.id
        }))
      )
      this.chartOption.xAxis[0].data = records.map(item => item.date)
      this.chartOption.legend.data = records.map(item => `${item['market_name']} ${item['variety_name']}`)
      this.chartOption.series = this.compareList.map(item => generateSeries(`${item.market.name} ${item.variety.name}`, item.market.id, item.variety.id))
      this.chartOption.series.forEach(series => {
        series.data = records.map(record => {
          const res = record.items.find(item => item['variety_id'] === series.meta.varietyId && item['market_id'] === series.meta.marketId)
          return res ? res.price : 0
        })
      })
      this.$refs.myChart && this.$refs.myChart.setOption(this.chartOption, true);
      this.loading--;
    }
  },
};
</script>

<style lang="scss" scoped>
.page-wrapper {
  display: flex;
  height: 100%;
  flex-direction: column;

  .page-header {
    display: flex;
    flex: none;
    justify-content: center;
    border-bottom: 1px solid #dcdfe6;
    margin-bottom: 20px;
  }

  .page-main {
    flex: auto;
    display: flex;
    .page-main-left {
      width: 600px;
      height: 100%;
      flex: none;
    }
    .page-main-right {
      flex: auto;
    }
  }
}
</style>