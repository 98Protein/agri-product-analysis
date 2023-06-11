export default {
  backgroundColor: '#fff',
  title: {
    text: '农产品价格预测折线图',
    textStyle: {
      color: '#000',
      fontSize: 18,
      fontWeight: 'bold'
    },
    subtext: '已根据您选择的时间段预测价格',
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
      name: '￥',
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
  legend: {
    top: 50,
    icon: 'rect',
    itemWidth: 14,
    itemHeight: 7,
    itemGap: 13, //间隔
    data: ['实际', '预测'],
    right: '4%',
    textStyle: {
      fontSize: 20,
      color: '#73716D'
    }
  },
  series: [
    {
      type: 'line',
      name: '实际',
      stack: '实际',
      data: [],
      emphasis: {
        label: {
          color: '#000'
        }
      }
    },
    {
      type: 'line',
      name: '预测',
      stack: '预测',
      data: [],
      emphasis: {
        label: {
          color: '#f00'
        }
      }
    }
  ]
};
