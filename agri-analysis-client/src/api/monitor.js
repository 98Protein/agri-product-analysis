import request from '@/utils/request';
import dayjs from 'dayjs';

export async function getBasicInfo() {
  const { data } = await request({
    url: '/api/monitor/basic',
    method: 'get'
  });
  return data;
}

export function runScrapy(timeRange) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/monitor/scrapy',
      data: {
        timeRange
      },
      method: 'post'
    })
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        reject(error);
      });
  })
}

export async function stopScrapy() {
  const { data } = await request({
    url: '/api/monitor/stop_scrapy',
    data: {},
    method: 'post'
  });
  return data
}

export async function getCrawls(dateRange, market) {
  let { data } = await request({
    url: '/api/monitor/crawls',
    method: 'post',
    data: {
      dateRange,
      market
    }
  });

  const dates = []
  let current = dayjs(dateRange[0])
  while (current.diff(dateRange[1], 'day') <= 0) {
    dates.push(current)
    current = current.add(1, 'day')
  }


  return dates.map(date => date.format('YYYY-MM-DD')).map(date => ({
    date: date,
    items: data.filter(item => item.date === date)
  }))
}
