export default {
  backgroundColor: '#fff',
  title: {
    text: '农产品售卖行情',
    textStyle: {
      color: '#000',
      fontSize: 18,
      fontWeight: 'bold'
    },
    subtext: '已根据您选择的时间间隔显示图表',
    subtextStyle: {
      color: '#000'
    }
  },
  tooltip: {
    show: true,
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#000'
      }
    }
  },
  grid: {
    left: 20,
    right: 20,
    top: 80,
    bottom: 20,
    containLabel: true
  },
  xAxis: {
    show: true,
    axisLabel: {
      interval: 1,
      rotate: -20,
      margin: 30,
      color: '#000',
      align: 'center'
    },
    axisTick: {
      alignWithLabel: true,
      lineStyle: {
        color: '#000'
      }
    },
    data: []
  },
  yAxis: [
    {
      type: 'value',
      name: '(人/次)',
      nameTextStyle: {
        color: '#000'
      },
      axisLabel: {
        color: '#000'
      },
      axisTick: {
        alignWithLabel: true,
        lineStyle: {
          color: '#000'
        }
      },
      splitLine: {
        show: false
      }
    }
  ],
  series: [
    {
      type: 'line',
      name: '售卖次数',
      stack: '人次',
      data: [],
      label: {
        show: true,
        position: 'insideTop',
        offset: [0, 20],
        color: '#000'
      },
      emphasis: {
        label: {
          color: '#000'
        }
      }
    }
  ]
};
