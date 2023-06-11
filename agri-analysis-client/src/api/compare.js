import request from '@/utils/request';
import dayjs from 'dayjs';

export async function getPriceDatas(dateRange, items) {
  const { data } = await request({
    url: '/api/compare/price',
    method: 'post',
    data: {
      dateRange,
      items
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
