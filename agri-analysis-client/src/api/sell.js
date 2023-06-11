import request from '@/utils/request';

export async function getYearSellData(dateRange, marketId, varietyId) {
  const { data } = await request({
    url: '/api/sell/year',
    method: 'post',
    data: {
      dateRange,
      marketId,
      varietyId
    }
  });
  return data.map(item => ({
    time: item.year,
    sum: item.sum
  }));
}

export async function getMonthSellData(dateRange, marketId, varietyId) {
  const { data } = await request({
    url: '/api/sell/month',
    method: 'post',
    data: {
      dateRange,
      marketId,
      varietyId
    }
  });
  return data.map((item) => ({
    time: `${item.year}-` + ('' + item.month).padStart(2, '0'),
    sum: item.sum
  }));
}

export async function getDaySellData(dateRange, marketId, varietyId) {
  const { data } = await request({
    url: '/api/sell/day',
    method: 'post',
    data: {
      dateRange,
      marketId,
      varietyId
    }
  });
  return data.map(item => ({
    time: item.date,
    sum: item.sell_number
  }));
}
