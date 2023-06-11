<template>
  <v-chart
    autoresize
    :option="rightOptions"
    @select="handleProvinceClick"
    :loading="mapLoading"
  />
</template>

<script>
import * as echarts from "echarts";
import provinceMap from "@/utils/map/province-map.js";
import axios from "axios";
export default {
  props: {
    provinceName: String
  },
  data() {
    return {
      mapLoading: false,
      rightOptions: {},
      provinceShowing: null,
      provinceData: null
    };
  },
  async created() {
    this.mapLoading = true;
    this.chinaData = (await axios.get("/map/china.json")).data;
    echarts.registerMap("china", this.chinaData);
    this.rightOptions = {
      title: {
        text: "全国地图",
      },
      series: [
        {
          type: "map",
          map: "china",
          selectedMode: "single",
        },
      ],
      toolbox: {
        show: true,
        feature: {
          myBackBtn: {
            show: false,
            title: "返回",
            icon: `image://${require("@/assets/images/back.svg")}`,
            onclick: this.handleMapBack,
          },
        },
      },
    };
    this.mapLoading = false;
  },
  methods: {
    async handleProvinceClick({ dataIndexInside: index, provinceName }) {
      if (this.provinceShowing) {
        if (index !== null && index !== undefined) {
          if (this.provinceShowing === '新疆')
            index++;
          this.$emit('changed', this.provinceData.features[index].properties.name, 2)
        }
        return
      }
      if (provinceName === '全国')
        return this.handleMapBack()

      this.mapLoading = true;
      this.rightOptions.toolbox.feature.myBackBtn.show = true;
      const _provinceName =
        provinceName ? provinceName : this.chinaData.features[index].properties.name;
      this.provinceShowing = _provinceName;
      const provinceData = (
        await axios.get(`/map/province/${provinceMap[_provinceName]}.json`)
      ).data;
      this.provinceData = provinceData
      this.rightOptions.series[0].map = provinceMap[_provinceName];
      this.rightOptions.title.text = `${this.provinceShowing}地图`;
      echarts.registerMap(provinceMap[_provinceName], provinceData);
      this.mapLoading = false;
      this.$emit('changed', _provinceName, 1);
    },
    handleMapBack() {
      this.provinceShowing = null;
      this.rightOptions.series[0].map = "china";
      this.rightOptions.title.text = "全国地图";
      this.$emit('changed', '全国', 0);
    },
  },
  watch: {
    provinceName(val) {
      if (val === '全国')
        return this.handleMapBack()
      this.handleProvinceClick({
        provinceName: val
      })
    }
  }
};
</script>

<style>
</style>