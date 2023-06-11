import request from '@/utils/request';

export async function getCountryData(date, varietyId) {
  const { data } = await request({
    url: '/api/region/country',
    method: 'post',
    data: {
      date,
      varietyId
    }
  });

  return data;
}

export async function getProvinceData(date, varietyId, provinceId) {
  const { data } = await request({
    url: '/api/region/province/' + provinceId,
    method: 'post',
    data: {
      date,
      varietyId
    }
  });
  return data;
}

export async function getCityData(date, varietyId, cityId) {
  const { data } = await request({
    url: '/api/region/city/' + cityId,
    method: 'post',
    data: {
      date,
      varietyId
    }
  });
  return data;
}
