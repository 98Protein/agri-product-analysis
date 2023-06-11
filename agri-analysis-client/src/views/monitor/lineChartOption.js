import * as echarts from 'echarts';

export function generateSeries(name, id) {
  const color = [Math.floor(Math.random() * 256), Math.floor(Math.random() * 256), Math.floor(Math.random() * 256)];
  return {
    name: name,
    meta: {
      id
    },
    type: 'line',
    smooth: true,
    symbol: 'circle',
    symbolSize: 5,
    showSymbol: false,
    lineStyle: {
      width: 1
    },
    //区域填充样式
    areaStyle: {
      color: new echarts.graphic.LinearGradient(
        0,
        0,
        0,
        1,
        [
          {
            offset: 0,
            color: `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.3)`
          },
          {
            offset: 0.8,
            color: `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0)`
          }
        ],
        false
      ),
      shadowColor: 'rgba(0, 0, 0, 0.1)',
      shadowBlur: 10
    },
    itemStyle: {
      color: `rgb(${color[0]},${color[1]},${color[2]})`,
      borderColor: `rgba(${color[0]},${color[1]},${color[2]},0.27)`,
      borderWidth: 12
    },
    data: []
  };
}

const option = {
  backgroundColor: '#FFFFFF',
  title: {
    top: 0,
    text: '抓取数量',
    textStyle: {
      family: '微软雅黑',
      fontWeight: 'normal',
      fontSize: 30,
      color: '#777879'
      //align: center
    },
    left: '40%'
  },
  //提示框组件
  tooltip: {
    trigger: 'axis', //坐标轴触发
    axisPointer: {
      lineStyle: {
        color: '#EAB543'
      }
    }
  },
  //图例
  legend: {
    top: 50,
    icon: 'rect',
    itemWidth: 14,
    itemHeight: 7,
    itemGap: 13, //间隔
    data: [],
    right: '4%',
    textStyle: {
      fontSize: 20,
      color: '#73716D'
    }
  },
  //网格
  grid: {
    top: 120,
    left: '2%',
    right: '2%',
    bottom: '2%',
    containLabel: true //grid区域是否包含刻度标签
  },
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#6F7072'
        },
        axisLabel: {
          margin: 10,
          fontSize: 20
        }
      },
      data: []
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '(条)',
      axisTick: {
        show: false
      },
      axisLine: {
        lineStyle: {
          color: '#6F7072'
        }
      },
      axisLabel: {
        margin: 10,
        fontSize: 20
      },
      splitLine: {
        lineStyle: {
          color: '#6F7072'
        }
      }
    }
  ],
  series: []
};

export default option;
