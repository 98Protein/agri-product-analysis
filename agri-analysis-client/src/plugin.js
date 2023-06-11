import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import '@/assets/style/global.scss'
import Fragment from 'vue-fragment'
import dayjs from 'dayjs';
import ECharts from 'vue-echarts'
import 'echarts'

Vue.use(ElementUI);
Vue.use(Fragment.Plugin);

Vue.component('v-chart', ECharts)
dayjs.extend(require('dayjs/plugin/customParseFormat'))