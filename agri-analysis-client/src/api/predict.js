import request from '@/utils/request';
import dayjs from 'dayjs';

export async function getPredictData(dateRange, marketId, varietyId, predictDays) {
  const { data } = await request({
    url: '/api/predict',
    data: {
      dateRange,
      marketId,
      varietyId,
      predictDays
    },
    method: 'post'
  });

  return {
    history: data.history.map((item) => ({
      date: item.ds,
      price: item.y
    })),
    predict: data.predict.map((item) => ({
      date: dayjs(+item.ds).format('YYYY-MM-DD'),
      price: item.yhat.toFixed(2)
    }))
  };
}
