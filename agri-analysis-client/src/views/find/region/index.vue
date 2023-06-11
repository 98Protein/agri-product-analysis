<template>
  <div class="page-wrapper">
    <div class="page-header">
      <el-form inline label-position="right" class="search-pane">
        <el-form-item label="日期">
          <el-date-picker
            v-model="searchDate"
            type="date"
            placeholder="选择日期"
          >
          </el-date-picker>
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
            icon="el-icon-search"
            :loading="!!searchLoading"
            @click="handleLoadCountryData"
            >查询</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <div class="page-main" v-loading="searchLoading">
      <el-empty v-if="!searched" description="暂无内容" style="width: 100%" />
      <template v-else>
        <div class="page-main-left">
          <v-chart
            @click="handleLineChartClicked"
            autoresize
            :option="leftOptions"
          />
        </div>
        <div class="page-main-right">
          <Map @changed="handleMapChanged" :provinceName="mapProvince" />
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import Map from "@/components/Map";
import lineChartOption from "./lineChartOption";
import {
  getTypeList,
  getVarietyList,
  getVariety,
  getProvinceList,
  getCityList,
  getMarketList,
} from "@/api/category";
import { getCountryData, getProvinceData, getCityData } from "@/api/region";
import dayjs from "dayjs";

export default {
  components: {
    Map,
  },
  data() {
    return {
      searchType: null,
      searchDate: null,
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

      leftOptions: lineChartOption,
      mapProvince: "全国",
      varietyName: "",
      provinceList: null,
      cityList: null,
      marketList: null,
      current: [],

      searched: false,
    };
  },
  methods: {
    handleMapChanged(v, level) {
      if (this.mapProvince === v) return;
      this.mapProvince = v;
      if (level === 0) {
        this.handleLoadCountryData();
        this.current = [];
      } else if (level === 1) {
        if (this.current.length === 2) this.current.splice(1, 1);
        this.handleLoadProvinceData(v);
      } else this.handleLoadCityData(v);
    },
    loadTypeCascade(node, resolve) {
      this.getTypeOptionsFuns[node.level](node.value).then((res) =>
        resolve(res)
      );
    },
    async handleLoadCountryData() {
      if (this.searchType === null || this.searchType.length === 0)
        return this.$message.error("种类不能为空")
      if (this.searchDate === null || this.searchDate.length === 0)
        return this.$message.error('日期不能为空')

      this.searchLoading++;
      getVariety(this.searchType[1]).then((res) => {
        this.varietyName = res.name;
        this.leftOptions.title.text = `${res.name} 区域行情 - 全国`;
        this.searchLoading--;
      });

      this.searchLoading++;
      const res = await getCountryData(
        dayjs(this.searchDate).format("YYYY-MM-DD"),
        this.searchType[1]
      );
      res.sort((a, b) => -a.name.localeCompare(b.name));
      this.leftOptions.yAxis.data = res.map((item) => item.name);
      this.leftOptions.series[0].data = res.map((item) => item["avg_price"]);
      this.searchLoading--;
      this.leftOptions.toolbox.feature.myBackBtn.show =
        this.current.length !== 0;
      this.searched = true;
    },
    async handleLoadProvinceData(provinceName) {
      const provinceId = this.provinceList.find(
        (item) => item.name === provinceName
      ).id;
      getCityList(provinceId).then((res) => (this.cityList = res));
      if (this.current.length == 0)
        this.current.push(provinceName);
      else
        this.current[0] = provinceName

      this.searchLoading++;
      this.leftOptions.title.text = `${this.varietyName} 区域行情 - ${provinceName}`;
      const res = await getProvinceData(
        dayjs(this.searchDate).format("YYYY-MM-DD"),
        this.searchType[1],
        provinceId
      );
      this.searchLoading--;
      res.sort((a, b) => -a.name.localeCompare(b.name));
      this.leftOptions.yAxis.data = res.map((item) => item.name);
      this.leftOptions.series[0].data = res.map((item) => item["avg_price"]);
      this.mapProvince = provinceName;
      this.leftOptions.toolbox.feature.myBackBtn.show =
        this.current.length !== 0;
    },
    async handleLoadCityData(cityName) {
      this.leftOptions.title.text = `${this.varietyName} 区域行情 - ${cityName}`;
      const cityId = this.cityList.find((item) => item.name === cityName).id;
      getMarketList(cityId).then((res) => (this.marketList = res));
      this.searchLoading++;
      const res = await getCityData(
        dayjs(this.searchDate).format("YYYY-MM-DD"),
        this.searchType[1],
        cityId
      );
      this.searchLoading--;
      if (this.current.length < 2)
        this.current.push(cityName);
      else
        this.current[1] = cityName
      res.sort((a, b) => -a.name.localeCompare(b.name));
      this.leftOptions.yAxis.data = res.map((item) => item.name);
      this.leftOptions.series[0].data = res.map((item) => item["avg_price"]);
      this.leftOptions.toolbox.feature.myBackBtn.show =
        this.current.length !== 0;
    },
    handleLineChartClicked({ name }) {
      if (this.current.length === 0) this.handleLoadProvinceData(name);
      else if (this.current.length === 1) this.handleLoadCityData(name);
    },
  },
  async created() {
    this.leftOptions.toolbox.feature.myBackBtn.onclick = () => {
      this.current.splice(this.current.length - 1, 1);
      if (this.current.length === 0) {
        this.handleLoadCountryData();
        this.mapProvince = "全国";
      } else if (this.current.length === 1)
        this.handleLoadProvinceData(this.current[0]);
      else this.handleLoadCityData(this.current[1]);
    };
    this.provinceList = await getProvinceList();
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