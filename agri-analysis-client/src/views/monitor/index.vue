<template>
  <div>
    <div class="fragment basic-info-fragment">
      <div class="fragment-header">基本信息</div>
      <div class="fragment-body" v-loading="!!basicInfoLoading">
        <div class="fragment-body-item">
          <div class="fragment-body-item-key">
            <i class="el-icon-school" style="color: rgba(248, 123, 6, 0.5)" />
            <span class="fragment-body-item-key-text">市场总数</span>
          </div>
          <div class="fragment-body-item-value" style="color: rgba(248, 123, 6, 0.5)">
            {{ basicInfo.marketTotal }}
          </div>
        </div>
        <div class="fragment-body-item">
          <div class="fragment-body-item-key">
            <i class="el-icon-orange" style="color: rgba(6, 187, 15, 0.411)" />
            <span class="fragment-body-item-key-text">品种总数</span>
          </div>
          <div class="fragment-body-item-value" style="color: rgba(6, 187, 15, 0.411)">
            {{ basicInfo.typeTotal }}
          </div>
        </div>
        <div class="fragment-body-item">
          <div class="fragment-body-item-key">
            <i class="el-icon-watermelon" style="color: rgba(214, 53, 4, 0.411)" />
            <span class="fragment-body-item-key-text">种类总数</span>
          </div>
          <div class="fragment-body-item-value" style="color: rgba(214, 53, 4, 0.411)">
            {{ basicInfo.varietyTotal }}
          </div>
        </div>
        <div class="fragment-body-item">
          <div class="fragment-body-item-key">
            <i class="el-icon-document-checked" style="color: rgba(6, 186, 218, 0.507)" />
            <span class="fragment-body-item-key-text">总抓取量</span>
          </div>
          <div class="fragment-body-item-value" style="color: rgba(6, 186, 218, 0.507)">
            {{ basicInfo.productTotal }}
          </div>
        </div>
      </div>
    </div>

    <div class="fragment data-monitor-fragment" style="margin-top: 20px">
      <div class="fragment-header">数据监控</div>
      <div class="fragment-body">
        <div class="fragment-body-header">
          <i class="el-icon-position fragment-body-header-icon" />
          <span class="fragment-body-header-title">查询/爬取</span>
        </div>
        <el-divider style="font-color=rgba(0, 0, 0, 0.200);"></el-divider>
        <div class="fragment-body-main">
          <el-form inline label-position="right" class="fragment-body-search-pane">
            <el-form-item label="日期范围">
              <el-date-picker v-model="searchDate" type="daterange" range-separator="至" start-placeholder="开始日期"
                end-placeholder="结束日期">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="地区">
              <el-cascader v-model="searchMarket" :props="{
                lazy: true,
                lazyLoad: loadMarketCascade,
              }" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="el-icon-search" @click="handleQuery"
                :loading="!!searchLoading">查询</el-button>
              <el-button icon="el-icon-odometer" @click="runCrwal" v-if="!carwl">爬取</el-button>
              <el-button v-else icon="el-icon-switch-button" @click="stopCrawl" :loading="!!stopLoading">停止</el-button>
            </el-form-item>
          </el-form>
          <div class="fragment-body-charts" v-loading="searchLoading">
            <el-empty v-if="!searchResult || searchResult.length == 0" description="暂无内容" />
            <template v-else>
              <v-chart autoresize class="fragment-body-line-chart" :option="lineChartOption"
                @click="handleLineChartClicked" />
              <el-empty v-if="!lineClicked" description="请选择日期" class="fragment-body-pie-chart" />
              <v-chart v-else autoresize class="fragment-body-pie-chart" :option="pieChartOption" />
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import lineChartOption, { generateSeries } from "./lineChartOption";
import pieChartOption from "./pieChartOption";
import { getBasicInfo, getCrawls, runScrapy, stopScrapy } from "@/api/monitor";
import {
  getProvinceList,
  getMarketList,
  getCityList,
  getTypeList,
} from "@/api/category";
import dayjs from "dayjs";

export default {
  data() {
    return {
      basicInfo: {},
      basicInfoLoading: 0,
      carwl: false,
      searchMarket: null,
      searchLoading: 0,
      stopLoading: 0,
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

      searchDate: [],
      searchResult: [],

      lineChartOption,
      pieChartOption,
      lineClicked: false,

      typeList: [],
    };
  },
  async created() {
    this.basicInfoLoading++;
    this.basicInfo = await getBasicInfo();
    const typeList = await getTypeList();
    this.lineChartOption.series = typeList.map((item) =>
      generateSeries(item.name, item["id"])
    );
    this.lineChartOption.legend.data = typeList.map((item) => item.name);
    this.typeList = typeList;
    this.basicInfoLoading--;
  },
  methods: {
    handleLineChartClicked({ name: date }) {
      const record = this.searchResult.find((item) => item.date === date);
      this.pieChartOption.title.subtext = record.date;
      this.pieChartOption.series[0].data = record.items.map((item) => ({
        name: this.typeList.find((type) => type.id === item["type_id"]).name,
        value: item.count,
      }));
      this.lineClicked = true;
    },
    loadMarketCascade(node, resolve) {
      this.getMarketOptionsFuns[node.level](node.value).then((res) =>
        resolve(res)
      );
    },
    async handleQuery() {
      if (this.searchDate.length === 0)
        return this.$message.error("请选择正确的时间范围")
      if (this.searchMarket === null)
        return this.$message.error("地区不能为空")

      this.searchLoading++;

      const records = await getCrawls(
        this.searchDate.map((item) => dayjs(item).format("YYYY-MM-DD")),
        this.searchMarket[2]
      );
      this.lineChartOption.xAxis[0].data = records.map((item) => item.date);
      this.lineChartOption.series.forEach((series) => {
        series.data = records.map((record) => {
          const res = record.items.find(
            (item) => item["type_id"] === series.meta.id
          );
          return res ? res.count : 0;
        });
      });
      this.searchResult = records;

      this.searchLoading--;
    },
    runCrwal() {
      if (this.searchDate.length === 0)
        return this.$message.error("请选择正确的时间范围")
      runScrapy(this.searchDate.map((item) => dayjs(item).format("YYYY-MM-DD"))).then(res => {
        if (res.success) {
          // console.log(res)
          this.carwl = true
          this.timer = setInterval(async () => {
            this.basicInfo = await getBasicInfo();
          }, 2000); // 每2秒执行一次
        }
      }).catch(err => {
        console.log(err)
      })
    },
    async stopCrawl() {
      this.stopLoading++
      clearInterval(this.timer); // 清除定时器
      const res = await stopScrapy()
      if (res.success) {
        this.stopLoading--
        this.carwl = false
      }
    }
  },
};
</script>

<style scoped lang="scss">
.fragment {
  .fragment-header {
    font-size: 32px;
    color: rgba(0, 0, 0, 0.658);
    font-family: "微软雅黑";
    font-weight: 600;
    margin-bottom: 20px;
  }

  .fragment-body {
    font-size: 12px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
}

.fragment.basic-info-fragment {
  .fragment-body {
    display: flex;

    .fragment-body-item {
      flex: auto;

      .fragment-body-item-key {
        font-size: 30px;
        font-family: "微软雅黑";
        font-weight: 500;
        text-align: center;
        margin-bottom: 20px;

        .fragment-body-item-key-text {
          margin-left: 10px;
          color: rgba(0, 0, 0, 0.438);
          font-size: 20px;
          line-height: 40px;
          vertical-align: top;
        }
      }

      .fragment-body-item-value {
        font-size: 40px;
        font-family: "微软雅黑";
        font-weight: 600;
        text-align: center;
      }
    }
  }
}

.fragment.data-monitor-fragment {
  .fragment-body {
    .fragment-body-header {
      .fragment-body-header-icon {
        margin-left: 30px;
        color: rgba(0, 132, 255, 0.61);
        font-size: 30px;
      }

      .fragment-body-header-title {
        margin-left: 10px;
        vertical-align: super;
        color: rgba(0, 0, 0, 0.459);
        font-size: 23px;
      }
    }

    .fragment-body-main {
      display: flex;
      flex-direction: column;
      align-items: center;

      .fragment-body-charts {
        display: flex;
        margin-top: 10px;
        justify-content: space-evenly;
        width: 100%;

        .fragment-body-line-chart {
          height: 500px;
          width: 1000px;
          flex: none;
        }

        .fragment-body-pie-chart {
          height: 500px;
          width: 500px;
          flex: none;
        }
      }
    }
  }
}
</style>